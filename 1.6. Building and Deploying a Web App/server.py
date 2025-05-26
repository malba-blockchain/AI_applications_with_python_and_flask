from flask import Flask, render_template, request, jsonify
from Maths.mathematics import summation, subtraction, multiplication
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask("Mathematics Problem Solver")

def validate_and_convert_numbers(num1_str, num2_str):

    if num1_str is None or num2_str is None:
        missing_params = []
        if num1_str is None:
            missing_params.append('num1')
        if num2_str is None:
            missing_params.append('num2')
        return None, None, f"Missing required parameters: {', '.join(missing_params)}"
    
    try:
        num1 = float(num1_str)
    except (ValueError, TypeError):
        return None, None, f"Invalid input for num1: '{num1_str}'. Please provide a valid number."
    
    try:
        num2 = float(num2_str)
    except (ValueError, TypeError):
        return None, None, f"Invalid input for num2: '{num2_str}'. Please provide a valid number."
    
    # Check for infinity and NaN
    if not (abs(num1) < float('inf')) or num1 != num1:  # NaN check
        return None, None, f"Invalid input for num1: '{num1_str}'. Number is too large or not a valid number."
    
    if not (abs(num2) < float('inf')) or num2 != num2:  # NaN check
        return None, None, f"Invalid input for num2: '{num2_str}'. Number is too large or not a valid number."
    
    return num1, num2, None

def format_result(result):
    try:
        if isinstance(result, (int, float)) and result.is_integer():
            return int(result)
        return result
    except (AttributeError, OverflowError):
        return result

def create_error_response(error_message, status_code=400):
    logger.warning(f"Error response: {error_message}")
    return jsonify({
        'error': True,
        'message': error_message,
        'result': None
    }), status_code

def create_success_response(result):
    # For backward compatibility, return string if request expects text
    if request.headers.get('Accept', '').startswith('application/json'):
        return jsonify({
            'error': False,
            'message': 'Success',
            'result': result
        })
    else:
        return str(result)

@app.route("/sum")
def sum_route():
    """Addition endpoint with error handling."""
    try:
        num1_str = request.args.get('num1')
        num2_str = request.args.get('num2')
        
        num1, num2, error = validate_and_convert_numbers(num1_str, num2_str)
        if error:
            return create_error_response(error)
        
        result = summation(num1, num2)
        formatted_result = format_result(result)
        
        logger.info(f"Sum calculation: {num1} + {num2} = {formatted_result}")
        return create_success_response(formatted_result)
        
    except Exception as e:
        logger.error(f"Unexpected error in sum_route: {str(e)}")
        return create_error_response("An unexpected error occurred during addition.", 500)

@app.route("/sub")
def sub_route():
    """Subtraction endpoint with error handling."""
    try:
        num1_str = request.args.get('num1')
        num2_str = request.args.get('num2')
        
        num1, num2, error = validate_and_convert_numbers(num1_str, num2_str)
        if error:
            return create_error_response(error)
        
        result = subtraction(num1, num2)
        formatted_result = format_result(result)
        
        logger.info(f"Subtraction calculation: {num1} - {num2} = {formatted_result}")
        return create_success_response(formatted_result)
        
    except Exception as e:
        logger.error(f"Unexpected error in sub_route: {str(e)}")
        return create_error_response("An unexpected error occurred during subtraction.", 500)

@app.route("/mul")
def mul_route():
    """Multiplication endpoint with error handling."""
    try:
        num1_str = request.args.get('num1')
        num2_str = request.args.get('num2')
        
        num1, num2, error = validate_and_convert_numbers(num1_str, num2_str)
        if error:
            return create_error_response(error)
        
        result = multiplication(num1, num2)
        formatted_result = format_result(result)
        
        logger.info(f"Multiplication calculation: {num1} * {num2} = {formatted_result}")
        return create_success_response(formatted_result)
        
    except Exception as e:
        logger.error(f"Unexpected error in mul_route: {str(e)}")
        return create_error_response("An unexpected error occurred during multiplication.", 500)

@app.route("/")
def render_index_page():
    """Render the main page with error handling."""
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error rendering index page: {str(e)}")
        return create_error_response("Unable to load the main page.", 500)

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors."""
    return create_error_response("Endpoint not found. Available endpoints: /sum, /sub, /mul", 404)

@app.errorhandler(405)
def method_not_allowed_error(error):
    """Handle 405 Method Not Allowed errors."""
    return create_error_response("Method not allowed for this endpoint.", 405)

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 Internal Server errors."""
    logger.error(f"Internal server error: {str(error)}")
    return create_error_response("Internal server error occurred.", 500)

# Health check endpoint
@app.route("/health")
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'message': 'Mathematics Problem Solver is running'
    })

if __name__ == "__main__":
    try:
        logger.info("Starting Mathematics Problem Solver server...")
        app.run(host="0.0.0.0", port=8080, debug=False)
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        print(f"Error starting server: {str(e)}")