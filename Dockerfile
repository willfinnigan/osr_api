FROM continuumio/miniconda3:23.5.2-0

COPY ./env.yml env.yml

RUN conda env create -n osr_api -f env.yml
SHELL ["conda", "run", "-n", "osr_api", "/bin/bash", "-c"]

RUN pip install git+https://github.com/Kohulan/DECIMER-Image_Transformer.git

EXPOSE 8080

COPY ./main.py main.py

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]