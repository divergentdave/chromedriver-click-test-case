FROM selenium/standalone-chrome-debug:3.141.59-vanadium

USER root

RUN apt-get -qqy remove google-chrome-stable
RUN apt-get -qqy update \
  && apt-get -qqy install python3-pip

USER seluser
RUN pip3 -q install selenium
USER root

RUN mkdir /opt/scripts /bisect
RUN chown seluser:seluser /bisect
RUN curl -s --basic -n "https://chromium.googlesource.com/chromium/src/+/master/tools/bisect-builds.py?format=TEXT" | base64 -d > /opt/scripts/bisect-builds.py
RUN chmod a+x /opt/scripts/bisect-builds.py
ADD scripts/ /opt/scripts/

USER seluser
WORKDIR /bisect

CMD bash
