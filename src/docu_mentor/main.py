from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/")
def read_root():
    return JSONResponse(
        status_code=status.HTTP_200_OK, content="Welcome to DocuMentor!"
    )


if __name__ == "__main__":
    app()
