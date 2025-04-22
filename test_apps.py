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
            "deadline": "2040-04-20",
            "importance": "High"
        }

        response = self.app.post('/tasks',
                                 data=json.dumps(task_data),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_delete_task(self):
    # Add a task first
        task_data = {
            "task": "Test Task",
            "deadline": "2025-05-01",
            "importance": "High"
        }
        response = self.app.post('/tasks',
                                 data=json.dumps(task_data),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)
    
        # Get the ID of the task just added
        task_id = response.json['id']  # Adjust this line based on the actual response
    
        # Now delete the task
        response = self.app.delete(f'/tasks/{task_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json)
        self.assertEqual(response.json['message'], 'Task deleted successfully')

if __name__ == "__main__":
    unittest.main()
