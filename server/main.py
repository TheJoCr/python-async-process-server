from .asgi import make_app
from .routes import routes
import uvicorn

def main():
    app = make_app( routes )
    uvicorn.run(app, port=8080)
