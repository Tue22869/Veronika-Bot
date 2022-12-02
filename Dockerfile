FROM python:3.10

COPY . tgbot

EXPOSE 6969

RUN pip install -r tgbot/requirements.txt

CMD ["python", "tgbot/main.py"]