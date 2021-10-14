FROM selenium/standalone-chrome-debug:3.141.59-vanadium

USER root

RUN apt-get -qqy remove google-chrome-stable
RUN apt-get -qqy update \
  && apt-get -qqy install python3-pip libgbm1

USER seluser
RUN pip3 -q install selenium
USER root

RUN rm /usr/bin/chromedriver
RUN bash -c 'for CHROMEDRIVER_VERSION in 78.0.3904.105 79.0.3945.36 80.0.3987.106 81.0.4044.138 83.0.4103.39 84.0.4147.30 85.0.4183.87 86.0.4240.22 87.0.4280.88 88.0.4324.96 89.0.4389.23 90.0.4430.24 91.0.4472.101 92.0.4515.107 93.0.4577.63 94.0.4606.61 95.0.4638.17 ;\
  do wget --no-verbose -O /tmp/chromedriver_linux64.zip https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip; \
  unzip /tmp/chromedriver_linux64.zip -d /opt/selenium; \
  rm /tmp/chromedriver_linux64.zip; \
  mv /opt/selenium/chromedriver /opt/selenium/chromedriver-$CHROMEDRIVER_VERSION; \
  chmod 755 /opt/selenium/chromedriver-$CHROMEDRIVER_VERSION;\
  done'

RUN mkdir /opt/scripts /bisect
RUN chown seluser:seluser /bisect
RUN curl -s --basic -n "https://chromium.googlesource.com/chromium/src/+/master/tools/bisect-builds.py?format=TEXT" | base64 -d > /opt/scripts/bisect-builds.py
RUN chmod a+x /opt/scripts/bisect-builds.py
ADD scripts/ /opt/scripts/

USER seluser
WORKDIR /bisect

CMD bash
