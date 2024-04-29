FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt


# If additional arguments are passed with docker run, it will be used as a CLI app
# Otherwise, it will run a Flask app
ENTRYPOINT ["python", "app.py"]