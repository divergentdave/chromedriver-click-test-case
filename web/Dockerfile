FROM python:3.8

RUN pip install selenium==3.141.0 urllib3==1.25.7

COPY capture.har server.py test.py ./

CMD python -u server.py
