import os
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Jarvis is online and active!"

def run():
    # Render assigns a dynamic port via environment variables
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()