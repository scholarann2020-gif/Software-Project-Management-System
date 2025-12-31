from pathlib import Path
import sys
# Ensure project root (folder that contains `app`) is on sys.path for test imports
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
