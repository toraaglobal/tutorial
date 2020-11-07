FROM continuumio/anaconda3:4.4.0
LABEL name="Tajudeen Abdulazeez" email="tabdulazeez99@gmail.com" version="1.0"
EXPOSE 5000

WORKDIR /web/
COPY ./web /web/

RUN pip install -r requirements.txt 
RUN pip install -Iv tensorflow_estimator==1.13.0
RUN conda install -c conda-forge keras

RUN python train_model.py
   
CMD ["python", "index.py"]