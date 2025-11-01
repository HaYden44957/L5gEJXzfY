# 代码生成时间: 2025-11-01 11:16:16
import psutil
from sanic import Sanic, response
from sanic.request import Request
from sanic.response import json


# 创建一个Sanic应用
app = Sanic('cpu_usage_analyzer')


# 定义一个路由，返回CPU使用率
@app.route('/cpu_usage', methods=['GET'])
async def cpu_usage(request: Request):
    """
    返回CPU使用率的API端点。
    :arg request: 请求对象
    :return: 包含CPU使用率的JSON响应
    """
    try:
        # 获取CPU使用率
        cpu_usage_percent = psutil.cpu_percent(interval=1)
        # 构建响应数据
        response_data = {'cpu_usage_percent': cpu_usage_percent}
        return response.json(response_data)
    except Exception as e:
        # 错误处理
        app.logger.error(f'Error fetching CPU usage: {e}')
        return response.json({'error': 'Failed to fetch CPU usage'}, status=500)


# 运行Sanic应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)