# tests/testEngineRules.py
import unittest
from app.engineRules import create_rule, combine_rules, evaluate_rule, serialize_ast, deserialize_ast


class TestRules(unittest.TestCase):
    """Unit tests for the rule engine functionalities."""

    def test_create_rule(self):
        """Test the creation of an AST from a rule string."""
        rule_string = "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
        ast = create_rule(rule_string)

        self.assertIsNotNone(ast)
        print("Created AST:", ast)

    def test_combine_rules(self):
        """Test combining multiple rule ASTs into a single AST."""
        rule1 = create_rule(
            "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)")
        rule2 = create_rule("((age > 30 AND department = 'Marketing')) AND (salary > 20000 OR experience > 5)")

        combined_ast = combine_rules([rule1, rule2])

        self.assertIsNotNone(combined_ast)
        print("Combined AST:", combined_ast)

if __name__ == '__main__':
    unittest.main()
