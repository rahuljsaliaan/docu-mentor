import subprocess
import os
from docu_mentor.core import settings
from docu_mentor.types.enums import EnvironmentEnum

def run():
    # Set the app based on the environment
    if settings.config.environment == EnvironmentEnum.development:
        reload = True
        app_dir = "src"
        host = "127.0.0.1"
    else:
        reload = False
        app_dir = None
        host = "0.0.0.0"

    # Command to run Streamlit from a Python script
    command = [
        "streamlit", 
        "run", 
        os.path.abspath("src/docu_mentor/main.py"),  # Path to your Streamlit script
        "--server.port", str(settings.config.port),
        "--server.address", host
    ]
    
    # If development mode, enable reloading
    if reload:
        command.append("--server.enableCORS=false")  # This can help with certain CORS issues in development
    
    # Run the Streamlit app
    subprocess.run(command)

if __name__ == "__main__":
    run()
