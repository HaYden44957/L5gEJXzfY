# 代码生成时间: 2025-09-23 00:40:53
from sanic import Sanic
from sanic.response import json, text
import re
import os
from datetime import datetime

# 定义日志解析工具
class LogParser:
    def __init__(self, log_file):
        self.log_file = log_file
        self.log_lines = []
        self.parse_log()

    def parse_log(self):
        """解析日志文件"""
        if not os.path.exists(self.log_file):
            raise FileNotFoundError(f"Log file {self.log_file} not found.")
        with open(self.log_file, 'r') as file:
            self.log_lines = file.readlines()

    def get_error_logs(self):
        """获取错误日志信息"""
        error_logs = [line for line in self.log_lines if 'ERROR' in line]
        return error_logs

    def get_info_logs(self):
        """获取信息日志信息"""
        info_logs = [line for line in self.log_lines if 'INFO' in line]
        return info_logs

    def get_logs_by_date(self, date):
        """根据日期获取日志信息"""
        try:
            dt = datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD.")
        logs = [line for line in self.log_lines if dt.strftime('%Y-%m-%d') in line]
        return logs

# 创建Sanic应用
app = Sanic('LogParserApp')

# 定义路由处理函数
@app.route('/logs/error', methods=['GET'])
async def get_error_logs(request):
    log_parser = LogParser('path/to/your/logfile.log')
    error_logs = log_parser.get_error_logs()
    return json({'error_logs': error_logs})

@app.route('/logs/info', methods=['GET'])
async def get_info_logs(request):
    log_parser = LogParser('path/to/your/logfile.log')
    info_logs = log_parser.get_info_logs()
    return json({'info_logs': info_logs})

@app.route('/logs/date/<date>', methods=['GET'])
async def get_logs_by_date(request, date):
    log_parser = LogParser('path/to/your/logfile.log')
    try:
        logs = log_parser.get_logs_by_date(date)
    except ValueError as e:
        return text(str(e), status=400)
    return json({'logs': logs})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)