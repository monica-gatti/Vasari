FROM alpine:latest
RUN apk add --no-cache python3-dev
RUN apk add py3-pip

WORKDIR /app

COPY . /app

RUN pip3 --no-cache-dir install -r requirements.txt

RUN apk --no-cache add curl

EXPOSE 5000

ENTRYPOINT python3 app.py