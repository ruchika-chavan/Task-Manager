import unittest
import json
from app import app

class TaskManagerTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        cls.app = app.test_client()

    def setUp(self):
        self.app.testing = True

    def tearDown(self):
        pass

    # Test POST /tasks to add a new task
    def test_add_task(self):
        task_data = {
            "task": "Test Task",
            "deadline": "2025-04-20",  # Use a specific deadline
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


if __name__ == '__main__':
    unittest.main()
