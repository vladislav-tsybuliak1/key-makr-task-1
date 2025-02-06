import collections
import re

LOG_PATTERN = re.compile(
    r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - \[(?P<datetime>.*?)] "(?P<method>\w+) (?P<url>.*?) (?P<protocol>HTTP/\d\.\d)" (?P<status>\d+) (?P<size>\d+)'
)


def parse_log(file_path):
    with open(file_path, "r") as file:
        for line in file:
            match = LOG_PATTERN.match(line)
            if match:
                yield match.groupdict()


def analyze_log(log_file):
    ip_counter = collections.Counter()
    status_counter = collections.Counter()
    total_size = 0
    logs_count = 0

    for log in parse_log(log_file):
        ip_counter[log["ip"]] += 1
        status_counter[log["status"]] += 1
        total_size += int(log["size"])
        logs_count += 1
