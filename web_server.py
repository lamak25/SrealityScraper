import http.server
import socketserver
import os
import json
from sreality_scraper.src.DBS_sreality import DBS_sreality
from time import sleep

# Set the port number you want to use
PORT = 8080

# Set the directory where your website files are located
DIRECTORY = "./"

# Specify the HTML file to serve
HTML_FILE = "./templates/index.html"
ITEM_FILE = "./templates/item.html"

def create_all_tiles(all_items):
    with open(ITEM_FILE, 'rb') as item_html:
        html = item_html.read().decode('utf-8')

    result_items = ''

    if len(all_items) == 0:
        result_items = "No items here"
    #for j in range(250): # For testing
    for i in all_items:
        html1 = html.replace('{url}', i[1]) # insert url into template
        html1 = html1.replace('{img}', i[3]) # insert img into template
        html1 = html1.replace('{headline}', i[2]) # insert headline into template
        result_items += html1
    return result_items

# Create a custom handler to serve the specified HTML file
class MyHandler(http.server.SimpleHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        self.DB = DBS_sreality("postgres", "postgres", "my_super_strong_password", "127.0.0.1", "5432")
        self.DB.create_open_database()

        # Populate for testing purposes
        #for i in range(3):
        #    self.DB.insert_item(str(12345678900 + i), "https://www.sreality.cz/detail/prodej/byt/2+kk/usti-nad-labem-severni-terasa-sramkova/2212459596", "Sample headlineee", "https://d18-a.sdn.cz/d_18/c_img_QM_Kb/dAFbUn.jpeg?fl=res,749,562,3|wrm,/watermark/sreality.png,10|shr,,20|jpg,90")

        # Call the superclass's __init__ method
        super().__init__(*args, **kwargs)

    def do_GET(self):
        # Ready for framework
        #if self.path == '/regenerate':
            # response = {'item': 'Hello, world!'}
            # print("REGENERETING TODO")
            # self.send_response(200)
            # self.send_header('Content-Type', 'application/json')
            # self.end_headers()
            # self.wfile.write(json.dumps(response).encode())
        if self.path == '/':
            self.path = HTML_FILE

            # Get an items from DB
            all_items = self.DB.get_all_items()
            print(all_items)

            with open(HTML_FILE, 'rb') as file:
                html = file.read().decode('utf-8')
                items_html = create_all_tiles(all_items)
                html = html.replace('{items}', items_html) # insert items into template
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                self.wfile.write(html.encode())
            return
        else:
            return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def __del__(self):
        if self.DB is not None:
            del self.DB

def run_server(DIRECTORY, PORT, MyHandler):
    # Use socketserver to set up and run the server
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print("Connection successful!", flush=True)
        print(f"Server running on port {PORT}", flush=True)
        print(f"Open http://localhost:{PORT}/ in your browser to access the website.", flush=True)
        print(f"To access the API endpoint, go to http://localhost:{PORT}/getitem", flush=True)

        # Set the current working directory to the website directory
        os.chdir(DIRECTORY)

        # Start the server and keep it running until interrupted
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass

        # Close the server when interrupted
        httpd.server_close()
        print("Server stopped.")

tried = 0
wait_time_for_DB = 3
print("Waitin %s for DB." % (wait_time_for_DB, ), flush=True)
sleep(wait_time_for_DB) # wait, perhaps the DB is starting
while True: # Find free port
    try:
        print("Trying to connect to DB... (after end and immediate restart it can take around 10-20 tries to connect)", flush=True)
        run_server(DIRECTORY, PORT, MyHandler)
        break
    except OSError:
        #PORT += 1
        tried += 1
        sleep(3) # wait, perhaps the DB is starting
        if tried > 50:
            print("Port/DB's problem")
            break
        continue
