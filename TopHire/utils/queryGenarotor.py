import json
from typing import List

from django.http import HttpResponse

from utils.enums import db_query_generator
from utils.query_format import query_format


def generate_db_query(query: str, output_format, field_name):
    query = ' '.join(query.replace('(', '( ').replace(')', ' )').split()).replace('( ', '(').replace(' )', ')')
    query_list = []
    start_index = -1
    is_double_quote = False
    for i, each in enumerate(query):
        if each.isalpha() or each == "'":
            if start_index == -1:
                start_index = i
                if each == "'":
                    is_double_quote = True
            elif each == "'":
                query_list.append(query[start_index + 1: i])
                start_index = -1
                is_double_quote = False
        elif each == ' ' or each == ')':
            if is_double_quote:
                continue
            if start_index != -1:
                query_list.append(query[start_index: i])
                start_index = -1
            if each == ')':
                query_list.append(each)
        elif each == '(':
            query_list.append(each)
        else:
            return HttpResponse(json.dumps({'error': 'Invalid query'}),
                                content_type="application/json")
    if start_index != -1:
        last_index = len(query)
        query_list.append(query[start_index: last_index])
    query_conditions = query_condition_generator(query_list,
                                                 query_formater=query_format.get(output_format),
                                                 field_name=field_name)
    query = db_query_generator.get(output_format)
    return query(query_conditions)


def query_condition_generator(query_list: List, query_formater, field_name):
    length = len(query_list)
    query_list.insert(0, '(')
    query_list.insert(length + 1, ')')
    stack = ['(']
    index = 1
    while len(stack) != 1 or stack[0] == '(':
        if index < length and query_list[index] != ')':
            stack.append(query_list[index])
            index += 1
            continue
        index += 1
        temp = []
        val = stack.pop()
        while val != '(':
            temp.append(val)
            val = stack.pop()
        if temp:
            stack.append(query_formater(keywords=temp, field_name=field_name))
    return stack[0]
