from flask import Flask
from flask import request
from flask import make_response
from flask import render_template
import fileinput, sys
from peopleworkingonbuilds import *
app = Flask(__name__)

@app.route("/claim")
def claim():
    build_name = request.args.get("build", '').strip()
    person = request.args.get("person", '').strip()
    new_claim_line = build_name + "::::" + person + "\n"

    claims = get_claims_as_hash()
    claims[build_name] = person
    save_claims(claims)
    response = make_response()
    response.headers["Access-Control-Allow-Origin"] = "<origin> | *";
    return "ok"

@app.route("/clear")
def clear():
    build_name = request.args.get("build", '').strip()
    
    claims = get_claims_as_hash()
    if claims.has_key(build_name):
        claims.pop(build_name)
    save_claims(claims)
    return "ok"

@app.route("/setup")
def setup():
    return render_template("setup.html")

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=8081)
