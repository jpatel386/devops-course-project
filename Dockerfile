FROM python:3.9 as base

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry install

EXPOSE 5000

COPY todo_app todo_app

ENV FLASK_APP=todo_app/app

ENV FLASK_ENV=development

ENV SECRET_KEY=secret-key

FROM base as development

ENTRYPOINT ["poetry", "run", "flask", "run", "--host=0.0.0.0"]

FROM base as production 

ENV FLASK_ENV=production

ENTRYPOINT ["poetry", "run", "gunicorn", "todo_app.app:create_app()"]

FROM base as test

RUN apt-get update -qqy && apt-get install -qqy wget gnupg unzip

# Install Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \ 
  && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
  && apt-get update -qqy \
  && apt-get -qqy install google-chrome-stable \
  && rm /etc/apt/sources.list.d/google-chrome.list \
  && rm -rf /var/lib/apt/lists/* /var/cache/apt/*

# Install Chrome driver that is compatible with the installed version of Chrome
RUN CHROME_MAJOR_VERSION=$(google-chrome --version | sed -E "s/.* ([0-9]+)(\.[0-9]+){3}.*/\1/") \
  && CHROME_DRIVER_VERSION=$(wget --no-verbose -O - "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_MAJOR_VERSION}") \
  && echo "Using chromedriver version: "$CHROME_DRIVER_VERSION \
  && wget --no-verbose -O /tmp/chromedriver_linux64.zip https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip \
  && unzip /tmp/chromedriver_linux64.zip -d /usr/bin \
  && rm /tmp/chromedriver_linux64.zip \
  && chmod 755 /usr/bin/chromedriver

#ENV GECKODRIVER_VER=v0.29.1

#Install Firefox - USING UBUNTU ON GITHUB - APK IS FOR ALPINE SO STICK WITH CHROME 
#RUN apk add --allow-untrusted firefox-esr curl

#Install geckodriver
#RUN curl -sSLO https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VER}/geckodriver-${GECKODRIVER_VER}-linux64.tar.gz \
#  && tar zxf geckodriver-*.tar.gz \
#  && mv geckodriver /usr/bin/ \
#  && rm geckodriver-*.tar.gz

ENTRYPOINT ["poetry" ,"run", "pytest"]
