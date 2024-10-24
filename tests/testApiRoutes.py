import unittest
import warnings
import json
from app import create_app

class TestAPI(unittest.TestCase):
    """Unit tests for the API endpoints of the rule engine."""

    def setUp(self):
        """Set up the test client for the Flask application."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.testing = True

    def test_create_rule_api(self):
        """Test the API for creating a rule."""
        rule_string = "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
        response = self.client.post('/create_rule',
                                    data=json.dumps({'rule_string': rule_string}),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertIn('ast', response.json)
        print("Created AST via API:", response.json['ast'])

    def test_combine_rules_api(self):
        """Test the API for combining multiple rules."""
        rule1 = "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
        rule2 = "((age > 30 AND department = 'Marketing')) AND (salary > 20000 OR experience > 5)"

        response = self.client.post('/combine_rules',
                                    data=json.dumps({'rule_strings': [rule1, rule2]}),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertIn('combined_ast', response.json)
        print("Combined AST via API:", response.json['combined_ast'])

    def test_evaluate_rule_api(self):
        """Test the API for evaluating a rule against data."""
        rule_string = "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"

        # Create the rule to get the AST
        create_response = self.client.post('/create_rule',
                                           data=json.dumps({'rule_string': rule_string}),
                                           content_type='application/json')
        ast_json = create_response.json['ast']

        # Sample data for evaluation
        data = {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}

        # Evaluate the rule
        evaluate_response = self.client.post('/evaluate_rule',
                                             data=json.dumps({'ast': ast_json, 'data': data}),
                                             content_type='application/json')

        self.assertEqual(evaluate_response.status_code, 200)
        print("Evaluation Result via API:", evaluate_response.json['result'])
        # Adjust the assertion based on the logic of the rules
        self.assertFalse(evaluate_response.json['result'])  # Expected to be False


if __name__ == '__main__':
    unittest.main()
