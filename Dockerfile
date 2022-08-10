FROM python:3-alpine

LABEL maintainer="BIBA - Bremer Institut für Produktion und Logistik GmbH"

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

EXPOSE 8080

CMD [ "python", "app.py" ]