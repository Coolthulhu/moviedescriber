FROM python:3.8

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
	libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR thesite
COPY requirements.txt ./

RUN pip install -r requirements.txt
COPY thesite .

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
