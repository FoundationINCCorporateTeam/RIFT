"""
RIFT Standard Library - HTTP Module

HTTP server and client functionality.
"""

import json
import re
import asyncio
from typing import Any, Dict, List, Optional, Callable, Tuple
from urllib.parse import parse_qs, urlparse
from http.server import HTTPServer, BaseHTTPRequestHandler
from http.cookies import SimpleCookie
import threading


def create_http_module(interpreter) -> Dict[str, Any]:
    """Create the HTTP module for RIFT."""
    
    # ========================================================================
    # HTTP Server
    # ========================================================================
    
    class RiftHTTPServer:
        """HTTP server for RIFT applications."""
        
        def __init__(self):
            self._routes: List[Tuple[str, List[str], Any]] = []
            self._middleware: List[Any] = []
            self._static_routes: Dict[str, str] = {}
            self._error_handlers: Dict[int, Any] = {}
            self._server = None
            self._sessions: Dict[str, Dict] = {}
        
        def route(self, path: str, methods: List[str], handler) -> None:
            """Register a route with multiple methods."""
            # Convert path params to regex
            pattern = self._path_to_regex(path)
            self._routes.append((pattern, [m.upper() for m in methods], handler, path))
        
        def get(self, path: str, handler) -> None:
            """Register GET route."""
            self.route(path, ['GET'], handler)
        
        def post(self, path: str, handler) -> None:
            """Register POST route."""
            self.route(path, ['POST'], handler)
        
        def put(self, path: str, handler) -> None:
            """Register PUT route."""
            self.route(path, ['PUT'], handler)
        
        def delete(self, path: str, handler) -> None:
            """Register DELETE route."""
            self.route(path, ['DELETE'], handler)
        
        def patch(self, path: str, handler) -> None:
            """Register PATCH route."""
            self.route(path, ['PATCH'], handler)
        
        def options(self, path: str, handler) -> None:
            """Register OPTIONS route."""
            self.route(path, ['OPTIONS'], handler)
        
        def middleware(self, handler) -> None:
            """Add middleware."""
            self._middleware.append(handler)
        
        def static(self, url_path: str, directory: str) -> None:
            """Serve static files."""
            self._static_routes[url_path] = directory
        
        def error_handler(self, status_code: int, handler) -> None:
            """Register error handler."""
            self._error_handlers[status_code] = handler
        
        def _path_to_regex(self, path: str) -> str:
            """Convert path with params to regex."""
            # Replace :param with named capture group
            pattern = re.sub(r':(\w+)', r'(?P<\1>[^/]+)', path)
            return f'^{pattern}$'
        
        def _match_route(self, method: str, path: str) -> Optional[Tuple]:
            """Find matching route."""
            for pattern, methods, handler, original_path in self._routes:
                if method in methods:
                    match = re.match(pattern, path)
                    if match:
                        return handler, match.groupdict()
            return None
        
        def _parse_cookies(self, cookie_header: str) -> Dict[str, str]:
            """Parse cookie header."""
            cookies = {}
            if cookie_header:
                cookie = SimpleCookie()
                cookie.load(cookie_header)
                for key, morsel in cookie.items():
                    cookies[key] = morsel.value
            return cookies
        
        def _parse_body(self, content_type: str, body: bytes) -> Any:
            """Parse request body based on content type."""
            if not body:
                return {}
            
            if 'application/json' in content_type:
                try:
                    return json.loads(body.decode('utf-8'))
                except json.JSONDecodeError:
                    return {}
            elif 'application/x-www-form-urlencoded' in content_type:
                return {k: v[0] if len(v) == 1 else v 
                        for k, v in parse_qs(body.decode('utf-8')).items()}
            else:
                return body.decode('utf-8', errors='replace')
        
        def serve(self, port: int = 8080, host: str = '0.0.0.0') -> None:
            """Start the HTTP server."""
            server_instance = self
            interp = interpreter
            
            class RiftHandler(BaseHTTPRequestHandler):
                def log_message(self, format, *args):
                    pass  # Suppress logging
                
                def _handle_request(self, method):
                    # Parse URL
                    parsed = urlparse(self.path)
                    path = parsed.path
                    query = {k: v[0] if len(v) == 1 else v 
                             for k, v in parse_qs(parsed.query).items()}
                    
                    # Check static routes first
                    for url_path, directory in server_instance._static_routes.items():
                        if path.startswith(url_path):
                            file_path = path[len(url_path):].lstrip('/')
                            return self._serve_static(directory, file_path)
                    
                    # Find matching route
                    result = server_instance._match_route(method, path)
                    
                    if not result:
                        self._send_error(404, {'error': 'Not found'})
                        return
                    
                    handler, params = result
                    
                    # Parse request
                    content_length = int(self.headers.get('Content-Length', 0))
                    body = self.rfile.read(content_length) if content_length > 0 else b''
                    content_type = self.headers.get('Content-Type', '')
                    
                    # Build request object
                    request = {
                        'method': method,
                        'path': path,
                        'params': params,
                        'query': query,
                        'headers': dict(self.headers),
                        'body': server_instance._parse_body(content_type, body),
                        'cookies': server_instance._parse_cookies(
                            self.headers.get('Cookie', '')
                        ),
                        'session': {},
                    }
                    
                    # Run middleware
                    for mw in server_instance._middleware:
                        try:
                            mw_result = interp._call(mw, [request], None)
                            if mw_result is not None:
                                if isinstance(mw_result, dict) and 'status' in mw_result:
                                    self._send_response(mw_result)
                                    return
                        except Exception as e:
                            self._send_error(500, {'error': str(e)})
                            return
                    
                    # Call handler
                    try:
                        response = interp._call(handler, [request], None)
                        self._send_response(response)
                    except Exception as e:
                        self._send_error(500, {'error': str(e)})
                
                def _send_response(self, response):
                    if response is None:
                        self.send_response(204)
                        self.end_headers()
                        return
                    
                    if isinstance(response, dict):
                        status = response.get('status', 200)
                        headers = response.get('headers', {})
                        body = response.get('body', '')
                        content_type = response.get('contentType', 'application/json')
                        
                        self.send_response(status)
                        self.send_header('Content-Type', content_type)
                        
                        for key, value in headers.items():
                            self.send_header(key, value)
                        
                        # Handle cookies
                        if 'cookies' in response:
                            for name, value in response['cookies'].items():
                                self.send_header('Set-Cookie', f'{name}={value}')
                        
                        self.end_headers()
                        
                        if isinstance(body, dict) or isinstance(body, list):
                            self.wfile.write(json.dumps(body).encode())
                        elif isinstance(body, bytes):
                            self.wfile.write(body)
                        else:
                            self.wfile.write(str(body).encode())
                    else:
                        self.send_response(200)
                        self.send_header('Content-Type', 'text/plain')
                        self.end_headers()
                        self.wfile.write(str(response).encode())
                
                def _send_error(self, status, body):
                    self.send_response(status)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(body).encode())
                
                def _serve_static(self, directory, file_path):
                    import os
                    import mimetypes
                    
                    full_path = os.path.join(directory, file_path)
                    
                    if not os.path.exists(full_path) or not os.path.isfile(full_path):
                        self._send_error(404, {'error': 'File not found'})
                        return
                    
                    mime_type, _ = mimetypes.guess_type(full_path)
                    if not mime_type:
                        mime_type = 'application/octet-stream'
                    
                    try:
                        with open(full_path, 'rb') as f:
                            content = f.read()
                        
                        self.send_response(200)
                        self.send_header('Content-Type', mime_type)
                        self.send_header('Content-Length', len(content))
                        self.end_headers()
                        self.wfile.write(content)
                    except IOError:
                        self._send_error(500, {'error': 'Error reading file'})
                
                def do_GET(self):
                    self._handle_request('GET')
                
                def do_POST(self):
                    self._handle_request('POST')
                
                def do_PUT(self):
                    self._handle_request('PUT')
                
                def do_DELETE(self):
                    self._handle_request('DELETE')
                
                def do_PATCH(self):
                    self._handle_request('PATCH')
                
                def do_OPTIONS(self):
                    self._handle_request('OPTIONS')
            
            print(f"RIFT server running on http://{host}:{port}")
            self._server = HTTPServer((host, port), RiftHandler)
            
            try:
                self._server.serve_forever()
            except KeyboardInterrupt:
                print("\nServer stopped")
                self._server.shutdown()
        
        def stop(self):
            """Stop the server."""
            if self._server:
                self._server.shutdown()
    
    # Global server instance
    _server = RiftHTTPServer()
    
    # ========================================================================
    # Response Helpers
    # ========================================================================
    
    def http_json(status: int, data: Any, headers: Dict = None) -> Dict:
        """Create JSON response."""
        return {
            'status': status,
            'contentType': 'application/json',
            'body': data,
            'headers': headers or {}
        }
    
    def http_text(status: int, text: str, headers: Dict = None) -> Dict:
        """Create text response."""
        return {
            'status': status,
            'contentType': 'text/plain',
            'body': text,
            'headers': headers or {}
        }
    
    def http_html(status: int, html: str, headers: Dict = None) -> Dict:
        """Create HTML response."""
        return {
            'status': status,
            'contentType': 'text/html',
            'body': html,
            'headers': headers or {}
        }
    
    def http_css(status: int, css: str, headers: Dict = None) -> Dict:
        """Create CSS response."""
        return {
            'status': status,
            'contentType': 'text/css',
            'body': css,
            'headers': headers or {}
        }
    
    def http_js(status: int, js: str, headers: Dict = None) -> Dict:
        """Create JS response."""
        return {
            'status': status,
            'contentType': 'application/javascript',
            'body': js,
            'headers': headers or {}
        }
    
    def http_file(path: str, content_type: str = None) -> Dict:
        """Create file response."""
        import os
        import mimetypes
        
        if not os.path.exists(path):
            return http_json(404, {'error': 'File not found'})
        
        if not content_type:
            content_type, _ = mimetypes.guess_type(path)
            if not content_type:
                content_type = 'application/octet-stream'
        
        with open(path, 'rb') as f:
            content = f.read()
        
        return {
            'status': 200,
            'contentType': content_type,
            'body': content,
            'headers': {
                'Content-Length': str(len(content))
            }
        }
    
    def http_redirect(url: str, status: int = 302) -> Dict:
        """Create redirect response."""
        return {
            'status': status,
            'headers': {'Location': url},
            'body': ''
        }
    
    # ========================================================================
    # HTTP Client
    # ========================================================================
    
    def http_request(url: str, options: Dict = None) -> Dict:
        """Make HTTP request."""
        import urllib.request
        import urllib.error
        
        options = options or {}
        method = options.get('method', 'GET').upper()
        headers = options.get('headers', {})
        body = options.get('body', None)
        timeout = options.get('timeout', 30)
        
        # Prepare body
        data = None
        if body:
            if isinstance(body, dict):
                data = json.dumps(body).encode('utf-8')
                if 'Content-Type' not in headers:
                    headers['Content-Type'] = 'application/json'
            elif isinstance(body, str):
                data = body.encode('utf-8')
            elif isinstance(body, bytes):
                data = body
        
        # Create request
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                response_body = response.read()
                content_type = response.headers.get('Content-Type', '')
                
                # Parse response body
                if 'application/json' in content_type:
                    try:
                        parsed_body = json.loads(response_body.decode('utf-8'))
                    except json.JSONDecodeError:
                        parsed_body = response_body.decode('utf-8')
                else:
                    parsed_body = response_body.decode('utf-8', errors='replace')
                
                return {
                    'status': response.status,
                    'headers': dict(response.headers),
                    'body': parsed_body,
                    'ok': 200 <= response.status < 300
                }
        except urllib.error.HTTPError as e:
            response_body = e.read()
            return {
                'status': e.code,
                'headers': dict(e.headers),
                'body': response_body.decode('utf-8', errors='replace'),
                'ok': False,
                'error': str(e)
            }
        except urllib.error.URLError as e:
            return {
                'status': 0,
                'headers': {},
                'body': None,
                'ok': False,
                'error': str(e)
            }
    
    def http_get(url: str, headers: Dict = None) -> Dict:
        """Make GET request."""
        return http_request(url, {'method': 'GET', 'headers': headers or {}})
    
    def http_post(url: str, body: Any = None, headers: Dict = None) -> Dict:
        """Make POST request."""
        return http_request(url, {
            'method': 'POST',
            'body': body,
            'headers': headers or {}
        })
    
    def http_put(url: str, body: Any = None, headers: Dict = None) -> Dict:
        """Make PUT request."""
        return http_request(url, {
            'method': 'PUT',
            'body': body,
            'headers': headers or {}
        })
    
    def http_delete_client(url: str, headers: Dict = None) -> Dict:
        """Make DELETE request."""
        return http_request(url, {'method': 'DELETE', 'headers': headers or {}})
    
    # ========================================================================
    # Module Exports
    # ========================================================================
    
    return {
        # Server
        'route': _server.route,
        'get': _server.get,
        'post': _server.post,
        'put': _server.put,
        'delete': _server.delete,
        'patch': _server.patch,
        'options': _server.options,
        'middleware': _server.middleware,
        'static': _server.static,
        'serve': _server.serve,
        'stop': _server.stop,
        
        # Response helpers
        'json': http_json,
        'text': http_text,
        'html': http_html,
        'css': http_css,
        'js': http_js,
        'file': http_file,
        'redirect': http_redirect,
        
        # Client
        'request': http_request,
        'fetch': http_get,
        'postTo': http_post,
        'putTo': http_put,
        'deleteFrom': http_delete_client,
        
        # Create new server instance
        'createServer': lambda: RiftHTTPServer(),
    }
