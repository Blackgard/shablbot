FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY setup.py pyproject.toml README.md /app/
COPY shablbot /app/shablbot/
COPY deploy/hodor /app/deploy/hodor/

RUN pip install --no-cache-dir -e /app

WORKDIR /app/deploy/hodor

ENV PYTHONUNBUFFERED=1
EXPOSE 3010

CMD ["python", "run.py"]
