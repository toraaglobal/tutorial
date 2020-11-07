FROM continuumio/anaconda3:4.4.0
LABEL name="Tajudeen Abdulazeez" email="tabdulazeez99@gmail.com" version="1.0"
EXPOSE 5000

WORKDIR /web/
COPY ./web /web/
RUN pip install --upgrade pip \
    && pip uninstall -y numpy \
    && pip install -r requirements.txt \
    && pip uninstall tensorflow_estimator \
    && pip install -Iv tensorflow_estimator==1.13.0 \
    && conda install tensorflow \
    && conda install -c conda-forge keras

RUN python train_model.py
   
CMD ["python", "index.py"]