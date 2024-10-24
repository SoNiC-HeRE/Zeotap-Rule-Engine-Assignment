# app/apiRoutes.py

from functools import wraps
from typing import Dict, List, Any, Callable
from flask import request, jsonify, render_template, Response
import logging
from http import HTTPStatus

from app.dbConfig import save_rule
from app.engineRules import (
    create_rule,
    combine_rules,
    evaluate_rule,
    serialize_ast,
    deserialize_ast,
    RuleEngineError
)

# Configure logging
logger = logging.getLogger(__name__)

# Custom types
JsonResponse = Response
RuleData = Dict[str, Any]


def validate_json_request(required_fields: List[str]) -> Callable:
    """
    Decorator to validate JSON request data.

    Args:
        required_fields: List of required fields in the request JSON

    Returns:
        Decorated function
    """

    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated_function(*args, **kwargs) -> JsonResponse:
            if not request.is_json:
                return jsonify({
                    "status": "error",
                    "message": "Request must be JSON"
                }), HTTPStatus.BAD_REQUEST

            data = request.get_json()
            missing_fields = [field for field in required_fields if field not in data]

            if missing_fields:
                return jsonify({
                    "status": "error",
                    "message": f"Missing required fields: {', '.join(missing_fields)}"
                }), HTTPStatus.BAD_REQUEST

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def handle_rule_engine_error(f: Callable) -> Callable:
    """
    Decorator to handle RuleEngineError exceptions.

    Args:
        f: Function to decorate

    Returns:
        Decorated function
    """

    @wraps(f)
    def decorated_function(*args, **kwargs) -> JsonResponse:
        try:
            return f(*args, **kwargs)
        except RuleEngineError as e:
            logger.error(f"Rule engine error: {str(e)}", exc_info=True)
            return jsonify({
                "status": "error",
                "message": str(e)
            }), HTTPStatus.BAD_REQUEST
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            return jsonify({
                "status": "error",
                "message": "An unexpected error occurred"
            }), HTTPStatus.INTERNAL_SERVER_ERROR

    return decorated_function


def create_success_response(data: Dict[str, Any]) -> JsonResponse:
    """
    Create a standardized success response.

    Args:
        data: Response data

    Returns:
        JSON response
    """
    return jsonify({
        "status": "success",
        **data
    })


def init_app(app) -> None:
    """
    Initialize Flask application routes.

    Args:
        app: Flask application instance
    """

    @app.route('/')
    def index() -> str:
        """Render the main application page."""
        return render_template('index.html')

    @app.route('/create_rule', methods=['POST'])
    @validate_json_request(['rule_string'])
    @handle_rule_engine_error
    def create_rule_api() -> JsonResponse:
        """
        Create a new rule from a rule string.

        Request JSON:
            rule_string: String representation of the rule

        Returns:
            JSON response with created AST
        """
        rule_string = request.json['rule_string']
        logger.info(f"Creating rule: {rule_string}")

        ast = create_rule(rule_string)
        ast_json = serialize_ast(ast)
        save_rule(rule_string, ast_json)

        return create_success_response({"ast": ast_json})

    @app.route('/combine_rules', methods=['POST'])
    @validate_json_request(['rule_strings'])
    @handle_rule_engine_error
    def combine_rules_api() -> JsonResponse:
        """
        Combine multiple rules into a single rule.

        Request JSON:
            rule_strings: List of rule strings to combine

        Returns:
            JSON response with combined AST
        """
        rule_strings = request.json['rule_strings']
        logger.info(f"Combining {len(rule_strings)} rules")

        if not isinstance(rule_strings, list):
            return jsonify({
                "status": "error",
                "message": "rule_strings must be a list"
            }), HTTPStatus.BAD_REQUEST

        rules = [create_rule(rule) for rule in rule_strings]
        combined_ast = combine_rules(rules)
        combined_ast_json = serialize_ast(combined_ast)
        save_rule("combined_rule", combined_ast_json)

        return create_success_response({"combined_ast": combined_ast_json})

    @app.route('/evaluate_rule', methods=['POST'])
    @validate_json_request(['ast', 'data'])
    @handle_rule_engine_error
    def evaluate_rule_api() -> JsonResponse:
        """
        Evaluate a rule against provided data.

        Request JSON:
            ast: JSON representation of the rule AST
            data: Data to evaluate the rule against

        Returns:
            JSON response with evaluation result
        """
        ast_json = request.json['ast']
        data = request.json['data']
        logger.info("Evaluating rule")

        ast = deserialize_ast(ast_json)
        result = evaluate_rule(ast, data)

        return create_success_response({"result": result})

    # Register error handlers
    @app.errorhandler(404)
    def not_found_error(error) -> JsonResponse:
        """Handle 404 errors."""
        return jsonify({
            "status": "error",
            "message": "Resource not found"
        }), HTTPStatus.NOT_FOUND

    @app.errorhandler(405)
    def method_not_allowed_error(error) -> JsonResponse:
        """Handle 405 errors."""
        return jsonify({
            "status": "error",
            "message": "Method not allowed"
        }), HTTPStatus.METHOD_NOT_ALLOWED