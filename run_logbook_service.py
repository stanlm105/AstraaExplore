"""
Launcher for the Messier Log Book Flask web service.

Run this script from the project root to start the Flask app.
"""

import sys
import os
from pathlib import Path

# Add the project root to sys.path for module imports
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

from services.logbook.flask_logbook_service import app

if __name__ == "__main__":
    # Get port from environment variable or default to 8080
    port = int(os.environ.get("PORT", 8080))
    # Run the Flask app on all interfaces
    app.run(host="0.0.0.0", port=port)