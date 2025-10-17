# 代码生成时间: 2025-10-18 00:24:42
import asyncio
from sanic import Sanic
from sanic.response import json

# 创建一个Sanic应用实例
app = Sanic("UIComponentLibrary")

# 用户界面组件字典，可以扩展更多的组件
UI_COMPONENTS = {
    "button": "<button>Click me!</button>",  # HTML按钮组件
    "input": "<input type='text' placeholder='Enter text'>",  # HTML输入框组件
    "checkbox": "<input type='checkbox'>Check me!",  # HTML复选框组件
    # 更多组件可以在这里添加
}

# 获取所有UI组件的路由
@app.route("/components", methods=["GET"])
async def get_components(request):
    # 响应所有UI组件
    return json(UI_COMPONENTS)

# 获取单个UI组件的路由
@app.route("/components/<component_name>", methods=["GET"])
async def get_component(request, component_name):
    # 检查请求的组件是否存在
    if component_name in UI_COMPONENTS:
        return json({component_name: UI_COMPONENTS[component_name]})
    else:
        # 如果组件不存在，返回404错误
        return json({"error": "Component not found"}, status=404)

# 错误处理
@app.exception(404)
async def not_found_exception_handler(request, exception):
    return json({"error": "Component not found"}, status=404)

# 运行Sanic应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
