FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY dns_adblocker.py .

CMD ["python3", "dns_adblocker.py"]
