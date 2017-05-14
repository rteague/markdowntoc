#!/bin/python

# mark down table of contents generator

import re, argparse, sys, collections

def readfile(path):
    contents = None
    try:
        fp = open(path, 'r')
        try:
            contents = fp.readlines()
        except Exception, e:
            print e
        finally:
            fp.close()
    except IOError, e:
        print e
    return contents

class MDTOC(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        # table of contents (toc)
        self.toc = None
        self.buildtoc(readfile(self.path[0]))
    
    def __str__(self):
       return self.toc
    
    def is_section(self, s):
        """ returns None if failed match else, the MatchObject
        """
        regex_str  = "^(#{1,6})(?!#)([^\n]*)$"
        # section regex, section name extracted from the data
        sect_regex = re.compile(regex_str)
        return sect_regex.match(s)
    
    def buildtoc(self, data):
        """ data is a list type
        """
        root = 1 if self.root is None else self.root[0]
        prev_sect_header = root
        prev_indent = 0
        indent = 0
        sections = list()
        data_size = len(data)
        if data_size > 0:
            self.toc = ''
        for i in range(data_size):
            if data[i] == "\n": continue
            sect = self.is_section(data[i])
            if sect:
                sect_name = sect.group(2).strip()
                sect_header = len(sect.group(1)) 
                if sect_header < root: continue
                if sect_header == root:
                    indent = 0
                elif sect_header == prev_sect_header:
                    indent = prev_indent
                elif sect_header > prev_sect_header:
                    indent = prev_indent + 1
                elif sect_header < prev_sect_header:
                    indent = 1
                    i = len(sections) - 1
                    while i >= 0:
                        if sect_header == sections[i]['header']:
                            indent = sections[i]['indent']
                            break
                        if sect_header > sections[i]['header']:
                            indent = sections[i]['indent'] + 1
                            break
                        i = i - 1
                indent_str = ".."*indent
                sections.append({'indent': indent, 'header': sect_header})
                anchor = sect_name.replace(' ','-').lower()
                anchor = re.sub(r"[^-a-z0-9_]", "", anchor)
                self.toc = "%s%s* [%s](#%s)\n" % (self.toc, indent_str, sect_name, anchor)
                prev_sect_header = sect_header
                prev_indent = indent

def main():
    class arg_namespace():pass
    argn = arg_namespace() 
    parser = argparse.ArgumentParser(
        description = 'Generates a table of contents section for your *.md files',
        epilog = 'by Rashaud Teague'
    )
    parser.add_argument('--root', nargs = 1, type = int, help = 'the starting depth, example 2 = ##')
    parser.add_argument('path', nargs = 1)
    parser.parse_args(namespace = argn)
    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    
    kwargs = vars(argn)
    toc = MDTOC(**kwargs)
    print toc

if __name__ == '__main__':
    main()


