FROM --platform=linux/arm64 python:3.11.5

WORKDIR /backend

RUN apt-get update && apt-get install -y ffmpeg

COPY requirements.txt .
RUN pip install -r requirements.txt -U

COPY ./main.py .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
