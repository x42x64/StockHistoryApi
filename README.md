# Stock history collector API

A small webserver which collects historic stock data from OnVista. May break anytime, as no official API is used.

Originally intended to use with Portfolio performance. Settings:
```
URL:                http://<hostname>:<port>/<isin>/<exchange> (/<exchange> is optional)
path to timestamp:  $.data[*].datetimeLast.UTCTimeStamp
path to stockprice: $.data[*].last
```

## Build and run a dockerimage locally

Build the image:
```
git clone https://github.com/x42x64/StockHistoryApi.git
cd StockHistoryApi
docker build -t <image_name> .
```

Run the image:
```
docker run -d <image_name>
```

Custom port, interface and/or sub uri:
```
docker run <image_name> --help

usage: server.py [-h] [--host_name HOST_NAME] [--port PORT]
                 [--base_uri BASE_URI]

Providing an API to get historic stock data for given ISIN

optional arguments:
  -h, --help            show this help message and exit
  --host_name HOST_NAME
                        host where to serve
  --port PORT           port where to serve
  --base_uri BASE_URI   base uri
```
