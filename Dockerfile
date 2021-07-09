FROM python:3.8

WORKDIR /home/bot   

COPY ./req.txt .

RUN pip install -r ./req.txt

COPY ./source ./source

CMD ["python", "source/server.py"]