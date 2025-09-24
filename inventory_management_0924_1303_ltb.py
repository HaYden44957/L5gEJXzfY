# 代码生成时间: 2025-09-24 13:03:57
import json
from sanic import Sanic, response
from sanic.exceptions import ServerError, abort
from sanic.request import Request
from sanic.response import HTTPResponse

# Inventory management system
app = Sanic('Inventory Management System')

# Dummy inventory data
inventory = {
    "items": [
        {
            "id": 1,
            "name": "Laptop",
            "quantity": 10
        },
        {
            "id": 2,
            "name": "Smartphone",
            "quantity": 20
        }
    ]
}

# Helper function to get item by id
def get_item_by_id(item_id):
    for item in inventory['items']:
        if item['id'] == item_id:
            return item
    return None

# Endpoint to get all items
@app.route('/api/items', methods=['GET'])
async def get_all_items(request: Request):
    return response.json(inventory['items'])

# Endpoint to get an item by id
@app.route('/api/items/<item_id:int>', methods=['GET'])
async def get_item(request: Request, item_id: int):
    item = get_item_by_id(item_id)
    if item is None:
        abort(404, 'Item not found')
    return response.json(item)

# Endpoint to create a new item
@app.route('/api/items', methods=['POST'])
async def create_item(request: Request):
    try:
        data = request.json
        if not all(key in data for key in ['name', 'quantity']):
            abort(400, 'Missing name or quantity')
        item = {
            "id": len(inventory['items']) + 1,
            "name": data['name'],
            "quantity": data['quantity']
        }
        inventory['items'].append(item)
        return response.json(item, status=201)
    except Exception as e:
        raise ServerError('Failed to create item', e)

# Endpoint to update an item by id
@app.route('/api/items/<item_id:int>', methods=['PUT'])
async def update_item(request: Request, item_id: int):
    try:
        data = request.json
        item = get_item_by_id(item_id)
        if item is None:
            abort(404, 'Item not found')
        item['name'] = data.get('name', item['name'])
        item['quantity'] = data.get('quantity', item['quantity'])
        return response.json(item)
    except Exception as e:
        raise ServerError('Failed to update item', e)

# Endpoint to delete an item by id
@app.route('/api/items/<item_id:int>', methods=['DELETE'])
async def delete_item(request: Request, item_id: int):
    try:
        item = get_item_by_id(item_id)
        if item is None:
            abort(404, 'Item not found')
        inventory['items'].remove(item)
        return response.json({'message': 'Item deleted successfully'})
    except Exception as e:
        raise ServerError('Failed to delete item', e)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)