# logging utils

# pyright: reportMissingImports=false

import logging
import shlex
import subprocess
import argparse


def remove_existing_file_handlers():
    logger = logging.getLogger()
    saved_handlers = []
    for h in logger.handlers:
        if isinstance(h, logging.FileHandler):
            saved_handlers.append(h)
            logging.getLogger().removeHandler(h)
    return saved_handlers


def reinstate_file_handlers(saved_handlers):
    """
    Reinstate saved file handlers.

    Parameters:
    -----------
    saved_handlers: list
        list of saved file handlers
    """

    for h in list(set(saved_handlers)):
        logging.getLogger().addHandler(h)


# from https://stackoverflow.com/questions/21953835/run-subprocess-and-print-output-to-logging
def run_shell_command(command_line, verbose=False):
    command_line_args = shlex.split(command_line)

    if verbose:
        logging.info('Subprocess: "' + command_line + '"')

    try:
        command_line_process = subprocess.Popen(
            command_line_args,
            stdout=subprocess.PIPE,
            # stderr=subprocess.STDOUT,
        )

        process_output, _ = command_line_process.communicate()

        if verbose:
            logging.info(f'got line from subprocess: {process_output.decode("utf-8")}')
    except Exception as e:
        logging.error(f'Exception occured: {e}')
        return False
    else:
        # no exception was raised
        if verbose:
            logging.info('Subprocess finished')

    return process_output.decode("utf-8")


def dict_to_namespace(d):
    # convert dict to argparse.Namespace
    args = argparse.Namespace()
    for k, v in d.items():
        setattr(args, k, v)
    return args


def dict_to_args_list(d):
    # convert a dict to a set of command line args
    argslist = []
    for k, v in d.items():
        if isinstance(v, bool):
            if v:
                argslist.append(f"--{k}")
        elif isinstance(v, (int, float, str)):
            argslist.extend((f"--{k}", f"{v}"))
        elif isinstance(v, list):
            argslist.append(f"--{k}")
            argslist.extend(f"{vv}" for vv in v)
    return argslist
