FROM python:3.7-alpine
WORKDIR /app
RUN chown -R nobody /app
RUN apk add --no-cache gcc libc-dev
COPY . .
RUN pip install -r server/requirements.txt
CMD ["./server/server.py"]