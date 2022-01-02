FROM python:3.8-alpine

ENV DIR=/DiscordBot

WORKDIR ${DIR}

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "src/main.py" ]