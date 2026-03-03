FROM python:latest

WORKDIR /app

COPY . /app

RUN pip install -r req.txt

EXPOSE 9999

CMD [ "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "9999" ]