"""
Launcher for the Messier Log Book Flask web service.
Run this from the project root.
"""

import sys
import os
from pathlib import Path
    
# Add the project root to sys.path for imports
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

from services.logbook.flask_logbook_service import app

if __name__ == "__main__":
    print("CWD:", os.getcwd())
    print("Static exists:", os.path.exists("static/logo_main_2.png"))
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)