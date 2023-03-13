FROM python:3.10
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
#ENV HOME=/app
#RUN chown -R root:root $HOME
#RUN chmod a+x $HOME/entrypoint.sh
RUN apt-get install -y netcat
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt



ENTRYPOINT ["/app/entrypoint.sh"]
