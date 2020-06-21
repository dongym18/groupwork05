#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Collect data"""

__author__ = "YanHaoqiu"
__copyright__ = "Copyright2020,Group05 Final_Project"
__license__ = "GPL"
__version__ = "3.2"
__maintainer__ = ["YanHaoqiu", "YeYinru"]

import re
import pandas as pd
import time
from subprocess import Popen, PIPE
import unicodedata


class StableFiles(object):
    """"Query files in linux-stable, and get its metric data.
    --Parameter--
    file_name: Files’ relative path in linux-stable.git
    lines: Files’ lines, which does include blanks lines
    Authors: the number of persons who wrote these lines of the files, from v3.0 to now
    Shas: the number of shas, among the existing lines of files, from v3.0 to now
    the_first_time: the earliest time of commits,
                    among the existing lines of files, from v3.0 to now
    the_last_time: the latest time of commits,
                    among the existing lines of files, from v3.0 to now
    average_date: the average time of commits,
                    among the existing lines of files, from v3.0 to now
    total_shas: the total number of commits, from v3.0 to now
    last_fixes: the latest shas of commit with “Fixes: SHA (text)" line
    fixes_percent: the proportion of commit with “Fixes: SHA (text)" line
                    against the total commit starting with “commit:”

    >>> repo = 'C:/Users/admin/Desktop/linux-stable'
    >>> kernelRange = 'v3.0..HEAD'
    >>> file_path = "arch/arm/mach-iop32x/gpio-iop32x.h"
    >>> file = StableFiles(file_path, kernelRange, repo)
    >>> file.repo
    C:/Users/admin/Desktop/linux-stable
    >>> file.fileName
    arch/arm/mach-iop32x/gpio-iop32x.h
    >>> a = file.blame()
    >>> a.head(3)
        sha	author	time_str
    0	b24413180f560	Greg Kroah-Hartman	2017-11-01 15:07:57
    1	7b85b867b9904	Linus Walleij	2013-09-09 16:39:51
    2	e34ca9de0b357	Linus Walleij	2013-09-09 16:59:54
    >>> file.df_blame.head(3)
            sha	author	time_str
    0	b24413180f560	Greg Kroah-Hartman	2017-11-01 15:07:57
    1	7b85b867b9904	Linus Walleij	2013-09-09 16:39:51
    2	e34ca9de0b357	Linus Walleij	2013-09-09 16:59:54
   """
    def __init__(self, file_path, kernelRange, repo):
        self.fileName = file_path
        self.kernelRange = kernelRange
        self.repo = repo
        self.df_blame = self.blame()
        self.the_first_time, self.the_last_time, self.average_date,self.clean_df = self.count_avetime()
        self.lines = self.count_lines()
        self.authors = self.count_author()
        self.shas = self.count_commit()
        self.fixes_percent, self.total_shas, self.last_fixes = self.gitFixCommits()

    def blame(self):
        """Query 'git blame --no-merges kernelRange fileName',
        extract shas, authors, and time_str.
         """
        cmd = ["git", "blame", "--no-merges", self.kernelRange, self.fileName]
        p = Popen(cmd, cwd=self.repo, stdout=PIPE)
        data, res = p.communicate()
        records = []  # collect data line by line
        for line in data.decode("utf-8").split("\n"):
            if line:  # ignore the last blank line
                row = line.split(")", 1)[0]
                parts = row.split(" ")
                parts = [i for i in parts if i != '']
                sha = parts[0]
                try:
                    # when blame'result includes time
                    first_name = parts[2].split('(')[1]
                    if parts[3] != [parts[-4]]:
                        last_name = ' '.join(parts[3:-4])
                    else:
                        last_name = ''
                except IndexError:
                    # when blame'result does not include time
                    first_name = parts[1].split('(')[1]
                    try:
                        if parts[2] != [parts[-4]]:
                            last_name = ' '.join(parts[2:-4])
                        else:
                            last_name = ''
                    except IndexError:
                        continue
                author = ' '.join([first_name, last_name])
                time_str = ' '.join([parts[-4], parts[-3]])
                record = [sha, author.rstrip(), time_str]
                records.append(record)
        return pd.DataFrame(records, columns=['sha', 'author', 'time_str'])

    def gitFixCommits(self):
        """Query 'git log -p --np-merges --date-order kernelRange fileName',
        search for lines which starts with 'commit: ' or 'Fixes: '.
        """
        commit = re.compile('^commit [0-9a-z]{40}$', re.IGNORECASE)
        fixes = re.compile('^\W+Fixes: [a-f0-9]{8,40} \(.*\)$', re.IGNORECASE)
        nr_fixes = 0  # count Fixes commits
        total_commits = 0  # count total commits
        cmd = ["git", "log", "-p", "--no-merges", "--date-order", self.kernelRange, self.fileName]
        p = Popen(cmd, cwd=self.repo, stdout=PIPE)
        data, res = p.communicate()
        # clean and normalize the data, ignore bad data
        data = unicodedata.normalize(u'NFKD', data.decode(encoding="utf-8", errors="ignore"))
        tag = 1
        last_fixes = None
        for line in data.split("\n"):
            if commit.match(line):
                cur_commit = line
                total_commits += 1
            if fixes.match(line):
                if tag:
                    last_fixes = cur_commit[7:19]  # extract shas
                    tag = 0
                    print("last_fixes", last_fixes)
                nr_fixes += 1
        try:
            # some files may have no commit in kernelRange
            fixes_percent = (nr_fixes / total_commits) * 100
        except ZeroDivisionError:
            fixes_percent = 0
        return fixes_percent, total_commits, last_fixes

    def count_author(self):
        """Count the number of different authors who committed."""
        authors = self.clean_df['author'].drop_duplicates().values.tolist()
        return len(authors)

    def count_commit(self):
        """Count the number of different shas."""
        commits = self.clean_df['sha'].drop_duplicates().values.tolist()
        return len(commits)

    def count_avetime(self):
        """Count the_first_time, the_last_time and the_average_time."""
        time_str = self.df_blame['time_str']
        time_num = []
        bad_time = []
        clean_df = self.df_blame
        for i in range(len(time_str)):
            try:
                # some lines may fail to convert into timestamps,
                # record and delete failed lines .
                value = time.mktime(time.strptime(time_str[i], '%Y-%m-%d %H:%M:%S'))
                time_num.append(value)
            except ValueError:
                clean_df = self.df_blame.drop(i, axis=0, inplace=False).reset_index(drop=True)
                bad_time.append(time_str[i])
                pass
        average_date = sum(time_num) / len(time_num)
        time_num = sorted(time_num)
        the_first_time = time_num[0]
        the_last_time = time_num[-1]
        list_save('BadTime.txt', bad_time)
        return the_first_time, the_last_time, average_date, clean_df

    def count_lines(self):
        return self.clean_df.shape[0]


