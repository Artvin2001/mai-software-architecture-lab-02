from argparse import ArgumentParser

import uvicorn
from fastapi import FastAPI

app = FastAPI(
    title='Conference Service',
    description='Сервис конференций',
    docs_url='/',
)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("--host", type=str, dest="host", default="127.0.0.1")
    parser.add_argument("--port", type=int, dest="port", default=8000)
    arguments = parser.parse_args()

    uvicorn.run(app, host=arguments.host, port=arguments.port)
