#!/usr/bin/env python3

"""
requires Python3 and BeautifulSoup4

this script takes two arguments from the command line, a url and an html tag type, and returns all of the attributes
of the requested tag type from the given urls response content, if two arguments are not given at the command line
the script will ask the user to provide them at runtime
"""

import sys
import requests
from bs4 import BeautifulSoup


# get arguments that should have been passed via command line but were missing
def get_args(name, prompt):
    while True:
        temp_string = input(prompt)
        if len(temp_string) == 0:
            print("{} cannot be empty".format(name ))
            continue
        else:
            break
    return temp_string


# takes a URL as a string and gets the content from the given url and returns that content
def get_content(url):
    successful = False
    try:
        response = requests.get(url)
        if response.status_code == 200:
            page_content = BeautifulSoup(response.content, "html.parser")
            successful = True
        else:
            print("{} returned a status code {}, expected 200, please try another URL".format(url, response.status_code))
    except requests.exceptions.MissingSchema:
        print("URL malformed, please use 'http://www.____.com' format")
    if successful:
        return page_content
    else:
        exit("An error occurred, run the script again")


# takes the HTML of a web page and an HTML tag as inputs and returns all of the tags of the given type from the HTML
def get_tags(page_content, tag):
    tag_results = page_content.find_all(tag)
    if len(tag_results) > 0:
        return tag_results
    else:
        exit("no <{}> tags found, run the script again and try a different tag".format(tag))


# takes a list of tag objects and stores their HTML attributes and values as a dict stored in a list like: [{},{}...]
def create_list(tag_objs):
    temp_list = []
    for item in tag_objs:
        temp_list.append(item.attrs)
    return temp_list


# takes a list of dicts as input and returns a formatted string containing a visual representation of the data
def create_results(list_of_tags):
    results_as_string = ""
    for index, tag_dict in enumerate(list_of_tags):
        results_as_string = results_as_string + "Attributes in tag {}:\n".format(index+1)
        for key, value in tag_dict.items():
            results_as_string = results_as_string + "\t{} : {}\n".format(key, value)
    return results_as_string


# takes in a string as input and writes it to a file
def save_results(string):
    with open("output.txt", "w") as text_file:
        text_file.write(string)


# calls other functions
def main():
    if len(sys.argv) >= 3:
        url = sys.argv[1]
        tag = sys.argv[2]
    else:
        url = get_args("URL","Enter a URL (http://www.____.com):")
        tag = get_args("tag", "Enter a tag:")
    content = get_content(url)
    tags = get_tags(content, tag)
    tag_list = create_list(tags)
    results = create_results(tag_list)
    print(results)
    save_results(results)


# call main
main()
