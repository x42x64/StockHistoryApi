from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import time
import logging
import argparse

import onvista

logging.basicConfig(level=logging.INFO)


def get_stock_api_handler(base_uri):

    class StockApi(BaseHTTPRequestHandler):

        def parse_path(self, path):
            path = path.lstrip(base_uri)
            elems = path.strip('/').split('/')
            if len(elems) > 2:
                raise ValueError("Unsupported URL format. Expected /isin or /isin/exchange")
            elif (len(elems) == 2):
                return (elems[0], elems[1])
            else:
                return (elems[0], None)

        def _set_headers(self):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

        def do_GET(self):
            try:
                isin, exchange = self.parse_path(self.path)
            except ValueError as err:
                self.send_response(400)
                response = {'status': "Err", 'data': str(err)}
                self.wfile.write(json.dumps(response).encode("utf-8"))
                return
            
            
            self._set_headers()
            try:
                history = onvista.get_history_by_isin(isin, exchange)
                response = {'status': "OK", 'data': history}
            except ValueError as err:
                self.send_response(400)
                response = {'status': "Err", 'data': str(err)}
            
            self.wfile.write(json.dumps(response).encode("utf-8"))

    return StockApi

if __name__ == "__main__":        

    parser = argparse.ArgumentParser(description='Providing an API to get historic stock data for given ISIN')
    parser.add_argument('--host_name', type=str, default='localhost', help='host where to serve')
    parser.add_argument('--port', type=int, default=8080, help='port where to serve')
    parser.add_argument('--base_uri', type=str, default='/', help='base uri')

    args = parser.parse_args()  

    webServer = HTTPServer((args.host_name, args.port), get_stock_api_handler(args.base_uri))
    logging.info(f"Server started http://{args.host_name}:{args.port}")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")