import argparse
import collections
import logging
import os.path
import re
import sys


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(filename="log_analyzer.log", mode="a"),
        logging.StreamHandler(stream=sys.stdout),
    ],
)

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
    if not os.path.exists(log_file):
        logging.error(f"File '{log_file}' does not exist")
        return

    ip_counter = collections.Counter()
    status_counter = collections.Counter()
    total_size = 0
    logs_count = 0

    for log in parse_log(log_file):
        ip_counter[log["ip"]] += 1
        status_counter[log["status"]] += 1
        total_size += int(log["size"])
        logs_count += 1

    logging.info("Counting top 5 IP addresses with the most requests:")
    for ip, num in ip_counter.most_common(5):
        logging.info(f"{ip}: {num} requests")

    logging.info("Counting most frequent errors:")
    for status, num in status_counter.most_common(10):
        if status.startswith("4") or status.startswith("5"):
            logging.info(f"{status}: {num} occurrences")

    avg_size = total_size / logs_count if logs_count > 0 else 0
    logging.info(f"Average response size: {round(avg_size, 2)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze Nginx log files")
    parser.add_argument(
        "logfile",
        help="Path to the log file",
    )
    args = parser.parse_args()
    analyze_log(args.logfile)


if __name__ == "__main__":
    main()
