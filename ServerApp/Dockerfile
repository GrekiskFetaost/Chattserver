FROM python:3.10-slim
WORKDIR /app
COPY . /app
COPY requirements.txt .
RUN pip install -r requirements.txt
EXPOSE 55555
CMD ["python", "server.py"]