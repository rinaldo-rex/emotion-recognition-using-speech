FROM python:3.6

WORKDIR /app

COPY Pip* /app/

RUN pip install --upgrade pip && \
    pip install pipenv && \
    pipenv install --deploy --system

COPY . /app/

EXPOSE 5678

# Production gunicorn instantiation
#CMD ["gunicorn", \
#        "-w 4", \
#        "-b 0.0.0.0:5014", \
#        "wsgi:app", \
#        "--reload", \
#        "--error-logfile=logs/yekaliva_response.log", \
#        "--log-level=debug"]

# Use the following command to test it on Flask Server for dev purposes
CMD ["python", "app_server.py"]
