# 代码生成时间: 2025-09-21 22:14:09
import psutil
from sanic import Sanic, response
from sanic.request import Request
from sanic.response import json

# 创建一个Sanic应用实例
app = Sanic('MemoryUsageAnalyzer')

# 定义一个端点来获取内存使用情况
@app.route('/memory', methods=['GET'])
async def memory_usage(request: Request):
    try:
        # 获取内存使用信息
        mem = psutil.virtual_memory()
        # 构建返回的内存使用数据
        memory_data = {
            'total': mem.total,
            'available': mem.available,
            'used': mem.used,
            'free': mem.free,
            'percent': mem.percent
        }
        return response.json(memory_data)
    except Exception as e:
        # 错误处理
        return response.json({'error': str(e)})

# 运行Sanic应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
