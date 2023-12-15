FROM python:3.11.7

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

ENTRYPOINT ["python3", "main.py"]
CMD ["--host=0.0.0.0", "--port=8000"]
