from flask import Flask
from flask import request, jsonify, render_template

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/')
def home():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
