"""Serves the repo so the animation page can load the app icon, and saves the
recorded video into tools/install-video/out/ (only .mp4 and .png accepted).

    python3 tools/install-video/server.py 8650
    then open http://localhost:8650/tools/install-video/ and run record() in the console
"""
import http.server
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
OUT = os.path.join(HERE, 'out')
os.makedirs(OUT, exist_ok=True)


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=REPO, **kwargs)

    def do_POST(self):
        if not self.path.startswith('/save/'):
            self.send_error(404)
            return
        name = os.path.basename(self.path[len('/save/'):])
        if not name.endswith(('.mp4', '.png')):
            self.send_error(400)
            return
        length = int(self.headers.get('Content-Length', 0))
        with open(os.path.join(OUT, name), 'wb') as f:
            f.write(self.rfile.read(length))
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'ok')


port = int(sys.argv[1]) if len(sys.argv) > 1 else 8650
http.server.ThreadingHTTPServer(('127.0.0.1', port), Handler).serve_forever()
