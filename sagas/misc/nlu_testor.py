#!/usr/bin/env python
import utils
from rasa_nlu.model import Interpreter

def test_formbot():
    model_directory="examples/formbot/models/nlu/current"
    interpreter = Interpreter.load(model_directory)
    text="uh yes"
    result=interpreter.parse(text)
    utils.dump(result)

    text="what about chinese food"
    result=interpreter.parse(text)
    utils.dump(result)

if __name__ == '__main__':
    test_formbot()