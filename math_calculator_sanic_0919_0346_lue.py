# 代码生成时间: 2025-09-19 03:46:39
from sanic import Sanic, response
from sanic.exceptions import ServerError
from sanic.request import Request
from sanic.response import json as json_response
import math
def add(a, b):
    """Add two numbers together."""
    return a + b
def subtract(a, b):
    """Subtract the second number from the first."""
    return a - b
def multiply(a, b):
    """Multiply two numbers together."""
    return a * b
def divide(a, b):
    """Divide the first number by the second.
    Raise ValueError if division by zero is attempted."""
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b
def square(a):
    """Square a number."""
    return a * a
def square_root(a):
    """Calculate the square root of a number.
    Raise ValueError if the number is negative."""
    if a < 0:
        raise ValueError("Cannot calculate the square root of a negative number.")
    return math.sqrt(a)
def handle_404(request: Request, exception):
    """Handle 404 errors."""
    return response.json({"error": "Method not found."}, status=404)
def handle_500(request: Request, exception):
    """Handle 500 errors."""
    return response.json({"error": "Internal server error."}, status=500)
def calculate(request: Request, operation: str, a: float, b: float=None):
    """Endpoint to handle mathematical calculations."""
    try:
        if operation == "add":
            return response.json({"result": add(a, b)})
        elif operation == "subtract":
            return response.json({"result": subtract(a, b)})
        elif operation == "multiply":
            return response.json({"result": multiply(a, b)})
        elif operation == "divide":
            return response.json({"result": divide(a, b)})
        elif operation == "square":
            return response.json({"result": square(a)})
        elif operation == "square_root":
            return response.json({"result": square_root(a)})
        else:
            raise ValueError("Invalid operation.")
    except ValueError as e:
        return response.json({"error": str(e)}, status=400)app = Sanic("Math Calculator")\@app.exception(ServerError)
def exception_handler(request, exception):
    """Handle unexpected server errors."""
    return response.json({"error": str(exception)}, status=500)\@app.route("/calculate/<str:operation>/<float:a>/<float:b>", methods=["POST"])
async def calculate_route(request, operation, a, b=None):
    """Route to perform calculations on two numbers."""
    return calculate(request, operation, a, b)\@app.route("/calculate/<str:operation>/<float:a>", methods=["POST"])
async def calculate_single_route(request, operation, a):
    """Route to perform single number calculations."""
    return calculate(request, operation, a)\@app.exception(404)
def handle_404(request, exception):
    return response.json({"error": "Method not found."}, status=404)\@app.exception(500)
def handle_500(request, exception):
    return response.json({"error": "Internal server error."}, status=500)if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)