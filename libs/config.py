import importlib
import inspect
import logging
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_PATH = (Path(__file__) / "../..").resolve()

CLOUDS_MODULE = "libs.clouds"
NOTIFIERS_MODULE = "libs.notifiers"

SLEEP = int(os.environ.get("SLEEP", "10"))

NOTIFY_NEW_INSTANCES = os.environ.get("NOTIFY_NEW_INSTANCES", "false") == "true"
NOTIFY_LOST_INSTANCES = os.environ.get("NOTIFY_LOST_INSTANCES", "false") == "true"

SLACK_TOKEN = os.environ.get("SLACK_TOKEN")
SLACK_CHANNEL = os.environ.get("SLACK_CHANNEL")
SLACK_USERNAME = os.environ.get("SLACK_USERNAME")


def retrieve_classes(module_dir, parent_class=None):
    """Function to retrieve all classes from the specified directory"""
    classes = []
    for file in (PROJECT_PATH / module_dir.replace(".", "/")).glob("*.py"):
        if file.name == "__init__.py":
            continue
        # Assuming 'libs' is at the root of your project and is recognized as a package
        module_name = f"{module_dir}.{file.stem}"
        module = importlib.import_module(module_name)
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if (
                parent_class
                and parent_class in [base.__name__ for base in obj.__bases__]
                and obj.__name__ is not parent_class
            ):
                classes.append(obj)
    return classes


CLOUDS = retrieve_classes(CLOUDS_MODULE, "Cloud")
NOTIFIERS = retrieve_classes(NOTIFIERS_MODULE, "Notifier")


class CustomColorFormatter(logging.Formatter):
    # Color codes : https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html
    white = "\u001b[38;5;250m"
    blue = "\u001b[38;5;67m"
    yellow = "\u001b[38;5;214m"
    red = "\u001b[38;5;160m"
    grey = "\u001b[38;5;243m"
    dark_grey = "\u001b[38;5;240m"
    bold_red = "\u001b[1m\u001b[38;5;160m"
    title = "\u001b[1m\u001b[7m"
    reset = "\u001b[0m"
    format_str = "[%(asctime)s] %(levelname)s (%(threadName)s) : %(name)s %(module)s.%(funcName)s :%(lineno)d - %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format_str + reset,
        logging.INFO: blue + format_str + reset,
        logging.WARNING: yellow + format_str + reset,
        logging.ERROR: red + format_str + reset,
        logging.CRITICAL: bold_red + format_str + reset,
    }

    def format(self, record, **args):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


root_logger = logging.getLogger()

if os.environ.get("LOGGING_LEVEL"):
    root_logger.setLevel(getattr(logging, os.environ["LOGGING_LEVEL"]))
else:
    root_logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setFormatter(CustomColorFormatter())

root_logger.addHandler(console_handler)

logging.getLogger("urllib3").setLevel(logging.WARNING)
