FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

# this is for ollama
EXPOSE 11434

CMD ["python", "main.py"]
