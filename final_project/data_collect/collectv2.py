#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Collect data"""

import re
import pandas as pd
import time
from subprocess import Popen, PIPE
import unicodedata


def blame_one(kernelRange, fileName, repo):
    cmd = ["git", "blame", "--no-merges", kernelRange, fileName]
    p = Popen(cmd, cwd=repo, stdout=PIPE)
    data, res = p.communicate()
    records = []
    for line in data.decode("utf-8").split("\n"):
        if line:
            row = line.split(")",1)[0]
            parts = row.split(" ")
            parts = [i for i in parts if i != '']
            sha = parts[0]
            try:
                # blame的结果有日期时
                first_name = parts[2].split('(')[1]
                if parts[3] != [parts[-4]]:
                    last_name = ' '.join(parts[3:-4])
                else:
                    last_name = ''
            except IndexError:
                # blame的结果无日期时
                first_name = parts[1].split('(')[1]
                if parts[2] != [parts[-4]]:
                    last_name = ' '.join(parts[2:-4])
                else:
                    last_name = ''
            author = ' '.join([first_name, last_name])
            time_str = ' '.join([parts[-4],parts[-3]])
            record = [sha, author.rstrip(),time_str]
            records.append(record)
    print(records)
    return pd.DataFrame(records, columns=['sha', 'author', 'time_str'])


def blame_many(files):
    repo = 'C:/Users/admin/Desktop/linux-stable'
    kernelRange = "v3.0..HEAD"
    rows = []
    wrong_files = []
    for file_path in files:
        print("File_path:\n", file_path)
        df_blame = blame_one(kernelRange, file_path, repo)
        print("df_blame.head(10)", df_blame.head(10))
        try:
            the_first_time, the_last_time, average_date, clean_df = count_avetime(df_blame)  # Delete some lines.
        except ZeroDivisionError:
            wrong_files.append(file_path)
            continue
        lines = count_lines(clean_df)
        authors = count_author(clean_df)
        shas = count_commit(clean_df)
        fixes_percent, total_shas, last_fixes = gitFixCommits(kernelRange, repo, file_path)
        row = {'file_name': file_path, 'lines': lines, 'authors': authors, 'shas': shas,
               'the_first_time': the_first_time, 'the_last_time': the_last_time,
               'average_date': average_date, 'total_shas': total_shas, 'last_fixes': last_fixes,
               'fixes_percent': fixes_percent}
        rows.append(row)
        print("Row:\n", row)
    file_info = pd.DataFrame(rows)
    file_info.head(20)
    file_info.to_csv('results.csv', header=True, index=True)
    print("wrong_files:", wrong_files)



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


def gitFixCommits(kernelRange, repo, fileName):
    commit = re.compile('^commit [0-9a-z]{40}$', re.IGNORECASE)
    fixes = re.compile('^\W+Fixes: [a-f0-9]{8,40} \(.*\)$', re.IGNORECASE)
    nr_fixes = 0
    total_commits = 0
    cmd = ["git", "log", "-P", "--no-merges", "--date-order", kernelRange, fileName]
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
	if total_commits != 0:
		fixes_percent = (nr_fixes / total_commits) * 100
    else:
		print("last_fixes", last_fixes)
		fixes_percent = 0
    return fixes_percent, total_commits, last_fixes


if __name__ == '__main__':
    files = ["arch/arm/mach-iop32x/gpio-iop32x.h", "arch/arm/mach-iop32x/Kconfig",
             "arch/nds32/kernel/signal.c", "arch/nds32/kernel/syscall_table.c"]
    blame_many(files)


