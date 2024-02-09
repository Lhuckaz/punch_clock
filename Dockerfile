FROM python:3.9-slim

ENV URL=http://site.com
ENV USER=user
ENV PASSWORD=pass
ENV DESCRIPTION=example

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY punch_clock.py .

CMD ["python", "./punch_clock.py"]
