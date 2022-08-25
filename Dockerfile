FROM lyralemos/python-gdal:py3.8-gdal3.0.4

WORKDIR /app
COPY . .

RUN apt-get update && apt-get install -y --no-install-recommends git libgraphviz-dev wait-for-it gettext g++ && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir -r requirements.txt
