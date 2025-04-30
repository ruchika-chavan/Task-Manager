import unittest
import json
from app import app  # Make sure 'app.py' and 'test_apps.py' are in the same folder

class TaskManagerTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @app.route('/tasks', methods=['POST'])
    def test_add_task(self):
        task_data = {
            "task": "Test Task",
            "deadline": "2022-04-20",
            "importance": "High"
        }

        response = self.app.post('/tasks',
                                 data=json.dumps(task_data),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_delete_task(self):
        # First, add a task
        task_data = {
            "task": "Delete Me",
            "deadline": "2040-04-22",
            "importance": "Low"
        }
        add_response = self.app.post('/tasks',
                                     data=json.dumps(task_data),
                                     content_type='application/json')
        self.assertEqual(add_response.status_code, 201)

        # Fetch all tasks and get the last added one
        get_response = self.app.get('/tasks')
        tasks = get_response.get_json()
        self.assertGreater(len(tasks), 0)
        task_id = tasks[-1]['id']  # Get the ID of the last added task

        # Delete the task
        delete_response = self.app.delete(f'/tasks/{task_id}')
        self.assertEqual(delete_response.status_code, 200)
        self.assertIn("message", delete_response.get_json())

if __name__ == "__main__":
    unittest.main()
