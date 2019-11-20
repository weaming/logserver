FROM tiangolo/uvicorn-gunicorn:python3.7
COPY . /app

RUN pip install -r server/requirements.txt
ENV MODULE_NAME server.server