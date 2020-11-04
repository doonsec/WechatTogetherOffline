FROM python:3.6


COPY ./src /app/src

WORKDIR /app/src

RUN pip install -r requirements.txt -i https://pypi.douban.com/simple
RUN pip install gunicorn==19.5.0 gevent==1.4.0 -i https://pypi.douban.com/simple

CMD ["gunicorn", "-k", "gevent", "-b", "0.0.0.0:8000", "app:app"]