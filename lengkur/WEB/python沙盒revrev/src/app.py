import os
import subprocess
import sys

import flask

app = flask.Flask(__name__)


def waf(code):
    blacklisted_keywords = [
        "import",
        "open",
        "read",
        "write",
        "exec",
        "eval",
        "__",
        "os",
        "sys",
        "subprocess",
        "run",
        "flag",
        "'",
        '"',
    ]
    for keyword in blacklisted_keywords:
        if keyword in code:
            return False
    return True


@app.route("/", methods=["POST", "GET"])
def home():
    return flask.render_template("index.html")


@app.route("/code", methods=["POST"])
def Runner():
    code = flask.request.form["code"]

    if not code:
        return flask.render_template(
            "index.html", code=code, output="", error="请输入代码"
        )
    if not waf(code):
        return flask.render_template(
            "index.html", code=code, output="", error="Hacker!!!"
        )
    ultimate = f"""
import sys
sys.modules['os'] = 'not allowed'

def is_my_love_event(event_name):
    return event_name.startswith("Nothing is my love but you.") 

def my_audit_hook(event_name, arg):
    if len(event_name) > 0:
        raise RuntimeError("Too long event name!")
    if len(arg) > 0:
        raise RuntimeError("Too long arg!")
    if not is_my_love_event(event_name):
        raise RuntimeError("Hacker out!")

__import__('sys').addaudithook(my_audit_hook)

{code}"""

    result = subprocess.run(
        [sys.executable, "-c", ultimate], capture_output=True, text=True, timeout=10
    )
    return flask.render_template(
        "index.html", code=code, output=result.stdout, error=result.stderr
    )


if __name__ == "__main__":
    with open("/flag", "w", encoding="utf-8") as f:
        flag = os.environ.pop("GZCTF_FLAG", "flag{test}")
        f.write(flag)

    app.run(host="0.0.0.0", port=8070)
