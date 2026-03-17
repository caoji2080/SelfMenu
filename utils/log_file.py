
"""
日志工具 - 提供日志记录功能
"""
import logging
import os
from pathlib import Path
from datetime import datetime


class Logger:
    """日志工具类"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self):
        """初始化日志系统"""
        log_dir = Path(__file__).parent.parent / "logs"
        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / f"menu_app_{datetime.now().strftime('%Y%m%d')}.log"

        # 配置日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )

        self.logger = logging.getLogger('MenuApp')

    def info(self, message: str):
        """记录信息日志"""
        self.logger.info(message)

    def warning(self, message: str):
        """记录警告日志"""
        self.logger.warning(message)

    def error(self, message: str, exc_info=None):
        """记录错误日志"""
        self.logger.error(message, exc_info=exc_info)

    def debug(self, message: str):
        """记录调试日志"""
        self.logger.debug(message)

    def success(self, message: str):
        """记录成功日志"""
        self.logger.info(f"✅ SUCCESS: {message}")


# 快捷函数
def log_info(msg: str):
    Logger().info(msg)


def log_error(msg: str, exc_info=None):
    Logger().error(msg, exc_info=exc_info)


def log_success(msg: str):
    Logger().success(msg)
