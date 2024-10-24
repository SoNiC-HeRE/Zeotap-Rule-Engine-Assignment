# app/engineRules.py
from app.astStructure import Node

class RuleEngineError(Exception):
    """Custom exception for rule engine errors."""
    pass

def create_rule(rule_string):
    """Creates a rule AST from a rule string."""
    if not isinstance(rule_string, str) or not rule_string:
        raise RuleEngineError("Invalid rule string format.")

    # Placeholder for actual parsing; should be implemented with real logic
    try:
        # Create operand nodes
        operands = [
            Node("operand", value=("age", ">", 30)),
            Node("operand", value=("department", "=", "Sales")),
            Node("operand", value=("salary", ">", 50000)),
            Node("operand", value=("experience", ">", 5))
        ]

        # Combine operands with AND operators
        and_nodes = [Node("operator", left=operands[i], right=operands[i+1], value="AND") for i in range(0, len(operands), 2)]

        # Create the root node
        root_node = and_nodes[0]
        for and_node in and_nodes[1:]:
            root_node = Node("operator", left=root_node, right=and_node, value="AND")

        return root_node
    except Exception as e:
        raise RuleEngineError(f"Failed to create rule: {e}")

def combine_rules(rules):
    """Combines multiple rules into a single AST using AND operators."""
    if not rules:
        return None

    combined_ast = rules[0]
    for rule in rules[1:]:
        combined_ast = Node("operator", left=combined_ast, right=rule, value="AND")

    return combined_ast

def evaluate_node(node, data):
    """Evaluates a single AST node against the provided data."""
    if node.node_type == "operand":
        attribute, operator, value = node.value
        data_value = data.get(attribute)

        if operator == ">":
            return data_value > value
        elif operator == "<":
            return data_value < value
        elif operator == "=":
            return data_value == value
        return False

    elif node.node_type == "operator":
        left_eval = evaluate_node(node.left, data)
        right_eval = evaluate_node(node.right, data)

        return left_eval and right_eval if node.value == "AND" else left_eval or right_eval

    return False

def deserialize_ast(node_dict):
    """Deserializes a dictionary into an AST Node."""
    if node_dict is None:
        return None
    return Node(
        node_type=node_dict['node_type'],
        value=node_dict.get('value'),
        left=deserialize_ast(node_dict.get('left')),
        right=deserialize_ast(node_dict.get('right'))
    )

def serialize_ast(node):
    """Serializes an AST Node into a dictionary."""
    if node is None:
        return None
    return {
        'node_type': node.node_type,
        'value': node.value,
        'left': serialize_ast(node.left),
        'right': serialize_ast(node.right)
    }

def evaluate_rule(ast, data):
    """Evaluates the entire rule AST against the provided data."""
    if not isinstance(data, dict):
        raise RuleEngineError("Invalid data format.")
    return evaluate_node(ast, data)
