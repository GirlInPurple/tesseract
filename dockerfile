FROM ubuntu:lastest

RUN apt update
RUN apt install python3.11 -y
RUN python3.11 -m pip install py-cord

WORKDIR /usr/tesseract/src

COPY tesseractV2.py ./

CMD ["python3.11", "./tesseractV2.py"]