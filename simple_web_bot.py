from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

import argparse
import logging
import warnings
import json
from rasa_core.channels import HttpInputChannel
from rasa_core import utils
from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.channels.channel import UserMessage
from rasa_core.channels.direct import CollectingOutputChannel
from rasa_core.channels.rest import HttpInputComponent
from flask import Blueprint, request, jsonify, Response





class SimpleWebBot(HttpInputComponent):
    """A simple web bot that listens on a url and responds."""

    def blueprint(self, on_new_message):
        custom_webhook = Blueprint('custom_webhook', __name__)

        @custom_webhook.route("/status", methods=['GET'])
        def health():
            return jsonify({"status": "ok"})



        @custom_webhook.route("/", methods=['POST'])
        def receive():

            payload = request.json
            resp = Response({} , status=200, mimetype='application/json')
            if request.method == 'POST':
                sender_id = payload.get("sender", None)
                text = payload.get("message", None)
                out = CollectingOutputChannel()
                on_new_message(UserMessage(text, out, sender_id))
                print(out.messages)
                responses = [m["text"] if "text" in m else m[1] for m in out.messages]
                resp = Response(responses , status=200, mimetype='application/json')
            resp.headers["Access-Control-Allow-Origin"] = "*"
            resp.headers["Access-Control-Allow-Headers"] = "X-Requested-With"
            resp.headers["Allow"] = "GET,HEAD,POST,OPTIONS,TRACE"
            resp.headers["Content-Type"] = "application/json"
            return resp

        return custom_webhook


def run(serve_forever=True, model_name='current_sp'):
    # path to your NLU model
    interpreter = RasaNLUInterpreter("models/nlu/default/"+model_name)
    # path to your dialogues models
    agent = Agent.load("models/dialogue", interpreter=interpreter)
    # http api endpoint for responses
    input_channel = SimpleWebBot()
    if serve_forever:
        agent.handle_channel(HttpInputChannel(5004, "/chat", input_channel))
    return agent

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Starts the diego bot server')

    parser.add_argument('--fixed_model_name',
                        help="If present, a model will always be persisted "
                             "in the specified directory instead of creating "
                             "a folder like 'model_20171020-160213'")

    cmdline_args = parser.parse_args()

    run(model_name=cmdline_args.fixed_model_name )
