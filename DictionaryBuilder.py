import json
import re
import os


tokenized_documents = []

stopList = {'a': '', 'an': '', 'and': '', 'are': '', 'as': '', 'at': '', 'be': '', 'by': '', 'for': '', 'from': '',
            'has': '', 'in': '', 'is': '', 'it': '', 'its': '', 'of': '', 'on': '', 'that': '', 'the': '', 'to': '',
            'was': '', 'were': '', 'will': '', 'with': ''}


def tokenize_line(line):
    line = re.sub('[():;,]', '', line)
    line = re.sub('[/]', ' ', line)

    # Case-folding step
    line = line.lower()

    tokenized_line = line.split()

    return tokenized_line


def stopword_filter(tokens):
    for word in tokens.copy():
        try:
            if stopList[word] == '':
                del tokens[tokens.index(word)]
        except KeyError:
            continue

    return tokens


def normalize_tokens(tokens):
    for i in range(len(tokens)):
        tokens[i] = re.sub('[-\.]', '', tokens[i])

    return tokens


def porter_stem_tokens(tokens):
    for i in range(len(tokens)):
        if bool(re.search('sses\Z', tokens[i])):
            tokens[i] = re.sub('sses\Z', '', tokens[i])
        elif bool(re.search('ies\Z', tokens[i])):
            tokens[i] = re.sub('ies\Z', '', tokens[i])
        elif bool(re.search('ss\Z', tokens[i])):
            continue
        elif bool(re.search('s\Z', tokens[i])):
            tokens[i] = re.sub('s\Z', '', tokens[i])

    return tokens


def deduplicate(tokens):
    hashed_words = {}
    tokens.sort()

    for word in tokens:
        if word in hashed_words:
            hashed_words[word] += 1
        else:
            hashed_words[word] = 1

    return hashed_words


def create_dictionary(stop_flag, normalize_flag, stem_flag, documents):
    dictionary = []
    title_tokens = []
    body_tokens = []

    for key, value in documents[0].items():
        for i in range(2):
            if i == 0:
                token_line = tokenize_line(value['Title'])
            elif i == 1:
                token_line = tokenize_line(value['Body'])

            if stop_flag:
                token_line = stopword_filter(token_line)
            if normalize_flag:
                token_line = normalize_tokens(token_line)
            if stem_flag:
                token_line = porter_stem_tokens(token_line)

            if i == 0:
                title_tokens = token_line
            elif i == 1:
                body_tokens = token_line

            dictionary.extend(token_line)

        tokenized_documents.append({'DocID': key, 'Title': title_tokens, 'Body': body_tokens})

    deduplicated_dict = deduplicate(dictionary)

    return deduplicated_dict

