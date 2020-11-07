FROM continuumio/anaconda3:4.4.0
LABEL name="Tajudeen Abdulazeez" 
LABEL email="tabdulazeez99@gmail.com"
LABEL version="1.0"
EXPOSE 5000
RUN apt-get update && apt-get install -y apache2 \
    apache2-dev \   
    vim \
 && apt-get clean \
 && apt-get autoremove \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /var/www/app/
COPY ./index.wsgi /var/www/app/index.wsgi
COPY ./app /var/www/app/
RUN pip install -r requirements.txt 
RUN apt-get update && apt-get -y install locales

RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8     

RUN /opt/conda/bin/mod_wsgi-express install-module
RUN mod_wsgi-express setup-server index.wsgi --port=5000 \
    --user www-data --group www-data \
    --server-root=/etc/mod_wsgi-express

CMD /etc/mod_wsgi-express/apachectl start -D FOREGROUND