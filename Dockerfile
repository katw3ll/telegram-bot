FROM python:3

WORKDIR /telegram-bot

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /telegram-bot/app

CMD [ "python", "./app/app.py" ]
