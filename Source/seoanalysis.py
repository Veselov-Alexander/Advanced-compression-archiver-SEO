import sys
import os
import re
import math
from filemanager import FileManager
from collections import Counter

RESOURCES_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Resources")
DICTIONARY_PATH = os.path.join(RESOURCES_FOLDER, "dictionary.txt")
STOPWORDS_PATH = os.path.join(RESOURCES_FOLDER, "stopwords.txt")

def load_as_string(filename):
    dictionary = []
    with open(filename, "r") as file:
        for line in file:
            dictionary.append(line.lower().rstrip())
    return dictionary

def print_information(information):
    for parameter, value in information.items():
        if type(value) == float:
            print("{:50} | {:<.3f} %".format(parameter, value))
        else:
            print("{:50} | {}".format(parameter, value))
        
def split_to_words(text):
    inword_symbols = "-\'"
    words = Counter()
    for word in text.split():
        current_word = ""
        contains_letter = False
        for letter in word:
            if letter.isalpha() or (letter in inword_symbols and contains_letter):
                current_word += letter.lower()
                contains_letter = True
        if current_word:
            words[current_word] += 1

    return dict(words)

def split_dict(dictionary):
    parts = dict()
    for word in dictionary:
        first = word[0]
        if first not in parts:
            parts.update({first: []})
    for word in dictionary:
        parts[word[0]].append(word)
    return parts

def is_in_dict(dictparts, word_to_check):
    letter = word_to_check[0]
    if letter not in dictparts:
        return False
    dictionary = dictparts[letter]
    word_to_check = word_to_check.replace("-", " ")
    word_to_check = word_to_check.replace("\'", " ")
    for wordpart in word_to_check.split():
        if wordpart in dictionary:
            return True
        if len(wordpart) > 4:
            slicesize = 3
            for dictword in dictionary:
                if re.match("^" + wordpart[:-slicesize] + "*", dictword):
                    return True
    return False

def analyse(filename):
    print("SEO analysis: {}".format(filename))
    dictionary = split_dict(load_as_string(DICTIONARY_PATH))
    stopwords = load_as_string(STOPWORDS_PATH)

    text = FileManager.load_text(filename)
    words = split_to_words(text)
    words = dict(sorted(words.items(), key=lambda x: -x[1]))

    FORMAT = "\n\n{:51}| {:10}\n" + ("—" * 51) + "|" + ("—" * 10)

    print(FORMAT.format("Words", "Count")) 
    mostused = ("", 0)
    for word in words:
        if word not in stopwords:
            if words[word] > mostused[1]:
                mostused = (word, words[word])
            print("{:50} | {}".format(word, words[word]))

    print(FORMAT.format("Stop-words", "Count"))
    for word in words:
        if word in stopwords:
            print("{:50} | {}".format(word, words[word]))

    error_count = 0
    print(FORMAT.format("Grammatical errors (or unknown words)", "Count"))
    for word in words:
        if not is_in_dict(dictionary, word):
            error_count += 1
            print("{:50} | {}".format(word, words[word]))

    print(FORMAT.format("Statistics", "Value"))
    information = dict()
    information["Number of characters"] = sum([x.isprintable() for x in text])
    information["Number of characters without spaces"] = sum([not x.isspace() for x in text])
    information["Number of words"] = sum(words[x] for x in words)
    information["Number of unique words"] = len(set(words))
    information["Number of stop words"] = sum(words[x] if x in stopwords else 0 for x in words)
    information["Grammatical errors percent"] = error_count / information["Number of words"] * 100
    information["Water percent"] = information["Number of stop words"] / information["Number of words"] * 100
    information["Nausea percent"] = mostused[1] / information["Number of words"] * 100

    print_information(information)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Wrong parameters!")
        print("Example: py seoanalysis.py input.txt")
    else:
        analyse(sys.argv[1])