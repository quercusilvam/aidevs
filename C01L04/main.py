#!/usr/bin/env python3
import argparse
from restapi_helper import OpenAiHelper
from restapi_helper import AiDevsRestapiHelper
from restapi_helper import OpenAiModerator
from restapi_helper import ModeratorValidationException

parser = argparse.ArgumentParser(description='Solve first task')
parser.add_argument('-t', '--taskname', help='The task_name', required=True)
args = parser.parse_args()

task_name = args.taskname

if task_name == 'moderation':
    with AiDevsRestapiHelper(task_name) as restapi:
        js = restapi.get_task()
        oam = OpenAiModerator()
        response = []
        for text in js['input']:
            try:
                oam.verify(text)
                print(f'Verifying text="{text}"')
            except ModeratorValidationException:
                response.append(1)
            else:
                response.append(0)
        restapi.submit_answer(response)

if task_name == 'blogger':
    with AiDevsRestapiHelper(task_name) as restapi:
        js = restapi.get_task()
        response = []
        with OpenAiHelper() as oai:
            for text in js['blog']:
                text_message = [
                    {'role': 'system', 'content': """I'm a blogger. I'm writing about cooking. I'm helping write a blog.
                            I'm writing very short posts, only few words. All answers should be only in Polish language."""},
                    {'role': 'user', 'content': text}
                ]
                response.append(oai.chat_completion(text_message))
        restapi.submit_answer(response)
