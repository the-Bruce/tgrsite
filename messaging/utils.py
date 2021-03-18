import re

from django.utils.html import strip_tags


def visible(value):
    text = value
    text = strip_tags(text)
    lines = text.splitlines()
    text = ""
    for i in lines:
        if len(i) > 0:
            if i[0] == "#":  # Uppercase headings
                i = i.upper()
                i = i.replace("#", "")
                if len(i) > 0 and i[0] == " ":
                    i = i[1:]
        text = text + i + '\r\n'
    text = text.replace("*", "")
    text = text.replace("`", "")
    # Yay! REGEX!!! I recommend regexr.com to work out what this means:
    text = re.sub(r"{[^{}\n\r]*}", "", text)  # Remove { blarg } attr blocks
    text = re.sub(r"!\[([^\]\[]*)\]\(([^()]*)\)", r"", text)  # Strip image links
    text = re.sub(r"\[([^\]\[]*)\]\(", r"\1: (", text)  # Convert square bracket links to colon
    text = re.sub(r"\\(.)", r"\1", text)  # Remove escaping from chars
    if len(text) > 2 and text[0:1] == "\r\n":
        text = text[2:]
    return text.strip()
