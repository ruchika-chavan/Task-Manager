import unittest
import json
from app import app  # Make sure 'app.py' and 'test_apps.py' are in the same folder

class TaskManagerTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @app.route('/tasks', methods=['POST'])
    def test_add_task():
    try:
        data = request.get_json()
        print("Received data:", data)  # Add this line

        task = data.get('task')
        deadline = data.get('deadline')
        importance = data.get('importance')

        if not all([task, deadline, importance]):
            return jsonify({'error': 'Missing required fields'}), 400

        # If there's a date validation or transformation, wrap it in try-except and log

        # Add the task to DB or Firebase...

        return jsonify({'message': 'Task added successfully'}), 201

    except Exception as e:
        print("Error in /tasks:", str(e))
        return jsonify({'error': 'Something went wrong'}), 400


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
