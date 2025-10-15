# 代码生成时间: 2025-10-16 02:25:24
import asyncio
from sanic import Sanic, response
from sanic.exceptions import ServerError, NotFound
from sanic.response import json, html
from jinja2 import Environment, FileSystemLoader
import os

# Define the path to the templates directory
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates')

# Initialize the Sanic app
app = Sanic("BreadcrumbsNav")

# Initialize the Jinja2 environment with the templates directory
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

# Define the route for the home page
@app.route("/", methods=['GET'])
async def home(request):
    # Render the home page template with breadcrumbs
    template = env.get_template("home.html")
    return response.html(template.render(breadcrumbs=[{"text": "Home", "url": "/"}]))

# Define the route for the about page
@app.route("/about", methods=['GET'])
async def about(request):
    # Render the about page template with breadcrumbs
    template = env.get_template("about.html")
    return response.html(template.render(breadcrumbs=[
        {"text": "Home", "url": "/"},
        {"text": "About", "url": "/about"}
    ]))

# Define the route for the contact page
@app.route("/contact", methods=['GET'])
async def contact(request):
    # Render the contact page template with breadcrumbs
    template = env.get_template("contact.html")
    return response.html(template.render(breadcrumbs=[
        {"text": "Home", "url": "/"},
        {"text": "Contact", "url": "/contact"}
    ]))

# Define the error handler for ServerError
@app.exception(ServerError)
async def server_error(request, exception):
    # Return a 500 error response with a message
    return response.json({
        "error": "Internal Server Error",
        "message": str(exception)
    }, status=500)

# Define the error handler for NotFound
@app.exception(NotFound)
async def not_found(request, exception):
    # Return a 404 error response
    return response.json({
        "error": "Not Found"
    }, status=404)

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
