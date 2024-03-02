import string
import sys
import os
from string import Template
from po_msg import PoMsg, PoMsgs

def process(work_po_msgs, base_po_msgs):
    pass

def open_file(filename, mode='r'):
    try:
        f = open(filename, mode)
        return f
    except IOError:
        print('Could not open file: %s' % filename)
        sys.exit(1)

def get_lines(filename):
    result = []
    f = open_file(filename)
    result = f.read().splitlines()
    f.close()

    return result

def get_po_msgs(filename):
    lines = get_lines(filename)

    for line in lines:


def main(filename, base_filename):
    work_po_msgs = get_po_msgs(filename)
    base_po_msgs = get_po_msgs(base_filename)
    process(work_po_msgs, base_po_msgs)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
