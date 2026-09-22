import os
from flask import Flask, send_from_directory

app = Flask(__name__)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def home(path):
    target = os.path.join(ROOT_DIR, path)
    if path != "" and os.path.exists(target) and not os.path.isdir(target):
        return send_from_directory(ROOT_DIR, path)
    return send_from_directory(ROOT_DIR, 'index.html')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
