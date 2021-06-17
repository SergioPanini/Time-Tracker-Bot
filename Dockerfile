FROM python:3.8

WORKDIR /home/bot

COPY . .

RUN pip install -r ./req.txt

CMD ["python", "server.py"]