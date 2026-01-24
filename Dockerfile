FROM python:3.9-buster
RUN apt-get update
RUN apt-get install -y wget xvfb python3 vim

RUN mkdir /root/browsers
#RUN wget https://chromedriver.storage.googleapis.com/89.0.4389.23/chromedriver_linux64.zip
WORKDIR /root/browsers
RUN curl https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o /chrome.deb
RUN dpkg -i /chrome.deb || apt-get install -yf

#RUN rm /chrome.deb
# Install chromedriver for Selenium

WORKDIR /root/browsers
RUN cd /root/browsers
RUN curl https://chromedriver.storage.googleapis.com/89.0.4389.23/chromedriver_linux64.zip -o chromedriver_linux64.zip
RUN ls
RUN unzip chromedriver_linux64.zip
RUN mv chromedriver /usr/local/bin/chromedriver

#RUN chmod +x /usr/local/bin/chromedriver

#docker run  -it -v "/Users/admas/Google Drive/PROJECTS/SuperSQA/Courses/MegaCourses/SeleniumPython/course-code/course-code-py-selenium-working/course-selenium-and-python/ssqatest":/root/ssqa ssqafe /bin/bash

RUN export BROWSER=headlesschrome
COPY . /root/ssqa
#RUN python /root/ssqa/setup.py install

