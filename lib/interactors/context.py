""" Context object for interactors file """
import os
import sys

sys.path.insert(0, os.path.realpath(os.path.dirname(__file__)) + '/../../lib')

from interactors.api_interactor import MatchHistoryBySequenceNum

class Context(object):
    def __init__(self):
        self.history = MatchHistoryBySequenceNum()