def run(files, result_csv):
    """Main Function for Data Collection.
    --Parameter--
    files: query object
    result_csv: path to save collected data"""
    repo = 'C:/Users/admin/Desktop/linux-stable'
    kernelRange = "v3.0..HEAD"
    rows = []
    wrong_files = ['wrong files: ']
    try:  # save previous files data safely if any error happens.
        for file_path in files:
            print("File_path:\n", file_path)
            try:
                # some files may fail to extract data, for losing time or author
                file = StableFiles(file_path, kernelRange, repo)
            except ZeroDivisionError:
                wrong_files.append(file_path)  # record failed files
                continue
            row = {'file_name': file.fileName, 'lines': file.lines, 'authors': file.authors, 'shas': file.shas,
                   'the_first_time': file.the_first_time, 'the_last_time': file.the_last_time,
                   'average_date': file.average_date, 'total_shas': file.total_shas, 'last_fixes': file.last_fixes,
                   'fixes_percent': file.fixes_percent}
            rows.append(row)
            print("Row:\n", row)
    except Exception:
        file_info = pd.DataFrame(rows)
        file_info.head(20)
        file_info.to_csv(result_csv, header=True, index=True)
        list_save('BadTime.txt', wrong_files)
        print("Filtered lines are saved as BadTime.txt")
        raise
    file_info = pd.DataFrame(rows)
    file_info.head(20)
    file_info.to_csv(result_csv, header=True, index=True)
    list_save('BadTime.txt', wrong_files)
    print("Filtered lines are saved as BadTime.txt")


def list_save(filename, data):
    """Save a list as a csv file."""
    with open(filename, 'a') as fb:  # append write
        for i in range(len(data)):
            # delete '[' and ']' of a list in string form
            line = str(data[i]).replace('[', '').replace(']', '')
            # remove single quotes, commas,
            # and append line breaks at the end of each line
            line = line.replace("'", '').replace(',', '') + '\n'
            fb.write(line)


if __name__ == '__main__':
    result_csv = 'results.csv'
    files = ["arch/arm/mach-iop32x/gpio-iop32x.h", "arch/arm/mach-iop32x/Kconfig",
             "arch/nds32/kernel/signal.c", "arch/nds32/kernel/syscall_table.c"]
    run(files, result_csv)


