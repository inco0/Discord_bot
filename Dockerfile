FROM python:latest

ENV DIR=/DiscordBot

WORKDIR ${DIR}

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "src/main.py" ]