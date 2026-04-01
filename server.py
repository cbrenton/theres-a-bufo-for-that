#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# ///
import argparse
import json
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BUFOS_DIR = os.path.join(SCRIPT_DIR, "bufos")


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.serve_file("index.html", "text/html")
        elif self.path == "/api/list":
            self.serve_list()
        elif self.path.startswith("/bufos/"):
            filename = self.path[len("/bufos/"):]
            filepath = os.path.join(BUFOS_DIR, filename)
            if os.path.isfile(filepath):
                ext = filename.rsplit(".", 1)[-1].lower()
                content_types = {
                    "png": "image/png",
                    "jpg": "image/jpeg",
                    "jpeg": "image/jpeg",
                    "gif": "image/gif",
                    "webp": "image/webp",
                }
                ct = content_types.get(ext, "application/octet-stream")
                with open(filepath, "rb") as f:
                    data = f.read()
                self.send_response(200)
                self.send_header("Content-Type", ct)
                self.send_header("Content-Length", len(data))
                self.end_headers()
                self.wfile.write(data)
            else:
                self.send_error(404)
        else:
            self.send_error(404)

    def serve_file(self, filename, content_type):
        filepath = os.path.join(os.path.dirname(__file__), filename)
        with open(filepath, "rb") as f:
            data = f.read()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", len(data))
        self.end_headers()
        self.wfile.write(data)

    def serve_list(self):
        files = sorted(
            f for f in os.listdir(BUFOS_DIR)
            if os.path.isfile(os.path.join(BUFOS_DIR, f))
            and not f.startswith(".")
        )
        data = json.dumps(files).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(data))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, format, *args):
        pass  # silence request logs


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bufo browser")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    port = args.port
    server = HTTPServer(("", port), Handler)
    print(f"http://localhost:{port}")
    server.serve_forever()
