import unittest
import json
from app import app, init_db
from datetime import datetime

class TaskManagerTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Initialize the database (set up before tests)
        app.config['TESTING'] = True
        init_db()

        init_db()

    def setUp(self):
        # Set up the testing environment, run the app in testing mode
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        # Clean up after each test, could add more cleanup logic if necessary
        pass

    # Test POST /tasks to add a new task
    def test_add_task(self):
        task_data = {
            "task": "Test Task",
            "deadline": (datetime.today().date()).strftime("%Y-%m-%d"),  # Use today's date as deadline
            "importance": "High"
        }

        response = self.app.post('/tasks', 
                                 data=json.dumps(task_data), 
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('Task added successfully', str(response.data))

    # Test POST /tasks with missing fields (error case)
    def test_add_task_missing_fields(self):
        task_data = {
            "task": "Incomplete Task",
            "importance": "Moderate"
            # Missing deadline
        }
        response = self.app.post('/tasks', 
                                 data=json.dumps(task_data), 
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing fields', str(response.data))

    # Test DELETE /tasks/<task_id> to delete a task
    def test_delete_task(self):
        # First, add a task to delete
        task_data = {
            "task": "Delete Me",
            "deadline": (datetime.today().date()).strftime("%Y-%m-%d"),
            "importance": "Low"
        }

        self.app.post('/tasks', 
                      data=json.dumps(task_data), 
                      content_type='application/json')

        # Now delete the task (task_id = 1 in this case)
        response = self.app.delete('/tasks/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Task deleted successfully', str(response.data))

    # Test DELETE /tasks to delete all tasks
    def test_delete_all_tasks(self):
        # First, add some tasks
        task_data_1 = {
            "task": "Task 1",
            "deadline": (datetime.today().date()).strftime("%Y-%m-%d"),
            "importance": "Moderate"
        }
        task_data_2 = {
            "task": "Task 2",
            "deadline": (datetime.today().date()).strftime("%Y-%m-%d"),
            "importance": "Low"
        }

        self.app.post('/tasks', 
                      data=json.dumps(task_data_1), 
                      content_type='application/json')
        self.app.post('/tasks', 
                      data=json.dumps(task_data_2), 
                      content_type='application/json')

        # Now delete all tasks
        response = self.app.delete('/tasks')
        self.assertEqual(response.status_code, 200)
        self.assertIn('All tasks deleted', str(response.data))

    # Test POST /tasks with deadline in the past
    def test_add_task_past_deadline(self):
        past_deadline = (datetime.today().date().replace(year=datetime.today().year - 1)).strftime("%Y-%m-%d")
        task_data = {
            "task": "Past Deadline Task",
            "deadline": past_deadline,
            "importance": "High"
        }

        response = self.app.post('/tasks', 
                                 data=json.dumps(task_data), 
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Deadline cannot be in the past!', str(response.data))

if __name__ == '__main__':
    unittest.main()
