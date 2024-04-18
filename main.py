import datetime as dt
import os
import time
import logging
import argparse
import croniter
import requests


def run(args):
    url = args.url
    output = args.output
    fmt = args.format

    if args.daemon:
        cron = croniter.croniter(args.daemon, dt.datetime.now())
        while True:
            next_time = cron.get_next(dt.datetime)
            logging.info(f"Next run at {next_time}")
            time.sleep((next_time - dt.datetime.now()).total_seconds())
            logging.info("Running...")
            _run(url, output, fmt)
    else:
        _run(url, output, fmt)


def _run(url, output, fmt):
    url = f"{url}&format={fmt}"
    logging.info(f"Downloading {url}")
    r = requests.get(url, auth=tuple(args.u.split(":")))
    r.raise_for_status()
    with open(output, "wb") as f:
        f.write(r.content)
    logging.info(f"Downloaded to {output}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="todoist export url")
    parser.add_argument("--format", help="output format", default="json_all")
    parser.add_argument("--output", help="output file", default="todoist.json")
    parser.add_argument("--daemon", help="run as daemon", default=None)
    parser.add_argument("-u", help="HTTP auth (format: user:password)",
                        default=None)

    args = parser.parse_args()

    run(args)
