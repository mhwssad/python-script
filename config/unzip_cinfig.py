from pathlib import Path

from pathlib import Path

# 获取项目根目录的路径
project_root = Path(__file__).parent.parent.parent

# 定义日志文件的相对路径
log_file = project_root / "log/unzip.log"
path_test = Path(r"..\..\log\unzip.7z").resolve()
# 确保日志目录存在
log_dir = log_file.parent
if not log_dir.exists():
    log_dir.mkdir(parents=True, exist_ok=True)
