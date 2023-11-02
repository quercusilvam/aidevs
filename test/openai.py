#!/usr/bin/env python3
import sys

from restapi_helper import OpenAiHelper
from restapi_helper import OpenAiModerator
from restapi_helper import ModeratorValidationException

with OpenAiHelper() as oai:
    test_message = [
        {'role': 'system', 'content': """I'm a helpful assistant"""},
        {'role': 'user', 'content': 'Who won the world series in 2020?'}
    ]
    print(oai.chat_completion(test_message))

oam = OpenAiModerator()
try:
    oam.verify('This is valid text')
except ModeratorValidationException:
    print(f'[ERROR] caught ModeratorValidationException but did not')
else:
    print('Verified ok')

try:
    oam.verify('I hate you!')
except ModeratorValidationException as e:
    print(f'Correctly catches {e}')
else:
    print(f'[ERROR] Should rise ModeratorValidationException but did not')
