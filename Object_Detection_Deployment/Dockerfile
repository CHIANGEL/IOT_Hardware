FROM registry.cn-hangzhou.aliyuncs.com/se-wd/conda-arm64:v1.0
COPY / /model
WORKDIR /model
RUN conda config --append channels c4aarch64 && conda config --append channels conda-forge && conda config --append channels gaiar && conda install --yes --file requirements.txt
RUN chmod +x deploy.py && chmod +x models.py && chmod +x client_demo.py
EXPOSE 32442