# 代码生成时间: 2025-09-18 15:59:43
import os
from sanic import Sanic, response
from sanic.request import Request
from sanic.response import HTTPResponse, json
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from pandas import DataFrame

# Initialize the Sanic application
app = Sanic("ExcelGenerator")

# Define the route for generating an Excel file
@app.route("/generate", methods=["GET"], strict_slashes=False)
async def generate_excel(request: Request):
    # Create a new workbook
    wb = Workbook()
    ws = wb.active

    # Assume we have a DataFrame from some source
    # Here is an example DataFrame
    data = {'Name': ['Alice', 'Bob', 'Charlie'],
            'Age': [25, 30, 35]}
    df = DataFrame(data)

    # Convert DataFrame to rows and add to Excel worksheet
    for r_idx, row in enumerate(dataframe_to_rows(df, index=False, header=True), 1):
        for c_idx, value in enumerate(row, 1):
            ws.cell(row=r_idx, column=c_idx, value=value)

    # Save the workbook to a temporary file
    filename = "temp_excel_file.xlsx"
    wb.save(filename)

    # The file path
    file_path = os.path.join(os.getcwd(), filename)

    # Remove the file after sending it
    def remove_file(file_path):
        os.remove(file_path)
    request.app.add_task(remove_file, file_path)

    # Return the file as a HTTP response
    return response.file(file_path, filename=filename)

# Error handler for 404 Not Found
@app.exception(404)
async def not_found_exception(request: Request, exception: Exception):
    return response.json({'error': 'The endpoint you requested was not found.'}, status=404)

# Error handler for Server Error (500)
@app.exception(500)
async def server_error_exception(request: Request, exception: Exception):
    return response.json({'error': 'Internal server error.'}, status=500)

# Run the server
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)