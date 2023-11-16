#!/usr/bin/env python3
import argparse
from restapi_helper import AiDevsRestapiHelper

parser = argparse.ArgumentParser(description='Solve first task')
parser.add_argument('-t', '--taskname', help='The task_name', required=True)
args = parser.parse_args()

task_name = args.taskname

with AiDevsRestapiHelper(task_name) as restapi:
    js = restapi.get_task()
    restapi.submit_answer(js['cookie'])
