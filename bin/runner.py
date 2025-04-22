import uvicorn

from docu_mentor.core import settings
from docu_mentor.types.enums import EnvironmentEnum


def run():
    # Set the app based on the environment
    if settings.environment == EnvironmentEnum.development:
        reload = True
        app_dir = "src"
        host = "127.0.0.1"
    else:
        reload = False
        app_dir = None
        host = "0.0.0.0"

    # Run the app with uvicorn
    uvicorn.run(
        app="docu_mentor.main:app",
        host=host,
        port=settings.port,
        reload=reload,
        app_dir=app_dir,
        proxy_headers=True,
    )


if __name__ == "__main__":
    run()
