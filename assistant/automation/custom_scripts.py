import subprocess
import os
import json
import threading
import time
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from utils.logger import log

# Load configuration
try:
    with open("/Users/vishal_pansare/PycharmProjects/Buntroid/assistant/automation/config.json", "r") as config_file:
        config = json.load(config_file)
except FileNotFoundError:
    log("Error: config.json file not found.", "error")
    # exit(1)
except json.JSONDecodeError:
    log("Error: Failed to parse config.json. Check the file format.", "error")
    # exit(1)

SCRIPT_PATHS = config.get("scripts", {}).get("paths", [])
SCHEDULE_INTERVALS = config.get("scripts", {}).get("schedule", {})
SCRIPTS_CRON = config.get("scripts", {}).get("cron", {})

if not SCRIPT_PATHS:
    log("Error: No script paths found in config.json.", "error")
    exit(1)

if not SCHEDULE_INTERVALS and not SCRIPTS_CRON:
    log("Error: No schedule or cron schedule found in config.json.", "error")
    exit(1)

scheduler = BackgroundScheduler()


def log_script_execution(script_path, status, message):
    """
    Log the execution status of a script (success or failure).

    Parameters:
        script_path (str): The path to the script.
        status (str): The status of the execution (success or failure).
        message (str): Additional message or output.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log(f"{timestamp} - {script_path} - {status}: {message}", "info" if status == "success" else "error")


def run_script(script_path):
    """
    Execute a custom script (Python, Shell, Batch).

    Parameters:
        script_path (str): Path to the script to execute.

    Returns:
        str: The output or error message.
    """
    start_time = datetime.now()
    log_script_execution(script_path, "started", f"Started execution at {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    try:
        if not os.path.exists(script_path):
            log_script_execution(script_path, "failed", "Script not found.")
            return "Script not found."

        # Detect script type based on file extension
        extension = os.path.splitext(script_path)[1].lower()
        command = []

        if extension == ".py":
            command = ["python", script_path]  # Python script
        elif extension == ".sh":
            command = ["bash", script_path]  # Shell script
        elif extension == ".bat":
            command = [script_path]  # Batch file (Windows)
        else:
            log_script_execution(script_path, "failed", f"Unsupported script type: {extension}")
            return f"Unsupported script type: {extension}."

        # Execute the script
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )

        end_time = datetime.now()
        log_script_execution(script_path, "success", f"Execution completed at {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        return result.stdout

    except subprocess.CalledProcessError as e:
        log_script_execution(script_path, "failed", f"Error: {e.stderr}")
        return f"Error executing script: {e.stderr}"
    except Exception as e:
        log_script_execution(script_path, "failed", f"Unexpected error: {str(e)}")
        return f"Unexpected error: {str(e)}"


def schedule_script(script_path, interval):
    """
    Schedule a custom script to run at a specified interval using APScheduler.

    Parameters:
        script_path (str): The path to the script.
        interval (int): Interval in seconds.
    """
    log(f"Scheduling script {script_path} every {interval} seconds.", "info")
    scheduler.add_job(run_script, IntervalTrigger(seconds=interval), args=[script_path], id=script_path)


def schedule_cron_script(script_path, cron_expression):
    """
    Schedule a custom script using a cron expression.

    Parameters:
        script_path (str): The path to the script.
        cron_expression (str): The cron expression for scheduling.
    """
    log(f"Scheduling script {script_path} with cron expression: {cron_expression}", "info")
    scheduler.add_job(run_script, CronTrigger.from_crontab(cron_expression), args=[script_path], id=script_path)


def start_scheduled_scripts():
    """
    Start all scheduled scripts using APScheduler.
    """
    # Schedule scripts based on intervals or cron expressions
    for script_path, interval in SCHEDULE_INTERVALS.items():
        if script_path in SCRIPT_PATHS:
            # Ensure interval is an integer
            try:
                interval = int(interval)
            except ValueError:
                log(f"Invalid interval for {script_path}. Interval must be an integer.", "error")
                continue  # Skip this script if the interval is invalid
            schedule_script(script_path, interval)

    for script_path, cron_expression in SCRIPTS_CRON.items():
        if script_path in SCRIPT_PATHS:
            schedule_cron_script(script_path, cron_expression)

    # Start the APScheduler
    scheduler.start()


def manual_trigger_script(script_path):
    """
    Manually trigger the execution of a script.

    Parameters:
        script_path (str): The path to the script.
    """
    log(f"Manually triggering script: {script_path}", "info")
    result = run_script(script_path)
    log(f"Manual script run result: {result}", "info")


def pause_script(script_path):
    """
    Pause a running script using APScheduler.

    Parameters:
        script_path (str): The script to pause.
    """
    job = scheduler.get_job(script_path)
    if job:
        job.pause()
        log(f"Paused script: {script_path}", "info")
    else:
        log(f"Script {script_path} not found in scheduler.", "error")


def resume_script(script_path):
    """
    Resume a paused script using APScheduler.

    Parameters:
        script_path (str): The script to resume.
    """
    job = scheduler.get_job(script_path)
    if job:
        job.resume()
        log(f"Resumed script: {script_path}", "info")
    else:
        log(f"Script {script_path} not found in scheduler.", "error")


def remove_script(script_path):
    """
    Remove a script from the scheduler.

    Parameters:
        script_path (str): The script to remove.
    """
    job = scheduler.get_job(script_path)
    if job:
        job.remove()
        log(f"Removed script: {script_path}", "info")
    else:
        log(f"Script {script_path} not found in scheduler.", "error")


def list_available_scripts(script_directory="scripts"):
    """
    Lists all available scripts in the specified directory.

    Parameters:
        script_directory (str): The directory where the scripts are stored.

    Returns:
        list: A list of script filenames.
    """
    if not os.path.exists(script_directory):
        log(f"Error: Directory '{script_directory}' does not exist.", "error")
        return []

    scripts = [f for f in os.listdir(script_directory) if os.path.isfile(os.path.join(script_directory, f))]
    log(f"Available scripts in '{script_directory}': {scripts}", "info")
    return scripts


def run_single_script(script_path):
    """
    Executes a single script (can be a Python, Shell, or Batch script).

    Parameters:
        script_path (str): The path to the script to be run.

    Returns:
        str: The result or status of the execution.
    """
    try:
        # Check if the file exists
        if not os.path.isfile(script_path):
            log(f"Error: The script '{script_path}' does not exist.", "error")
            return f"Error: The script '{script_path}' does not exist."

        # Determine script type and run accordingly
        if script_path.endswith(".py"):
            result = subprocess.run(['python', script_path], capture_output=True, text=True)
        elif script_path.endswith(".sh"):
            result = subprocess.run(['bash', script_path], capture_output=True, text=True)
        elif script_path.endswith(".bat"):
            result = subprocess.run([script_path], capture_output=True, text=True)
        else:
            log(f"Error: Unsupported script type for '{script_path}'.", "error")
            return f"Error: Unsupported script type for '{script_path}'."

        # Check for errors in execution
        if result.returncode != 0:
            log(f"Error running script '{script_path}': {result.stderr}", "error")
            return f"Error running script: {result.stderr}"

        log(f"Script '{script_path}' executed successfully.", "info")
        return f"Script executed successfully: {result.stdout}"

    except Exception as e:
        log(f"An error occurred while running the script '{script_path}': {str(e)}", "error")
        return f"An error occurred while running the script: {str(e)}"


if __name__ == "__main__":
    # Create a shutdown event to manage graceful shutdown
    print(list_available_scripts())
