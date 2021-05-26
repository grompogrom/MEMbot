FROM python:3.6.12-stretch
WORKDIR /bots/MEMbot
COPY . .
RUN pip install -r requirements.txt
RUN touch Tlogs.txt Glogs.txt
CMD ["python", "./telebott/Tbot.py", ">>", "Tlogs.txt", "&", ";", "python", "./discordbot/Dbot.py", ">>", "Dlogs.txt", "&"]
