# Use the official Python image as the parent image
FROM python:3.9-slim


RUN apt update && \
    apt install -y curl gpg && \
    curl https://repo.anaconda.com/pkgs/misc/gpgkeys/anaconda.asc | \
    gpg --dearmor > /etc/apt/trusted.gpg.d/anaconda.gpg && \
    echo 'deb https://repo.anaconda.com/pkgs/misc/debrepo/conda stable main' > /etc/apt/sources.list.d/conda.list && \
    apt update && \
    apt install -y conda graphviz && \
    touch ~/.bashrc && \
    /opt/conda/bin/conda init bash

RUN . ~/.bashrc && \
    conda install -y -n base -c conda-forge mamba  && \
    mamba create -y --name research python=3.10.6  && \
    mamba install -y -n research -c conda-forge -c bioconda snakemake conda-build gcc git && \
    mamba clean -ya

COPY pyproject.toml poetry.lock ./
RUN . /opt/conda/etc/profile.d/conda.sh &&\
    conda activate research &&\
    pip install poetry==1.2.2 && \
    poetry config virtualenvs.in-project false && \
    poetry config virtualenvs.path /opt/conda/envs && \
    poetry install --no-root --no-interaction --no-ansi


# Set the working directory to /app
WORKDIR /app

# Copy the project files into the container
COPY . /app/

# Install LaTeX packages
RUN apt-get update \
  && apt-get install -y texlive-latex-base texlive-latex-extra texlive-fonts-recommended

# Generate the .tex file
RUN . ~/.bashrc && \
    conda activate research && \
    conda install -y -n base -c conda-forge mamba  && \
    mamba install -c conda-forge pygraphviz && \
    python sp_hw2/hw2.py


# Compile the .tex file into a PDF
RUN pdflatex -output-directory=sp_hw2/artifacts sp_hw2/artifacts/result_tex_file.tex

# Expose port 8000
EXPOSE 8000

# Start the server to serve the generated PDF file
CMD ["python", "-m", "http.server", "8000"]

