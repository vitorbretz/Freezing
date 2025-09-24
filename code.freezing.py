import sys
import yaml

CONFIG_FILE = "config.yml"

def get_config(filename: str) -> dict:
    with open(filename) as f:
        return yaml.safe_load(f)

def unpack_config(config: dict) -> tuple:
    try:
        glass_breaker_group = config["glass_breaker_group"]
        freezing_dates = config["freezing_dates"]
    except KeyError:
        print(f"One of the keys was not found in the config file: {CONFIG_FILE}")
        sys.exit(1)
    return (glass_breaker_group, freezing_dates)


def main():
    config = get_config(CONFIG_FILE)
    glass_breaker_group, freezing_dates = unpack_config(config)

    print(glass_breaker_group)

if __name__ == "__main__":
    main()