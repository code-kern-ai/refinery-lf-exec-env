FROM python:3.7

RUN apt update && apt install -y curl

COPY . .

RUN pip3 install -r requirements.txt

ENTRYPOINT ["/run.sh"]
