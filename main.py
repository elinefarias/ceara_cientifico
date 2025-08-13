from fastapi import FastAPI
from server.gunicorn_server import GunicornServer
from controller import news

app = FastAPI(
    title="News Web Crawler",
    version="0.1",
    description="API to get news from web."
)

app.include_router(news.router)

if __name__ == '__main__':
    options = {
        'bind': '{}:{}'.format('0.0.0.0', '8080'),
        'workers': 1,
        'worker_class': 'uvicorn.workers.UvicornWorker',
        'timeout': 600
    }

    GunicornServer(app, options).run()
