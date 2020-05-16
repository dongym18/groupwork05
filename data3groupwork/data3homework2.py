#!/usr/bin/env python3

'''
get fix commits can the number of fix commits of the version range.
'''

__copyright__ = 'T5,Lanzhou University,2020'
__license__ = 'GPLV2 or later'
__version__ = 1.0
__author__ = ['Yuming Dong Group05']

import re
import unicodedata
from matplotlib import pyplot as plt
from argparse import ArgumentParser
from subprocess import Popen, PIPE

class extract_meta_data:
    def __init__(self):
        parser = ArgumentParser(description='get extract number of fixes tag')
        parser.add_argument('reversion')
        parser.add_argument('kernelRange', type = str)
        parser.add_argument('repo', type = str)
        args = parser.parse_args()
        self.rev = args.reversion
        self.kernelRange = args.kernelRange
        self.repo = args.repo
        self.commit = re.compile('^commit [0-9a-z]{40}$', re.IGNORECASE)
        self.fixes  = re.compile('^\W+Fixes: [a-f0-9]{8,40} \(.*\)$', re.IGNORECASE)
        self.gitFixCommits()

    def gitFixCommits(self):
        nr_fixes = 0
        for i in range(1, int(self.kernelRange) + 1):
            cnt_fix = self.rev + '.' + str(i)
            cmd = ["git", "log", "-P", "--no-merges", cnt_fix]
            p = Popen(cmd, cwd=self.repo, stdout=PIPE)
            data, res = p.communicate()
            # we need to clean and normalize the data - note the errors ignore !by nicho
            data = unicodedata.normalize(u'NFKD', data.decode(encoding="utf-8", errors="ignore"))
            for line in data.split("\n"):
                if(self.commit.match(line)):
                    cur_commit = line
                if(self.fixes.match(line)):
                    # we have a fixes tag 
                    nr_fixes += 1
                    # just emit the two hashes - the secnd one is
                    # shortened to 7 == shortest fixes tag I found
                    print(cur_commit[7:19],",",line.strip()[9:16],sep="")
            with open('fix_commit', 'w') as f:
                f.write("total found fixes:" + str(nr_fixes))
            print("total found fixes:",nr_fixes)

if __name__ == '__main__':
    a = extract_meta_data()
    import doctest
    doctest.testmod()

