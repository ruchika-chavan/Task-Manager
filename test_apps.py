import unittest
import json
from app import app  # Make sure 'app.py' and 'test_apps.py' are in the same folder

class TaskManagerTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_add_task(self):
        task_data = {
            "task": "Test Task",
            "deadline": "2025-04-20",
            "importance": "High"
        }

        response = self.app.post('/tasks',
                                 data=json.dumps(task_data),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_missing_fields(self):
        task_data = {
            "task": "Incomplete Task"
        }
        response = self.app.post('/tasks',
                                 data=json.dumps(task_data),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)

if __name__ == "__main__":
    unittest.main()
