FROM continuumio/miniconda3:4.10.3-alpine

WORKDIR /opt/pku-embl

# Need the following line in mainland China
COPY ./docker/tsinghua.condarc /root/.condarc

COPY ./docker/conda_env.yml /opt/pku-embl/conda_env.yml

RUN conda env create -f conda_env.yml && conda clean -afy
RUN rm -f conda_env.yml

RUN conda run --no-capture-output --name pku-embl pip install --no-cache-dir python-dateutil==2.8.2 openpyxl PyYAML==5.4.1 pandas==1.5.3 pytz==2022.05 retry -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY ./src .

COPY ./docker/config /etc/pku-embl

ENV NUM_PROCESS=2
ENV NUM_THREAD=2
ENV TIME_OUT=1800


CMD conda run --no-capture-output --name pku-embl uwsgi \
    --http 0.0.0.0:8088 \
    --uid root \
    --enable-threads \
    --lazy \
    --processes $NUM_PROCESS\
    --threads $NUM_THREAD \
    --logto /var/log/pku-ece-cv.log \
    --protocol uwsgi \
    --http-timeout $TIME_OUT \
    --harakiri $TIME_OUT \
    --wsgi app:app