# -*- coding: utf-8 -*-

"""
Homework in git.pdf:
Call it from a subprocess writing the output to a pipe
Collect the output from the pipe
Arrange the output into a indexample data array
Write the entire record to a file
"""

__author__ = "Group5"
__copyright__ = "Copyright 2020 The SaveAsCSV Project"
__credits__ = "Group5"
__license__ = "GPL"
__version__ = "2.0"

from subprocess import Popen, PIPE
import csv


class QueryFile(object):
    def __init__(self, fileName, repo):
        self.fileName = fileName
        self.repo = repo
        self.answer = self.query()
        self.lines = None
        self.shas = None

    def query(self, kernelRange='v3.0..HEAD'):
        cmd = ["git", "-P", "log", "--stat", "--oneline", "--follow", kernelRange, self.fileName]
        p = Popen(cmd, cwd=self.repo, stdout=PIPE)
        data, res = p.communicate()
        return data.decode("utf-8").split("\n")

    def savecsv(self, save_path):
        with open(save_path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            # Instantiate a writer object to write data using the Writerow method.
            for i in range(int((len(self.answer) - 1) / 3)):  # traverse self.answer
                s1 = self.answer[3 * i].split(' ')  # get the first line of self.answer
                s2 = self.answer[3 * i + 1].split(' ')  # get the second line of self.answer。
                s3 = self.answer[3 * i + 2].split(' ')  # get the third line of self.answer
                row = [i + 1, s1[0], ' '.join(s1[1:]), s2[1], s3[4]]  # group together and number them
                # print(row)
                writer.writerow(row)  # write into a csv


if __name__ == '__main__':
    file = QueryFile("kernel/sched/core.c", r"C:\Users\admin\Desktop\linux-stable")
    file.query('v5.0..HEAD')
    file.savecsv('gitlog_answers.csv')
