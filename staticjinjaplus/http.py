from __future__ import annotations
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from http import HTTPStatus
import os


class ThreadingHTTPServerWithConfig(ThreadingHTTPServer):
    """Same as ThreadingHTTPServer but the directory to be served may be passed to its constructor"""
    allow_reuse_address = True
    daemon_threads = True
    directory: str
    RequestHandlerClass: SimpleEnhancedHTTPRequestHandler

    def __init__(self, *args, directory: str, **kvargs):
        super().__init__(*args, **kvargs)

        self.directory = directory

    def finish_request(self, request, client_address):
        self.RequestHandlerClass(request, client_address, self, directory=self.directory)


class SimpleEnhancedHTTPRequestHandler(SimpleHTTPRequestHandler):
    """A simple HTTP server handler which is meant to serve the output directory, with some enhancements (emulates URL
    rewrite for HTML files without .html extension; emulates custom 404 error page"""
    protocol_version = 'HTTP/1.1'
    server: ThreadingHTTPServerWithConfig

    def __init__(self, *args, **kvargs):
        try:
            super().__init__(*args, **kvargs)
        except (ConnectionAbortedError, BrokenPipeError):
            pass

    def translate_path(self, path):
        path = super().translate_path(path)

        if not path.endswith(('\\', '/')):
            _, extension = os.path.splitext(path)

            if not extension:
                path += '.html'

        return path

    def send_error(self, code, message=None, explain=None):
        if self.command != 'HEAD' and code == HTTPStatus.NOT_FOUND:
            try:
                f = open(os.path.join(self.directory, '404.html'), 'rb')
            except OSError:
                return super().send_error(code, message=message, explain=explain)

            fs = os.fstat(f.fileno())

            self.log_error("code %d, message %s", code, message)
            self.send_response(code, message)
            self.send_header('Connection', 'close')

            self.send_header('Content-Type', self.error_content_type)
            self.send_header('Content-Length', str(fs[6]))
            self.end_headers()

            self.copyfile(f, self.wfile)
        else:
            return super().send_error(code, message=message, explain=explain)
