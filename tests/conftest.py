import sys
from pathlib import Path

# 添加项目根目录到Python路径，确保可以导入app模块
sys.path.insert(0, str(Path(__file__).parent.parent))
