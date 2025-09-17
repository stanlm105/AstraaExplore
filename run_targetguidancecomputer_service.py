"""
Launcher for the Messier Target Guidance Computer Flask web service.
Run this from the project root.
"""
import sys
import os
from pathlib import Path
    
# Add the project root to sys.path for imports
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

from services.target_guidance_computer.flask_target_guidance_service import app

app.config["PROJECT_ROOT"] = str(project_root)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)