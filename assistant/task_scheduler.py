import schedule
import time

tasks = []

def add_task(name, interval, action):
    tasks.append((name, interval, action))
    schedule.every(interval).seconds.do(action)
    return f"Task '{name}' scheduled every {interval} seconds."

def run_tasks():
    while True:
        schedule.run_pending()
        time.sleep(1)
