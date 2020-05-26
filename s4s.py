#!/usr/bin/env python3

import getopt
import sys
import flask
import re
from flask import request, jsonify
from subprocess import Popen, PIPE

opts, args = getopt.getopt(
    sys.argv[1:],
    "hp:a:i:m:",
    ["help", "port=", "address=", "input-mode=", "method="]
)
opts = dict(opts)

def usage():
    print("""Service for Script
Usage: s4s [options] <script with arguments>
    -h --help
    -a --address (127.0.0.1)
    -p --port (5000)
    -i --input-mode <querystring|form> (form)
    -m --method <GET|POST> (POST)

Examples:
    s4s -p 7777 'echo $text'
    curl -F text=hello http://127.0.0.1:7777

    s4s -p 7777 nl
    curl -F file=@/path/to/file http://127.0.0.1:7777
""")
    sys.exit(0)

if "-h" in opts or "--help" in opts:
    usage()

PORT = int(opts.get("-p") or opts.get("--port") or "5000")
BIND_ADDRESS = opts.get("-a") or opts.get("--address") or "127.0.0.1"
INPUT_MODE = opts.get("-i") or opts.get("--input-mode") or "form"
METHOD = opts.get("-m") or opts.get("--method") or "POST"

if len(args) == 0:
    usage()

COMMAND = " ".join(args)

app = flask.Flask(__name__)
#app.config["DEBUG"] = True

@app.route('/', methods=[METHOD])
def index():
    # parse params
    params = {}
    if INPUT_MODE == "querystring":
        for k in request.args:
            params[k] = request.args.get(k)
    elif INPUT_MODE == "form":
        for k in request.form:
            params[k] = request.form.get(k)
    #print(params)
    command_stdin = ""
    if "file" in request.files:
        command_stdin = request.files["file"].read()
    # build command
    final_command = COMMAND
    for k in params:
        final_command = re.sub(r'\$\{?'+k+r'\}?', params[k], final_command)
    # run command
    child_process = Popen(re.split(r'\s+', final_command), stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = child_process.communicate(input=command_stdin)
    # result
    return stdout

app.run(host=BIND_ADDRESS, port=PORT)

