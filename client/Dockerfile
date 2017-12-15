FROM python:2.7-alpine3.6

RUN apk add bash curl --update
RUN pip install requests BeautifulSoup

WORKDIR /client

COPY . ./
