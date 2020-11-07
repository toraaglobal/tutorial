FROM continuumio/anaconda3:4.4.0
LABEL name="Tajudeen Abdulazeez" email="tabdulazeez99@gmail.com" version="1.0"
EXPOSE 5000

WORKDIR /web/
COPY ./web /web/
RUN pip install -r requirements.txt 
   
CMD ["python", "index.py"]