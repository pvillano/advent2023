import sys

import requests


def submit(answer, day, level, year, auth_token):
    url = f"https://adventofcode.com/{year}/day/{day}/answer"
    data = {"level": level, "answer": answer}
    cookies = {"session": auth_token}
    response = requests.post(url=url, data=data, cookies=cookies)
    messages = [
        "That's the right answer!",
        "That's not the right answer.",
        "You don't seem to be solving the right level.  Did you already complete it?",
    ]
    for message in messages:
        if message in response.text:
            print(message)
            return
    print(response.text, file=sys.stderr)
