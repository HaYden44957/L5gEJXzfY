# 代码生成时间: 2025-09-19 15:48:30
import asyncio
from sanic import Sanic, response
from sanic.exceptions import ServerError
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.asyncio import AsyncIOExecutor

# 初始化Sanic应用
app = Sanic("ScheduledTaskApp")

# 创建一个调度器
scheduler = AsyncIOScheduler(jobstores={'default': MemoryJobStore()},
                              executors={'default': AsyncIOExecutor()},
                              listener=app)

# 定时任务示例
def scheduled_task():
    """定时任务函数，打印一条消息到控制台"""
    print("Scheduled task executed")

# 定时任务配置，每天上午9点执行
scheduler.add_job(scheduled_task, CronTrigger(hour=9, minute=0), id='my_scheduled_task')

# 启动调度器
@app.listener('after_server_start')
async def schedule_tasks(app, loop):
    """启动定时任务调度器"""
    try:
        scheduler.start()
    except Exception as e:
        raise ServerError(f"Failed to start scheduler: {e}")

# 添加路由，用于测试和查看任务状态
@app.route('/status/', methods=['GET'])
async def status(request):
    """返回任务状态"""
    job = scheduler.get_job('my_scheduled_task')
    if job:
        return response.json({'status': 'scheduled', 'next_run_time': job.next_run_time})
    else:
        return response.json({'status': 'not scheduled'})

# 错误处理事件监听器
def error_listener(event):
    """错误处理事件监听器"""
    if event.exception:
        print(f"Job {event.job_id} raised an exception: {event.exception}")

# 绑定错误事件到监听器
scheduler.add_listener(error_listener, EVENT_JOB_ERROR)

# 任务执行完毕后的事件监听器
def executed_listener(event):
    """任务执行完毕后的事件监听器"""
    print(f"Job {event.job_id} executed successfully")

# 绑定任务执行完毕后的事件到监听器
scheduler.add_listener(executed_listener, EVENT_JOB_EXECUTED)

# 运行Sanic应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
