import unittest
from scripts.reminders import add_reminder, check_reminders, list_reminders
from scripts.notes import add_note, remove_note, list_notes
import time

from scripts.task_manager import add_task, list_tasks, remove_task


class TestAssistantModules(unittest.TestCase):
    def test_reminders(self):
        add_reminder("Test Reminder", 2)
        time.sleep(3)  # Wait for the reminder to be due
        self.assertEqual(check_reminders(), ["Test Reminder"])
        self.assertEqual(list_reminders(), [])

    def test_notes(self):
        add_note("Test Note")
        self.assertIn("Test Note", list_notes())
        remove_note("Test Note")
        self.assertNotIn("Test Note", list_notes())

    def test_add_task(self):
        add_task("Buy groceries")
        tasks = list_tasks()
        self.assertIn("Buy groceries", tasks)

    def test_remove_task(self):
        add_task("Buy grocery")
        remove_task("Buy grocery")
        tasks = list_tasks()
        self.assertNotIn("Buy grocery", tasks)


if __name__ == '__main__':
    unittest.main()
