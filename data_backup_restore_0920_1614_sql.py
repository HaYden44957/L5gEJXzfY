# 代码生成时间: 2025-09-20 16:14:29
import os
import shutil
from sanic import Sanic, response
from sanic.exceptions import ServerError, NotFound, abort
from sanic.request import Request
from sanic.response import text, json

# Define the application
app = Sanic('DataBackupRestore')

# Directory for backup files
BACKUP_DIR = 'backup'

# Check if backup directory exists, create it if not
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

# Route for backup
@app.route('/api/backup', methods=['GET'])
async def backup(request: Request):
    # Get the current working directory
    current_dir = os.getcwd()
    
    # Define the backup file path
    backup_file_path = os.path.join(BACKUP_DIR, 'backup_' + str(os.path.getctime(current_dir)) + '.zip')
    
    try:
        # Create a zip file of the current directory
        shutil.make_archive(backup_file_path, 'zip', current_dir)
        return json({'message': 'Backup successful', 'backup_file_path': backup_file_path})
    except Exception as e:
        # Handle any exceptions that occur during backup
        return json({'error': str(e)}), 500

# Route for restore
@app.route('/api/restore', methods=['POST'])
async def restore(request: Request):
    # Get the backup file path from the request body
    backup_file_path = request.json.get('backup_file_path')
    
    if not backup_file_path or not os.path.exists(backup_file_path):
        return json({'error': 'Backup file not found'}), 404
    
    try:
        # Extract the backup file to the current working directory
        shutil.unpack_archive(backup_file_path, os.getcwd())
        return json({'message': 'Restore successful'})
    except Exception as e:
        # Handle any exceptions that occur during restore
        return json({'error': str(e)}), 500

# Error handler for 404
@app.exception(NotFound)
async def handle_404(request, exception):
    return json({'error': 'Resource not found'}), 404

# Error handler for 500
@app.exception(ServerError)
async def handle_500(request, exception):
    return json({'error': str(exception)}), 500

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)