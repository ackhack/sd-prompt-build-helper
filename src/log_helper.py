from modules.shared import log
from .util import pbh_get_log_file_path
from datetime import datetime


def pbh_log_console(content):
    log.info("Prompt Build Helper: " + content)


def pbh_log_debug(content):
    log.debug("Prompt Build Helper: " + content)


def pbh_log_exception(e: Exception):
    pbh_log_console(str(e))
    pbh_log_file("Error: " + str(e))


def pbh_log_prompt(prompt: str):
    pbh_log_file("Prompt: " + prompt)


def pbh_log_file(content: str):
    with open(pbh_get_log_file_path(), 'a') as f:
        f.write(str(datetime.now()) + " | " + content + "\n")
