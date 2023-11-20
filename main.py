#!/usr/bin/env python3
import argparse
from restapi_helper import OpenAiHelper
from restapi_helper import AiDevsRestapiHelper
from restapi_helper import OpenAiModerator
from restapi_helper import ModeratorValidationException
from simple_term_menu import TerminalMenu as TM


def main_menu():
    """Show menu options to user."""
    options = ['blogger', 'inprompt', 'moderation' ]
    function_map = {
        'blogger': solve_blogger,
        'inprompt': solve_inprompt,
        'moderation': solve_moderation
    }

    tm = TM(options)
    menu_entry_index = tm.show()
    user_input = options[menu_entry_index]
    print(f'You have selected {user_input}!')
    if user_input in function_map:
        function_map[user_input](user_input)


def solve_blogger(task_name):
    """Solve blogger task."""
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


def solve_moderation(task_name):
    """Solve moderation task."""
    with AiDevsRestapiHelper(task_name) as restapi:
        js = restapi.get_task()
        response = []
        with OpenAiHelper() as oai:
            for text in js['blog']:
                text_message = [
                    {'role': 'system', 'content': """I'm a blogger. I'm writing about cooking. I'm helping write a blog.
                            I'm writing very short posts, max two sentences. All answers should be only in Polish language."""},
                    {'role': 'user', 'content': text}
                ]
                response.append(oai.chat_completion(text_message))
        restapi.submit_answer(response)


def solve_inprompt(task_name):
    """Solve inprompt task.

    remember information about each person and then answer the question in POLISH."""

    with AiDevsRestapiHelper(task_name) as restapi:
        js = restapi.get_task(verbose=False)
        question = js['question']
        people = {}
        for i in js['input']:
            people.update({i.split()[0]: i})

        with OpenAiHelper() as oai:
            text_message = [
                {'role': 'system', 'content': f'''Return the name only from message'''},
                {'role': 'user', 'content': question}
            ]
            name = oai.chat_completion(text_message)
            print(name)
            text_message = [
                {'role': 'system', 'content': f'''Answer question below using only context and nothing else. Answer in
                Polish.
                ###Context
                {people[name]}'''},
                {'role': 'user', 'content': question}
            ]
            restapi.submit_answer(oai.chat_completion(text_message))


if __name__ == '__main__':
    main_menu()
