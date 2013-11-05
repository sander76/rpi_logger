'''
Created on 28 aug. 2013

@author: Teunissen-S
'''
import os
import sys
from logger.persistence import Persistence
from logger.serialport import SerialPort
from arduino.em304parser import Em304Parser
from logger.loggers import EventBasedLogger
from flask import Flask, make_response
from logger.server import create_flask
from werkzeug.exceptions import abort
from flask.helpers import send_file, send_from_directory
from flask.wrappers import Response
pth = os.path.dirname(__file__)
os.chdir(pth)
import json
import logging
lgr = logging.getLogger(__name__)
app = Flask(__name__, static_folder="logger/static")
persistence = Persistence("output.txt")


@app.route('/')
def startpoint():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/static/<path:path>')
def catch_all(path):
    try:
        return send_from_directory(app.static_folder, path)
    except IOError:
        return


@app.route("/getlog/log.json")
def get_log():
    global persistence
    persistence.getlog()
    fl = persistence.return_queue.get(block=True, timeout=10)
    if fl:
        try:
            return Response(fl.file.readlines(), mimetype='text/json')
        except:
            abort('500')
        finally:
            fl.close()
    else:
        abort('500')


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.DEBUG)
        # logging.basicConfig(filename='error.log', level=logging.ERROR)

        # persistence = Persistence("/media/logger/output.txt")

        persistence.start()
        # create a serial port logger.
        serialport = SerialPort("COM16", 5)
        em341parser = Em304Parser()
        em341logger = EventBasedLogger(serialport, persistence, em341parser)
        em341logger.start()

        # app = create_flask()
        app.run(host='0.0.0.0', use_debugger=False, use_reloader=False, debug=True)

    except Exception, k:
        lgr.error(k)
        # go_on = 0

