"""Service settings."""
import os

PREFIX = "OPSX_"


def parse_bool(text):
    value = text.strip().lower()
    if value in ("true", "1", "yes", "on"):
        return True
    if value in ("false", "0", "no", "off"):
        return False
    raise ValueError("not a boolean: " + text)


def load_config(env=None):
    env = os.environ if env is None else env
    return {
        "db_host": env.get(PREFIX + "DB_HOST", "localhost"),
        "db_port": int(env.get(PREFIX + "DB_PORT", 5432)),
        "debug": parse_bool(env[PREFIX + "DEBUG"]) if PREFIX + "DEBUG" in env else False,
    }
