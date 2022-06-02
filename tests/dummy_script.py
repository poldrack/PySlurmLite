# this dummy script does its own internal logging
# this is meant to test the slurm logging functions

import logging
import argparse
import sys
from brainsss2.logging_utils import setup_logging
import time


print('testing')

# set up fake args for logging
args = argparse.Namespace()
setattr(args, 'logdir', 'logs')
setattr(args, 'verbose', True)
args = setup_logging(args, 'dummy_script_test')
logging.info('testing logging within dummy script')
time.sleep(10)
