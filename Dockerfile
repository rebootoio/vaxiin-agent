FROM python:3

COPY requirements.txt /requirements.txt

RUN pip3 install -r requirements.txt

COPY app/ /app

ENTRYPOINT [ "python3" ]

CMD [ "/app/vaxiin-agent.py" ]
