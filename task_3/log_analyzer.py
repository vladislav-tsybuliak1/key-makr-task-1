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
