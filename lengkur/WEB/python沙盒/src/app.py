import os
import subprocess
import sys

import flask

app = flask.Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def home():
    return flask.render_template("index.html")


@app.route("/code", methods=["POST"])
def Runner():
    code = flask.request.form["code"]
    result = subprocess.run(
        [sys.executable, "-c", code], capture_output=True, text=True, timeout=10
    )
    return flask.render_template(
        "index.html", code=code, output=result.stdout, error=result.stderr
    )


if __name__ == "__main__":
    with open("/flag", "w", encoding="utf-8") as f:
        f.write(os.environ.get("GZCTF_FLAG", "flag{test}"))

    app.run(debug=True, host="0.0.0.0", port=80)
