import os
import sys
from pathlib import Path

# Get the absolute path of the project root directory
project_root = Path(__file__).parent.absolute()
src_path = os.path.join(project_root, "src")
sys.path.insert(0, str(src_path))