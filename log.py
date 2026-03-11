import logging
from pathlib import Path
from datetime import datetime

# 获取项目根目录（python_code 的上一级）
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# logs 目录
LOG_DIR = PROJECT_ROOT / "log"
LOG_DIR.mkdir(exist_ok=True)

# 日志文件：2025_02_13.log
log_name = datetime.now().strftime("%Y_%m_%d") + ".log"
LOG_FILE = LOG_DIR / log_name

# 配置 logging（只在导入本模块时初始化一次）
logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s [%(levelname)s] %(message)s",
    filename=str(LOG_FILE),
    encoding="utf-8"
)

# 对外暴露 logger
logger = logging.getLogger("AnimeHelper")
