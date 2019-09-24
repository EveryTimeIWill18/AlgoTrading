"""
flask_back_end.py
~~~~~~~~~~~~~~~~~
"""
from flask import Flask

app = Flask(__name__)

@app.route('/')
def temp_route():
    return "<h2>Temp route</h2>"


if __name__ == '__main__':
    app.run(debug=True)
