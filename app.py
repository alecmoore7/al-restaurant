# Copyright © 2023, Indiana University
# BSD 3-Clause License

from flask import Flask, render_template

app = Flask(__name__)

EMPLOYEES_PATH = app.root_path + '/employees.csv'
CUSTOMERS_PATH = app.root_path + '/customers.csv'
LAWNS_PATH = app.root_path + '/lawns.csv'

@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
