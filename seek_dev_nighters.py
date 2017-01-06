import datetime
import json
from collections import defaultdict

import pytz
import requests

URL = 'https://devman.org/api/challenges/solution_attempts'
START_TIME = datetime.time(00, 00)
END_TIME = datetime.time(4, 00)


def get_number_of_pages():
    request = requests.get(URL)
    num_pages = json.loads(request.text)['number_of_pages']
    return num_pages


def load_data(page):
    request_params = {"page": page}
    request = requests.get(URL, params=request_params)
    records = json.loads(request.text)['records']
    return records


def get_all_users_records_with_timestamp_data(num_pages):
    for page in range(1, num_pages + 1):
        records = load_data(page)
        for record in records:
            if record['timestamp']:
                yield {
                    'username': record['username'],
                    'timestamp': float(record['timestamp']),
                    'timezone': record['timezone'],
                }


def get_midnighters(users_attempts_data):
    midnighters = defaultdict(list)
    for user_data in users_attempts_data:
        username = user_data['username']
        user_timezone = pytz.timezone(user_data['timezone'])
        attempt_time = datetime.datetime.fromtimestamp(user_data['timestamp'], user_timezone)
        if START_TIME <= attempt_time.time() <= END_TIME:
            midnighters[username].append(attempt_time)
    return midnighters


def print_midnighters(midnighters):
    print("List of midnighters:")
    for username, attempts in midnighters.items():
        attempts_formatted = [attempt.strftime("%H:%M:%S %d.%m.%y") for attempt in attempts]
        print("Username: '{username}', Attempts:\n{attempts}\n".format(
            username=username,
            attempts="\n".join(attempts_formatted))
        )


if __name__ == '__main__':
    num_pages = get_number_of_pages()
    users_attempts_data = get_all_users_records_with_timestamp_data(num_pages)
    midnighters = get_midnighters(users_attempts_data)
    print_midnighters(midnighters)
