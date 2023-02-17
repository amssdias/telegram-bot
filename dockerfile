FROM python:3.9-slim-buster

# Install Redis
RUN apt-get update && apt-get install -y redis-server

COPY . app/

# Set working directory
WORKDIR /app

RUN pip install -r requirements.txt

# Expose the Redis port
EXPOSE 6379

# Run Redis and the application
CMD [ "sh", "-c", "redis-server & python main.py" ]
