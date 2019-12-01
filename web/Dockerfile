FROM python:3.8

RUN pip install selenium==3.141.0

COPY capture.har server.py test.py ./

CMD python -u server.py
