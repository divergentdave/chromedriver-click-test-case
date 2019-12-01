import base64
import http.server
import json
import urllib.parse


class MockResponse:
    pass


class BodyResponse:
    def __init__(self, data):
        self.data = data


class RedirectResponse:
    def __init__(self, code, location):
        self.code = code
        self.location = location


def process_har(har):
    log = har["log"]
    entries = log["entries"]
    mock_map = {}
    for entry in entries:
        request = entry["request"]
        method = request["method"]
        url = request["url"]

        if "matomo.courtlistener.com" in url:
            continue
        if url == "http://172.18.0.7:35011/touch-icon-192x192.png":
            continue

        url_parsed = urllib.parse.urlsplit(url)
        if url_parsed.query:
            path_and_query = "{}?{}".format(url_parsed.path, url_parsed.query)
        else:
            path_and_query = url_parsed.path

        key = (method, path_and_query)
        if key in mock_map:
            raise Exception("URL appears more than once: {}".format(url))

        response = entry["response"]
        status = response["status"]
        if status == 200:
            content = response["content"]
            text = content["text"]
            if "encoding" in content:
                encoding = content["encoding"]
                if encoding == "base64":
                    mock_map[key] = BodyResponse(base64.b64decode(text))
                else:
                    raise Exception("Unsupported encoding: {}"
                                    .format(encoding))
            else:
                mock_map[key] = BodyResponse(text.encode("utf-8"))
        elif status == 301:
            location = None
            for header in response["headers"]:
                if header["name"] == "Location":
                    location = header["value"]
                    break
            mock_map[key] = RedirectResponse(status, location)

    return mock_map


class MockRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        key = ("GET", self.path)
        resp = self.server.mocks.get(key)
        if isinstance(resp, BodyResponse):
            self.send_response(200)
            self.send_header("Content-Length", len(resp.data))
            self.end_headers()
            self.wfile.write(resp.data)
        elif isinstance(resp, RedirectResponse):
            self.send_response(resp.code)
            self.send_header("Location", resp.location)
            self.end_headers()
        else:
            print("No response found for {}".format(self.path))
            self.send_error(500)
            self.end_headers()


def main():
    server_address = ('', 8000)
    server = http.server.HTTPServer(server_address, MockRequestHandler)
    with open("capture.har", "rb") as f:
        har = json.load(f)
    server.mocks = process_har(har)
    print("starting server")
    server.serve_forever()


if __name__ == "__main__":
    main()
