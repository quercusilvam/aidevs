#!/usr/bin/env python3

from restapi_helper import LangChainHelper
from langchain.schema import HumanMessage

print('==Simple message predict==')
with LangChainHelper() as lch:
    text = 'Hey there!'
    messages = [HumanMessage(content=text)]
    print(lch.predict_messages(messages))

print('==As English teacher - know the answer==')
with LangChainHelper() as lch:
    role = 'English teacher'
    text = 'What is a plural form of child?'
    print(lch.get_answer_as_role(role, text))

print('==As English teacher - does not know the answer==')
with LangChainHelper() as lch:
    role = 'English teacher'
    text = 'How old am I?'
    print(lch.get_answer_as_role(role, text))
