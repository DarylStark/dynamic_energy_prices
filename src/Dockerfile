FROM python:3.10.6-slim
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .

RUN mkdir /data

ENV FLASK_APP energy_prices:flask_app
ENV FLASK_ENV development
ENV FLASK_RUN_PORT 5000

ENV ENVIRONMENT production
ENV CONFIG_FILE /app/config.yaml
ENV DATA_FOLDER /data

CMD [ "python3", "-m", "flask", "run"]