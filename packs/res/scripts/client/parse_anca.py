# -*- coding: utf-8 -*-
import os
import string

RES_PATH = r"F:\SO\SO\packs\res"

def extract_strings(filepath):
    with open(filepath, "rb") as f:
        data = f.read()
    strings = set()
    current = []
    for byte in data:
        if 32 <= byte <= 126 and chr(byte) in string.printable:
            current.append(chr(byte))
        else:
            if len(current) >= 4:
                strings.add(''.join(current))
            current = []
    if len(current) >= 4:
        strings.add(''.join(current))
    return strings

def main():
    for base in ["characters/npc", "characters/creatures"]:
        base_path = os.path.join(RES_PATH, base)
        if not os.path.isdir(base_path):
            continue
        for root, dirs, files in os.walk(base_path):
            for f in files:
                if f.endswith(".anca"):
                    full_path = os.path.join(root, f)
                    strings = extract_strings(full_path)
                    actions = [s for s in strings if s and s[0].isupper() and len(s) < 30]
                    if actions:
                        print "\n[%s]" % full_path
                        for act in sorted(actions):
                            print "   ", act

if __name__ == "__main__":
    main()