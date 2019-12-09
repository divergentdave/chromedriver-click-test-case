FROM selenium/standalone-chrome-debug:3.141.59-vanadium

USER root

RUN apt-get -qqy remove google-chrome-stable
RUN apt-get -qqy update \
  && apt-get -qqy install python3-pip

USER seluser
RUN pip3 -q install selenium
USER root

RUN rm /usr/bin/chromedriver
RUN wget --no-verbose -O /tmp/chromedriver_linux64.zip https://chromedriver.storage.googleapis.com/78.0.3904.105/chromedriver_linux64.zip \
  && unzip /tmp/chromedriver_linux64.zip -d /opt/selenium \
  && rm /tmp/chromedriver_linux64.zip \
  && mv /opt/selenium/chromedriver /opt/selenium/chromedriver-78.0.3904.105 \
  && chmod 755 /opt/selenium/chromedriver-78.0.3904.105
RUN wget --no-verbose -O /tmp/chromedriver_linux64.zip https://chromedriver.storage.googleapis.com/79.0.3945.36/chromedriver_linux64.zip \
  && unzip /tmp/chromedriver_linux64.zip -d /opt/selenium \
  && rm /tmp/chromedriver_linux64.zip \
  && mv /opt/selenium/chromedriver /opt/selenium/chromedriver-79.0.3945.36 \
  && chmod 755 /opt/selenium/chromedriver-79.0.3945.36

RUN mkdir /opt/scripts /bisect
RUN chown seluser:seluser /bisect
RUN curl -s --basic -n "https://chromium.googlesource.com/chromium/src/+/master/tools/bisect-builds.py?format=TEXT" | base64 -d > /opt/scripts/bisect-builds.py
RUN chmod a+x /opt/scripts/bisect-builds.py
ADD scripts/ /opt/scripts/

USER seluser
WORKDIR /bisect

CMD bash
