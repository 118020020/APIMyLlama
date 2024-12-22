from flask import Flask
import os
from db import db_instance
from api import API
import cmd
import threading
from utils import Utils

app = Flask(__name__)
app.json.sort_keys = False

def read_port():
    if os.path.exists('port.conf'):
        with open('port.conf', 'r') as f:
            return int(f.read().strip())
    return None

def read_ollama_url():
    if os.path.exists('ollamaURL.conf'):
        with open('ollamaURL.conf', 'r') as f:
            return f.read().strip()
    return None

def write_port(port):
    with open('port.conf', 'w') as f:
        f.write(str(port))
    print(f"Port number saved to port.conf: {port}")

def write_ollama_url(url):
    with open('ollamaURL.conf', 'w') as f:
        f.write(url)
    print(f"Ollama url saved to ollamaURL.conf: {url}")

def ask_for_port():
    while True:
        try:
            port = int(input('Enter the port number for the API server: '))
            write_port(port)
            return port
        except ValueError:
            print("Please enter a valid port number")

def ask_for_ollama_url():
    url = input('Enter the URL for the Ollama server (URL that your Ollama server is running on. '
                'By default it is "http://localhost:11434" so if you didnt change anything it should be that.): ')
    write_ollama_url(url)
    return url

class CLI(cmd.Cmd):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.utils = Utils(db)
        self.prompt = '> '

    def do_generatekey(self, arg):
        """Generate a new API key"""
        self.utils.generate_key()

    def do_listkey(self, arg):
        """List all API keys"""
        self.utils.list_keys()

    def do_removekey(self, arg):
        """Remove an API key"""
        if not arg:
            print("Please provide an API key to remove")
            return
        self.utils.remove_key(arg)

    def do_addkey(self, arg):
        """Add a custom API key"""
        if not arg:
            print("Please provide an API key to add")
            return
        self.utils.add_key(arg)

    def do_changeport(self, arg):
        """Change the server port"""
        try:
            port = int(arg)
            write_port(port)
            print(f"Port changed to {port}. Please restart the server for changes to take effect.")
        except ValueError:
            print("Please provide a valid port number")

    def do_changeollamaurl(self, arg):
        """Change the Ollama server URL"""
        if not arg:
            print("Please provide a URL")
            return
        write_ollama_url(arg)
        print("Ollama URL updated successfully")

    def do_ratelimit(self, arg):
        """Set rate limit for an API key"""
        args = arg.split()
        if len(args) != 2:
            print("Usage: ratelimit <key> <limit>")
            return
        try:
            self.utils.set_rate_limit(args[0], int(args[1]))
        except ValueError:
            print("Please provide a valid rate limit number")

    def do_exit(self, arg):
        """Exit the CLI"""
        return True

def main():
    print('APIMyLlama python version is started.')
    
    # Initialize database
    db = db_instance.initialize_database()
    
    # Get or ask for port
    port = read_port()
    if port is None:
        port = ask_for_port()
    
    # Get or ask for Ollama URL
    ollama_url = read_ollama_url()
    if ollama_url is None:
        ollama_url = ask_for_ollama_url()
    
    # Setup API
    API(app, db)
    
    # Start CLI in a separate thread
    cli = CLI(db)
    cli_thread = threading.Thread(target=cli.cmdloop)
    cli_thread.daemon = True
    cli_thread.start()
    
    # Start the server
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    main()
