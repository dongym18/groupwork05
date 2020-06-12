#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Collect data"""

import re
import pandas as pd
import time
from subprocess import Popen, PIPE
import unicodedata


def blame_one(kernelRange, fileName, repo, columns):
    cmd = ["git", "blame", kernelRange, fileName]
    p = Popen(cmd, cwd=repo, stdout=PIPE)
    data, res = p.communicate()
    sha_head = columns[0]
    sha_tail = columns[1]
    author_head = columns[2]
    author_tail = columns[3]
    time_head = columns[4]
    time_tail = columns[5]
    rows = [[line[sha_head:sha_tail], line[author_head:author_tail].rstrip(),
             line[time_head:time_tail]] for line in data.decode("utf-8").split("\n") if line]
    return pd.DataFrame(rows, columns=['sha', 'author', 'time_str'])


def blame_many(files_columns):
    repo = 'C:/Users/admin/Desktop/linux-stable'
    kernelRange = "v3.0..HEAD"
    rows = []
    for file_path, columns in files_columns.items():
        print("File_path:\n", file_path)
        df_blame = blame_one(kernelRange, file_path, repo, columns)
        print("df_blame.head(10)", df_blame.head(10))
        the_first_time, the_last_time, average_date, clean_df = count_avetime(df_blame)  # Delete some lines.
        lines = count_lines(clean_df)
        authors = count_author(clean_df)
        shas = count_commit(clean_df)
        fixes_percent, total_shas, last_fixes = gitFixCommits(kernelRange, repo)
        row = {'file_name': file_path, 'lines': lines, 'authors': authors, 'shas': shas,
               'the_first_time': the_first_time, 'the_last_time': the_last_time,
               'average_date': average_date, 'fixes_percent': fixes_percent,
               'total_shas': total_shas, 'last_fixes': last_fixes}
        rows.append(row)
        print("Rows:\n", rows)
    file_info = pd.DataFrame(rows)
    file_info.head(20)
    file_info.to_csv('results.csv', header=True, index=True)



def count_author(df):
    authors = df['author'].drop_duplicates().values.tolist()
    return len(authors)


def count_commit(df):
    commits = df['sha'].drop_duplicates().values.tolist()
    return len(commits)


def count_avetime(df):
    time_str = df['time_str']
    time_num = []
    bad_time = []
    clean_df = df
    for i in range(len(time_str)):
        try:
            value = time.mktime(time.strptime(time_str[i], '%Y-%m-%d %H:%M:%S'))
            time_num.append(value)

        except ValueError:
            clean_df = df.drop(i, axis=0, inplace=False).reset_index(drop=True)
            bad_time.append(time_str[i])
            pass
    average_date = sum(time_num) / len(time_num)
    time_num = sorted(time_num)
    the_first_time = time_num[0]
    the_last_time = time_num[-1]
    list_save('BadTime.txt', bad_time)
    return the_first_time, the_last_time, average_date, clean_df


def count_lines(df):
    return df.shape[0]


def list_save(filename, data):  # filename为写入CSV文件的路径，data为要写入数据列表.
    with open(filename, 'a') as fb:  # 追加写
        for i in range(len(data)):
            line = str(data[i]).replace('[', '').replace(']', '')  # 去除[],这两行按数据不同，可以选择
            line = line.replace("'", '').replace(',', '') + '\n'  # 去除单引号，逗号，每行末尾追加换行符
            fb.write(line)
    print("Filtered lines are saved as BadTime.txt")


def gitFixCommits(kernelRange, repo):
    commit = re.compile('^commit [0-9a-z]{40}$', re.IGNORECASE)
    fixes = re.compile('^\W+Fixes: [a-f0-9]{8,40} \(.*\)$', re.IGNORECASE)
    nr_fixes = 0
    total_commits = 0
    cmd = ["git", "log", "-P", "--no-merges", "--date-order", kernelRange]
    p = Popen(cmd, cwd=repo, stdout=PIPE)
    data, res = p.communicate()
    # we need to clean and normalize the data - note the errors ignore !
    data = unicodedata.normalize(u'NFKD', data.decode(encoding="utf-8", errors="ignore"))
    tag = 1
    last_fixes = None
    for line in data.split("\n"):
        if commit.match(line):
            cur_commit = line
            total_commits += 1
        if fixes.match(line):
            if tag:
                last_fixes = cur_commit[7:19]
                tag = 0
                print("last_fixes", last_fixes)
            nr_fixes += 1
    fixes_percent = (nr_fixes / total_commits) * 100
    return fixes_percent, total_commits, last_fixes


if __name__ == '__main__':
    files_columns = {"kernel/sched/autogroup.c": [0, 13, 41, 60, 60, 79],
                     "kernel/sched/core.c": [0, 13, 35, 62, 62, 81]}
    blame_many(files_columns)


