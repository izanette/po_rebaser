import string
import sys
import os
from string import Template
from po_msg import PoMsg, PoMsgs
import codecs

def print_po_msg(po_msg, out_file):
    for line in po_msg.prevcontext:
        out_file.write(line+'\n')
    for line in po_msg.msgid:
        out_file.write(line+'\n')
    for line in po_msg.msgstr:
        out_file.write(line+'\n')

def process(work_po_msgs, base_po_msgs, out_file):
    #for po_msg in work_po_msgs.array:
    #    print(po_msg)
    for po_msg in base_po_msgs.array:
        #print(po_msg)
        base_key = po_msg.get_key()
        if base_key in work_po_msgs.dict:
            work_po_msg = work_po_msgs.dict[base_key]
            print_po_msg(work_po_msg, out_file)

def open_file(filename, mode='r'):
    try:
        f = codecs.open(filename, mode, 'utf-8')
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

def is_empty_line(line):
    for i in range(len(line)):
        if line[i] != ' ' and line[i] != '\t':
            return False
    return True
def get_po_msgs(filename):
    result = PoMsgs()
    lines = get_lines(filename)

    buffer_prev_context = []
    buffer_msgid = []
    buffer_msgstr = []

    state = 0

    for idx in range(len(lines)):
        line = lines[idx]
        if state == 0:
            if line.startswith('msgid'):
                state = 1
            else:
                buffer_prev_context.append(line)
                continue

        if state == 1:
            if line.startswith('msgstr'):
                state = 2
            else:
                if is_empty_line(line):
                    continue
                else:
                    if line.startswith('msgid') or line.startswith('"'):
                        buffer_msgid.append(line)
                    else:
                        print(f'### ERROR 1 at line "{line}"')
                    continue

        if state == 2:
            if not line.startswith('msgstr') and not line.startswith('"'):
                state = 0
                po_msg = PoMsg(buffer_msgid, buffer_msgstr, buffer_prev_context)
                result.addPoMsg(po_msg)

                buffer_msgid = []
                buffer_msgstr = []
                buffer_prev_context = []
                if line.startswith('msgid'):
                    state = 1
                    buffer_msgid.append(line)
                elif line.startswith('msgstr'):
                    print(f'### ERROR 2 at line "{line}"')
                else:
                    state = 0
                    buffer_prev_context.append(line)
                continue
            else:
                buffer_msgstr.append(line)

    return result


def main(filename, base_filename, out_filename):
    work_po_msgs = get_po_msgs(filename)
    base_po_msgs = get_po_msgs(base_filename)
    process(work_po_msgs, base_po_msgs, open_file(out_filename, 'w'))

def stats(filename):
    po_msgs = get_po_msgs(filename)
    num_empty = 0
    for po_msg in po_msgs.array:
        msgstr = po_msg.join_lines(po_msg.msgstr)
        if len(msgstr) == 0:
            num_empty += 1
    num_total = len(po_msgs.array)
    perc = num_empty * 100.0 / num_total
    print(f'Num Strings: {num_total}')
    print(f'Num Done:    {num_total-num_empty} / {100-perc:.2f}%')
    print(f'Num Empty:   {num_empty} / {perc:.2f}%')


if __name__ == "__main__":
    if sys.argv[1] == "info":
        stats(sys.argv[2])
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
