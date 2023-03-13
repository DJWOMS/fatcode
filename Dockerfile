FROM python:3.10
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
#ENV HOME=/app
#RUN chown -R root:root $HOME
#RUN chmod a+x $HOME/entrypoint.sh

COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]

COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

