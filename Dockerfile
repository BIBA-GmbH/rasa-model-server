FROM python:3-alpine

LABEL maintainer="Victor Rachieru"

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

EXPOSE 8080

CMD [ "python", "app.py" ]