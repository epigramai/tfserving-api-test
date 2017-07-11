FROM python:3.5

WORKDIR /app

# Install libraries
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copying project files, remember to exclude large files.
# Each COPY line is a layer that will be cached by docker.
COPY /predict_client ./predict_client
COPY /util ./util
COPY main.py .

# Make 5000 available to the world outside this container
EXPOSE 5000

ENTRYPOINT ["gunicorn"]
CMD ["-b", "0.0.0.0:5000", "-k", "gevent", "main:app"]
