# APIMyLlama V2 Documentation

## Overview

[![APIMyLlama Video](https://img.youtube.com/vi/x_MSmGX3Vmc/hqdefault.jpg)](https://www.youtube.com/embed/x_MSmGX3Vmc)

APIMyLlama is a server application that provides an interface to interact with the Ollama API, a powerful AI tool to run LLMs. It allows users to run this alongside Ollama to easily distribute API keys to create amazing things.

### Support Us

We now have a [Ko-fi](https://ko-fi.com/gimerstudios) open if you would like to help and donate to the project. We love to keep it free and open source when possible and donating helps a lot.

[Donate through Ko-fi](https://ko-fi.com/gimerstudios)

# Installation

## Prerequisites

- Python 3.8 or higher
- [Ollama](https://ollama.com/download) installed on your system
- pip (Python package installer)

## Ollama Setup
If you already have Ollama setup with the 'ollama serve' command and your desired model, you can skip this section. If not, here's how to set it up:

1. Install [Ollama](https://ollama.com/download) for your desired operating system
2. Pull the Llama model (or any other model you prefer):
```bash
ollama pull llama3
```

3. Start the Ollama server:
```bash
ollama serve
```

## Hosting the API

1. Clone the repository:
```bash
git clone https://github.com/Gimer-Studios/APIMyLlama.git
cd APIMyLlama
```

2. Install the required Python dependencies:
```bash
pip install -r requirements.txt
```

3. Start the application:
```bash
python app.py
```

On startup, you'll be prompted to:
- Enter a port number for the API server
- Provide the Ollama server URL (default is "http://localhost:11434")

## CLI Commands

The application provides an interactive command-line interface with the following commands:

- `generatekey`: Generate a new API key
- `listkey`: List all API keys
- `removekey <key>`: Remove an API key
- `addkey <key>`: Add a custom API key
- `changeport <port>`: Change the server port
- `changeollamaurl <url>`: Change the Ollama server URL
- `ratelimit <key> <limit>`: Set rate limit for an API key
- `addwebhook <url>`: Add a webhook URL
- `deletewebhook <id>`: Delete a webhook
- `listwebhooks`: List all webhooks
- `activatekey <key>`: Activate an API key
- `deactivatekey <key>`: Deactivate an API key
- `exit`: Exit the CLI

## Running on Different Systems

### Running Ollama on a Different Machine

If you're running Ollama on a different machine than APIMyLlama, you'll need to configure Ollama to listen on all interfaces:

#### Windows:
Set a System Environment Variable:
```
Variable: OLLAMA_HOST
Value: 0.0.0.0
```

#### Linux:
Either edit the service file `/etc/systemd/system/ollama.service` and add under [Service]:
```
Environment="OLLAMA_HOST=0.0.0.0"
```

Or run Ollama with:
```bash
OLLAMA_HOST=0.0.0.0 ollama serve
```

Then, when configuring APIMyLlama, use the appropriate server URL:
```
http://<YOUR_SERVER_IP>:11434
```

## API Endpoints

### Health Check
```
GET /health?apikey=<YOUR_API_KEY>
```

### Generate Response
```
POST /generate
Content-Type: application/json

{
    "apikey": "<YOUR_API_KEY>",
    "model": "llama2",
    "prompt": "Your prompt here",
    "stream": false,
    "images": [],
    "raw": false
}
```

## Troubleshooting

### Common Issues

#### 1. Port Already in Use
Choose a different port using the `changeport` command or modify the port.conf file.

#### 2. Database Connection Issues
Ensure you have write permissions in the application directory for the SQLite database.

#### 3. Ollama Connection Error
If you get "Error making request to Ollama API", verify:
- Ollama is running (`ollama serve`)
- The Ollama URL is correct (use `changeollamaurl` to update if needed)
- Network connectivity between APIMyLlama and Ollama server

#### 4. Rate Limiting
Each API key has a default rate limit. Use the `ratelimit` command to adjust it if needed.

## Examples to get response from API

Python example:
```python
import requests
from apimyllama import ApiMyLlama

def main():
    ip = "SERVER_IP"
    port = "PORT_NUMBER"
    apikey = "API_KEY" 
    prompt = "Hello"
    model = "llama3" 
    api = ApiMyLlama(ip, port)
    try:
        result = api.generate(apikey, prompt, model)
        print("API Response:", result)
    except requests.RequestException as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main()
```

## Checking API Health
The packages have built in health checking command (AS OF V2)
If you already have the Node.js or Python packages installed then you can just copy and paste the code below to test.

Python example:
```python
import requests
from apimyllama import ApiMyLlama

ip = 'YOUR_SERVER_IP'
port = 'YOUR_SERVER_PORT'
apikey = 'YOUR_API_KEY'

api = ApiMyLlama(ip, port)

try:
    health = api.get_health(apikey)
    print("Health Check Response:", health)
except requests.RequestException as error:
    print("Error:", error)
```

## API References
```
ApiMyLlama(ip, port)
ip: IP address of the APIMyLlama server.
port: Port number on which the APIMyLlama server is running.
```
```
api.generate(apiKey, prompt, model, stream)
api.get_health(apikey)
apiKey: API key for accessing the Ollama API.
prompt: Text prompt to generate a response.
model: Machine learning model to use for text generation.
stream: Boolean indicating whether to stream the response.
```

# Support
If there are any issues please make a Github Issue Report. To get quicker support join our discord server.
-[Discord Server](https://discord.gg/r6XazGtKg7) If there are any feature requests you may request them in the discord server. PLEASE NOTE this project is still in EARLY BETA. 

### Support Us

We now have a [Ko-fi](https://ko-fi.com/gimerstudios) open if you would like to help and donate to the project. We love to keep it free and open source when possible and donating helps a lot.

[Donate through Ko-fi](https://ko-fi.com/gimerstudios)

## FAQ

#### 1. Why am I getting the module not found error?

You most likely forgot to run the 'pip install -r requirements.txt' command after cloning the repository.

#### 2. Why can't I use the API outside my network?

You probably didn't port foward. And if you did your router may have not intialized the changes yet or applied them.

#### 3. Ollama Serve command error "Error: listen tcp 127.0.0.1:11434: bind: Only one usage of each socket address (protocol/network address/port) is normally permitted."

If you get this error just close the Ollama app through the system tray on Windows. And if your on Linux just use systemctl to stop the Ollama process. Once done you can try running the ollama serve command again.

#### 4. error: 'Error making request to Ollama API'

If you have a custom port set for your Ollama server this is a simple fix. Just run the 'changeollamaurl <YOUR_OLLAMA_SERVER_URL>' and change it to the url your Ollama server is running on. By default it is "http://localhost:11434" but if you changed it you will need to do this. You can also fix this problem through changing the port in the ollamaURL.conf file.

## Authors

- [@gimerstudios](https://github.com/Gimer-Studios)
