# First Stage
FROM python:3.10-slim-buster AS compile-image
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential gcc

# virtual environment:
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# creating virtual environment
COPY ./requirements.txt ./requirements.txt
RUN python -m pip install --upgrade pip \
    && pip3 install --no-cache-dir -r requirements.txt \
    && rm requirements.txt

# Second Stage
FROM python:3.10-slim-buster AS build-image
COPY --from=compile-image /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app

COPY . .

RUN useradd -u 1500 -m appuser \ 
    && chown -R appuser:appuser . \
    && chmod +w .

USER 1500

CMD ["/bin/bash", "-c", "cd app; streamlit run Web_crawler.py "]

EXPOSE 8501
