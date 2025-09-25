import datetime
import sys
import os
import logging
import yaml

CONFIG_FILE = "config.yml"
GITLAB_USER_LOGIN = os.getenv("GITLAB_USER_LOGIN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    level=logging.INFO
)

def get_config(filename: str) -> dict:
    with open(filename) as f:
        return yaml.safe_load(f)

def unpack_config(config: dict) -> tuple:
    try:
        glass_breaker_group = config["glass_breaker_group"]
        freezing_dates = config["freezing_dates"]
    except KeyError:
        logging.error(f"One of the keys was not found in the config file: {CONFIG_FILE}")
        sys.exit(1)
    return (glass_breaker_group, freezing_dates)


def is_user_logged_in(username: str, glass_breaker_group:list) -> bool:
    return username in glass_breaker_group

def is_today_within_freezing_dates(date_from: datetime.date, date_to: datetime.date) -> bool:
    date_today = datetime.date.today()
    return date_from <= date_today <= date_to

def main():
    config = get_config(CONFIG_FILE)
    glass_breaker_group, freezing_dates = unpack_config(config)

    if is_user_logged_in(GITLAB_USER_LOGIN, glass_breaker_group):
        logging.info(f"User {GITLAB_USER_LOGIN} logged in")
        sys.exit(0)
    else:
        for period, date in freezing_dates.items():

            date_from = date.get("from")
            date_to = date.get("to")
            logging.info(f"Validating period {period} that goes from {date_from} to {date_to}")
            if is_today_within_freezing_dates(date_from, date_to):
                logging.warning(f"The date current falls under {period}, blocked due to blockout period")
                sys.exit(1)

if __name__ == "__main__":
    main()