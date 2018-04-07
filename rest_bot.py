from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import logging
import warnings


from rasa_core import utils
from rasa_core.actions import Action
from rasa_core.agent import Agent
from rasa_core.channels.console import ConsoleInputChannel
from rasa_core.events import SlotSet
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.policies.memoization import MemoizationPolicy

logger = logging.getLogger(__name__)
from rasa_core.channels.custom import *


def run(serve_forever=True):
    interpreter = RasaNLUInterpreter("models/nlu/default/current_sp")
    agent = Agent.load("models/dialogue", interpreter=interpreter)
    customInput = CustomInput('localhost:8080')
    if serve_forever:
        agent.handle_channel(customInput)
    return agent


if __name__ == '__main__':
    utils.configure_colored_logging(loglevel="INFO")

    parser = argparse.ArgumentParser(
            description='starts the bot')

    run()



