# 代码生成时间: 2025-09-23 18:56:36
import psutil
from sanic import Sanic
from sanic.response import json

# 创建Sanic应用实例
app = Sanic("MemoryUsageAnalyzer")

# 定义一个路由来获取内存使用情况
@app.route("/memory", methods=["GET"])
async def get_memory_usage(request):
    """
    获取当前系统的内存使用情况
    :return: JSON格式的内存使用数据
    """
    try:
        # 获取内存使用情况
        memory_status = psutil.virtual_memory()
        # 构造返回的数据
        result = {
            "total": memory_status.total,
            "available": memory_status.available,
            "used": memory_status.used,
            "free": memory_status.free,
            "percent": memory_status.percent
        }
        return json(result)
    except Exception as e:
        # 错误处理
        return json({"error": str(e)})

# 运行Sanic应用
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)