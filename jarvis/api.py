"""Loopback-only WSGI API for local JARVIS UI clients.

Deploy behind authenticated infrastructure before making it network-accessible.
"""
from __future__ import annotations
import json
from dataclasses import asdict
from typing import Callable
from wsgiref.simple_server import make_server
from .assistant_core import JarvisAssistant
from .agent import JarvisAgent

class JarvisAPI:
    def __init__(self, agent: JarvisAgent | None = None) -> None:
        self.agent = agent or JarvisAgent()
        self.assistant = JarvisAssistant(self.agent)

    @staticmethod
    def _response(start_response: Callable, status: str, payload: dict) -> list[bytes]:
        data = json.dumps(payload).encode("utf-8")
        start_response(status, [("Content-Type", "application/json"), ("Content-Length", str(len(data))), ("Cache-Control", "no-store")])
        return [data]

    def __call__(self, environ: dict, start_response: Callable) -> list[bytes]:
        method, path = environ.get("REQUEST_METHOD"), environ.get("PATH_INFO", "/")
        if method == "GET" and path == "/health": return self._response(start_response, "200 OK", {"ok": True})
        if method == "GET" and path == "/status": return self._response(start_response, "200 OK", self.agent.status())
        if method == "GET" and path == "/tasks": return self._response(start_response, "200 OK", {"tasks": [asdict(t) for t in self.agent.tasks.list()]})
        if method != "POST": return self._response(start_response, "404 Not Found", {"error": "Not found"})
        try:
            length = int(environ.get("CONTENT_LENGTH") or 0)
            body = json.loads(environ["wsgi.input"].read(length) or b"{}")
            if not isinstance(body, dict): raise ValueError("JSON object required")
        except (ValueError, json.JSONDecodeError): return self._response(start_response, "400 Bad Request", {"error": "A JSON object is required."})
        if path in {"/chat", "/command"}:
            text = body.get("text")
            if not isinstance(text, str): return self._response(start_response, "400 Bad Request", {"error": "text is required"})
            reply = self.assistant.respond(text)
            return self._response(start_response, "200 OK", {"text": reply.text, "action": reply.action})
        if path == "/tasks":
            title = body.get("title")
            if not isinstance(title, str): return self._response(start_response, "400 Bad Request", {"error": "title is required"})
            task = self.agent.tasks.create(title)
            return self._response(start_response, "201 Created", {"task": asdict(task)})
        if path == "/emergency-stop":
            self.agent.emergency_stop()
            return self._response(start_response, "200 OK", self.agent.status())
        return self._response(start_response, "404 Not Found", {"error": "Not found"})

def run(host: str = "127.0.0.1", port: int = 8765) -> None:
    """Run only on loopback by default; no authentication is provided for remote use."""
    with make_server(host, port, JarvisAPI()) as server:
        print(f"JARVIS local API listening on http://{host}:{port}")
        server.serve_forever()

if __name__ == "__main__": run()
