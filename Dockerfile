FROM tiangolo/uvicorn-gunicorn:python3.7-alpine3.8
RUN apk --no-cache add gcc libc-dev inotify-tools
COPY . /app
RUN pip install -r server/requirements.txt
ENV MODULE_NAME server.server