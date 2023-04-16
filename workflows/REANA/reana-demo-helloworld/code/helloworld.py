# -*- coding: utf-8 -*-

"""REANA-Demo-HelloWorld is a minimal demonstration of REANA system."""

from __future__ import absolute_import, print_function

import argparse
import errno
import logging
import os
import sys
import time

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%dT%H:%M:%S')


def hello(inputfile="data/names.txt", outputfile="results/greetings.txt",
          sleeptime=0.0):
    """Say 'Hello' to given name and store the greeting to a file.

    Writes the greeting character by character. An optional waiting period
    between writing of each character can be specified.

    :param inputfile: The relative path to the file containing the names
        of the persons to greet.
    :param outputfile: The relative path to the file where greeting
        should be stored. Creates the file if it does not exist.
    :param sleeptime: A waiting period (in seconds) between writing
        characters of greeting.

    """
    # detect names to greet:
    names = []
    with open(inputfile, 'r') as f:
        for line in f.readlines():
            names.append(line.strip())

    # ensure output directory exists:
    # influenced by http://stackoverflow.com/a/12517490
    if not os.path.exists(os.path.dirname(outputfile)):
        try:
            os.makedirs(os.path.dirname(outputfile))
        except OSError as exc:  # guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    # write greetings:
    with open(outputfile, "at") as f:
        for name in names:
            message = "Hello " + name + "!\n"
            for char in message:
                f.write("{}".format(char))
                f.flush()
                time.sleep(sleeptime)
    f.close()
    return


if __name__ == '__main__':
    args = sys.argv[1:]

    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--inputfile",
                        help="Relative path to the file containing \
                                  the names of the persons to greet. \n \
                                  [default=data/names.txt]",
                        default="data/names.txt",
                        required=False)

    parser.add_argument("-o", "--outputfile",
                        help="Relative path to the file where greeting \
                                  should be stored. \n \
                                  [default=results/greetings.txt]",
                        default="results/greetings.txt",
                        required=False)

    parser.add_argument("-s", "--sleeptime",
                        help="Waiting period (in seconds) between \
                                  writing characters of greeting. \n \
                                  [default=1]",
                        default=1.0,
                        type=float,
                        required=False)

    parsed_args = parser.parse_args(args)

    logging.info("Parameters: inputfile={0} outputfile={1} sleeptime={2}"
                 .format(parsed_args.inputfile, parsed_args.outputfile,
                         parsed_args.sleeptime))

    hello(parsed_args.inputfile, parsed_args.outputfile, parsed_args.sleeptime)
