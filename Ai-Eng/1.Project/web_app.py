"""Serve the chat frontend using ChatService from app.py."""

import asyncio
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from app import ChatService

WEB_DIR = Path(__file__).with_name("web")


class ChatHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if urlparse(self.path).path not in ("/", "/index.html"):
            self.send_error(404)
            return
        page = (WEB_DIR / "index.html").read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(page)))
        self.end_headers()
        self.wfile.write(page)

    def do_POST(self):
        if urlparse(self.path).path != "/chat":
            self.send_error(404)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length > 100_000:
                self.send_error(413, "Message is too long")
                return
            payload = json.loads(self.rfile.read(length))
            question = payload.get("message", "").strip()
            if not question:
                self.send_error(400, "Message cannot be empty")
                return

            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream; charset=utf-8")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Connection", "close")
            self.end_headers()

            async def stream_answer():
                async for event in ChatService().ask_streaming(question):
                    self.wfile.write(("data: " + json.dumps(event) + "\n\n").encode())
                    self.wfile.flush()
                self.wfile.write(b'data: {"type":"done"}\n\n')
                self.wfile.flush()

            asyncio.run(stream_answer())
        except (BrokenPipeError, ConnectionResetError):
            return
        except Exception as error:
            try:
                message = str(error) if os.getenv("DEBUG") else "The assistant request failed. Check the server configuration and try again."
                event = {"type": "error", "message": message}
                self.wfile.write(("data: " + json.dumps(event) + "\n\n").encode())
                self.wfile.flush()
            except (BrokenPipeError, ConnectionResetError):
                pass


def main():
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8000"))
    print(f"Chat frontend running at http://{host}:{port}")
    ThreadingHTTPServer((host, port), ChatHandler).serve_forever()


if __name__ == "__main__":
    main()
