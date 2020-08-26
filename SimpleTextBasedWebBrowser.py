import sys
import os
import requests
from collections import deque
from bs4 import BeautifulSoup
from colorama import Fore


def is_url_valid(url_to_validate):
    if "." in url_to_validate:
        return True

    return False


def open_file(file_name):
    if os.path.isfile(file_name):
        fh = open(file_name)
        file_contents = fh.read()

        return file_contents

    return "Error"


def save_file(path, content):
    fh = open(path, "w")
    fh.write(content)


args = sys.argv
directory = args[1]

if not os.path.isdir(directory):
    os.mkdir(directory)

url_stack = deque()

current = ""
url = input()
while url != "exit":
    if url == "back":
        if len(url_stack) != 0:
            url_content = open_file(url_stack.pop())

            print(url_content)
    else:
        if not is_url_valid(url):
            url_content = open_file(directory + "\\" + url + ".txt")

            print(url_content)

            current = directory + "\\" + url + ".txt"
        else:
            url_stack.append(current)

            if "https://" not in url:
                url = "https://" + url

            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'html.parser')

            tags = []
            for tag in soup.find_all(["p", "a", "ul", "ol", "li"]):
                if tag.name == "a":
                    tags.append(Fore.BLUE + tag.text)
                else:
                    tags.append(tag.text)

            text_content = "\n".join(tags)

            print(text_content)

            txt_path = "\\" + directory + url.replace("https://", "") + ".txt"
            save_file(directory + txt_path, text_content)

            current = txt_path

    url = input()
