#!/usr/bin/env python3

from restapi_helper import OpenAiHelper
from restapi_helper import OpenAiModerator

with OpenAiHelper() as oai:
    test_message = [
        {'role': 'system', 'content': """I'm a helpful assistant"""},
        {'role': 'user', 'content': 'Who won the world series in 2020?'}
    ]
    print(oai.chat_completion(test_message))

oam = OpenAiModerator()
oam.verify('this is valid text')
oam.verify('I hate you!')
