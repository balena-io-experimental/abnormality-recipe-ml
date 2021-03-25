FROM python:3.8-alpine

WORKDIR /usr/src/app

RUN apk add --update alpine-sdk
RUN pip install poetry

EXPOSE 7860

COPY . ./
RUN poetry install

CMD ["poetry", "run", "start"]
