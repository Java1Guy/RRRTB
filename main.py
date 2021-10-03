# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
from jinja2 import Environment, FileSystemLoader, select_autoescape
import sys, getopt
from make_requests import ResultsSubsystem

hostName = "localhost"
serverPort = 8080
env = Environment(
    loader=FileSystemLoader("."),
    autoescape=select_autoescape()
)
template = env.get_template("main_page.html")


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        data = results_server.data
        last_read = results_server.last_read
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        print()
        self.wfile.write(bytes(template.render(data=data, time=last_read), "utf-8"))


if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:e:k:", ["interval=", "eventid=", "apikey="])
    except getopt.GetoptError:
        print('main.py -i <interval> -e <eventid> -k <apikey>')
        sys.exit(2)
    interval = 5
    event_id = ''
    api_key = ''
    for opt, arg in opts:
        if opt == '-h':
            print('main.py -i <interval> -e <eventid> -k <apikey>')
            sys.exit()
        elif opt in ("-i", "--interval"):
            interval = int(arg)
        elif opt in ("-e", "--eventid"):
            event_id = arg
        elif opt in ("-k", "--apikey"):
            api_key = arg
    if len(event_id) == 0:
        print("Event ID is required:")
        print('main.py -i <interval> -e <eventid> -k <apikey>')
        sys.exit()
    if len(api_key) == 0:
        print("API Key is required:")
        print('main.py -i <interval> -e <eventid> -k <apikey>')
        sys.exit()

    results_server = ResultsSubsystem(event_id, api_key)
    results_server.start_subsystem(interval)
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    webServer.server_close()
    results_server.stop_subsystem()
    print("Web Server stopped.")
