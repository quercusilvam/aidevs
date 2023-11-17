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

if task_name == 'liar':
    with AiDevsRestapiHelper(task_name) as restapi:
        restapi.get_task()
        js = restapi.ask_question('What is capital of Poland')
        with OpenAiHelper() as oai:
            text_message = [
                {'role': 'system', 'content': '''Tell me if user answer correctly the question
                "What is the capitol of Poland".
                Return only YES or NO'''},
                {'role': 'user', 'content': js['answer']}
            ]
            restapi.submit_answer(oai.chat_completion(text_message))
