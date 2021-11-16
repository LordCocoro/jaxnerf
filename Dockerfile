FROM tensorflow/tensorflow:2.6.0

ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"

RUN apt-get update -y

RUN apt-get install -y wget git python python-dev && rm -rf /var/lib/apt/lists/*

RUN apt-get install bzip2

RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda3-py39_4.10.3-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-py39_4.10.3-Linux-x86_64.sh -b \
    && rm -f Miniconda3-py39_4.10.3-Linux-x86_64.sh 

RUN conda --version

RUN pip install skia-python

RUN git clone https://github.com/LordCocoro/jaxnerf.git

RUN conda create --name jaxnerf python=3.7

RUN echo "source activate jaxnerf" > ~/.bashrc

ENV PATH /opt/conda/envs/env/bin:$PATH

RUN conda install pip; pip install --upgrade pip setuptools wheel

RUN pip install -r jaxnerf/requirements.txt

RUN pip install "jax[tpu]>=0.2.16" -f https://storage.googleapis.com/jax-releases/libtpu_releases.html

ENV MODELS_BUCKET='gs://nerf-bucket/models'

ENV CHECKPOINT_BUCKET='gs://nerf-bucket/chekpoint'

RUN cd jaxnerf

WORKDIR /jaxnerf

RUN git pull

RUN cd ..

WORKDIR /

EXPOSE 3000


CMD [ "python","-m", "jaxnerf.app" ]