import re
import json
import os

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "static/data/", "inverted_index.json")
index = json.load(open(json_url))
index = index[0]


def parse_query(query_string):
    operator_stack = []
    output = []
    operator_list = ['AND', 'OR', 'AND_NOT']

    query_string = re.sub('[(]', '( ', query_string)
    query_string = re.sub('[)]', ' )', query_string)

    query_tokens = query_string.split()

    query_tokens.insert(0, '(')
    query_tokens.append(')')

    for token in query_tokens:
        if token == '(':
            operator_stack.append(token)
        elif token in operator_list:
            operator_stack.append(token)
        elif token == ')':
            for i in range(len(operator_stack)):
                elem = operator_stack.pop()

                if elem == '(':
                    break
                else:
                    output.append(elem)
        else:
            output.append(token)

    return output


def evaluate_boolean_query(query_string):
    postfix_list = parse_query(query_string)
    operator_list = ['AND', 'OR', 'AND_NOT']
    operand_stack = []

    for token in postfix_list:
        if token in operator_list:
            term_one = operand_stack.pop()
            term_two = operand_stack.pop()

            if token == 'OR':
                operand_stack.append(evaluate_or(term_one, term_two))
            elif token == 'AND':
                operand_stack.append(evaluate_and(term_one, term_two))
            elif token == 'AND_NOT':
                operand_stack.append(evaluate_and_not(term_one, term_two))

        else:
            operand_stack.append(token)

    if bool(operand_stack):
        results = operand_stack.pop()
        results.sort(key=int)
    else:
        results = []

    return results


def evaluate_or(term_one, term_two):
    if type(term_one) is str:
        term_one_docs = search_term(term_one)
    else:
        term_one_docs = term_one

    if type(term_two) is str:
        term_two_docs = search_term(term_two)
    else:
        term_two_docs = term_two

    term_one_set = set(term_one_docs)
    term_two_set = set(term_two_docs)

    unique_term_two_results = term_two_set - term_one_set

    union_lists = term_one_docs + list(unique_term_two_results)

    return union_lists


def evaluate_and(term_one, term_two):
    if type(term_one) is str:
        term_one_docs = search_term(term_one)
    else:
        term_one_docs = term_one

    if type(term_two) is str:
        term_two_docs = search_term(term_two)
    else:
        term_two_docs = term_two

    term_one_set = set(term_one_docs)
    term_two_set = set(term_two_docs)

    set_intersection = term_one_set.intersection(term_two_set)

    return list(set_intersection)


def evaluate_and_not(term_one, term_two):
    if type(term_one) is str:
        term_one_docs = search_term(term_one)
    else:
        term_one_docs = term_one

    if type(term_two) is str:
        term_two_docs = search_term(term_two)
    else:
        term_two_docs = term_two

    term_one_set = set(term_one_docs)
    term_two_set = set(term_two_docs)

    set_difference = term_two_set - term_one_set

    return list(set_difference)


def search_term(term):
    doc_ids = []

    if term in index.keys():
        documents = index[term]['Postings']

        for doc in documents:
            doc_ids.append(doc['DocID'])

    return doc_ids

