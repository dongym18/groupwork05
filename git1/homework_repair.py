#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Here is homework in git.pdf.
Requirements:
Store data catched from homework.py as a csv file."""

__author__ = "YanHaoqiu"
__copyright__ = "Copyright2020,Group05 homework"
__license__ = "GPL"
__version__ = "1.2"
__maintainer__ = ["YanHaoqiu", "ZhangQiyuan"]


# References
# https://www.cnblogs.com/shmily2018/p/11592448.html
# pandas: https://www.jianshu.com/p/1df90420e45c  https://www.jianshu.com/p/6e35d37e7709

import argparse
from re import findall
from subprocess import Popen, PIPE, DEVNULL


class GitCount(object):
    """Use git commands, ask command line and count.

    >>> gitcnt = "git rev-list --pretty=format:\"%ai\" v4.4...v4.4.1"
    >>> commit_count = GitCount(gitcnt)
    >>> print(commit_count.get_commit_cnt())
    69
    >>> gitbase = "git log -1 --pretty=format:\"%ct\" v4.4"
    >>> base_count = GitCount(gitbase)
    >>> base_time = base_count.get_base_rev()
    >>> print(base_time)
    1584309683
    >>> gittag = "git log -1 --pretty=format:\"%ct\" v4.4.1"
    >>> daytag_count = GitCount(gittag)
    >>> print(daytag_count.get_tag_days(base_time))
    -36123

    """
    def __init__(self, command):
        self.cmd = Popen(command, stdout=PIPE, stderr=DEVNULL, shell=True)

    def get_commit_cnt(self):
        """Count the commits based on the number of time stamps."""
        try:
            raw_counts = self.cmd.communicate()[0]
        except IndexError:
            raise IndexError("Wrong git commands")
        # if we request something that does not exist -> 0
        cnt = findall('[0-9]*-[0-9]*-[0-9]*', str(raw_counts))
        return len(cnt)

    def get_tag_days(self, base):
        """Count the interval between this version and the basic version."""
        SecPerHour = 3600
        try:
            seconds = self.cmd.communicate()[0]
        except IndexError:
            raise IndexError("Wrong git commands")
        # print("Second:{0}, Base:{1}".format(seconds, base))
        return (int(seconds) - base) // SecPerHour

    def get_base_rev(self):
        """Count the base time of the benchmark revision."""
        git_time = self.cmd.communicate()[0]
        # clear git_time, since git_time is b'1584309683v4.4'
        time = git_time.decode('UTF-8')
        return int(time)


def get_parser():
    """read arguments of command lines"""
    parser = argparse.ArgumentParser(description="get the commit count per sublevel pointwise or cumulative")
    parser.add_argument('--revision', required=True)
    parser.add_argument('--sublevel', default=5, type=int, help='how many sublevels you intend to count')
    parser.add_argument('--cumulative', default=0, choices=[0,1])
    return parser


def main():
    # get arguments from command line
    parser = get_parser()
    args = parser.parse_args()
    rev = args.revision
    rev_range = args.sublevel
    cumulative = args.cumulative

    print("#sublevel commits %s stable fixes" % rev)
    print("lv hour bugs")

    # get the basic revision as a benchmark in time counting
    gitbase = "git log -1 --pretty=format:\"%ct\" " + rev
    # gitbase = ['git log -1', '--pretty=format:\"%ct\"', rev]
    base_count = GitCount(gitbase)
    base_time = base_count.get_base_rev()

    # preparation for git-command data
    sl_list = []
    days_list = []
    commits_list = []

    # traverse sublevel revisions
    rev1 = rev
    for sl in range(1, rev_range + 1):
        rev2 = rev + "." + str(sl)
        # tag_range = rev1 + "..." + rev2
        gitcnt = "git rev-list --pretty=format:\"%ai\" " + rev1 + "..." + rev2
        # gitcnt = ['git rev-list', '--pretty=format:\"%ai\"', tag_range]
        # gittag = "git log -1 --pretty=format:\"%ct\" " + rev2
        gittag = "git log -1 --pretty=format:\"%ct\" " + rev2
        commit_count = GitCount(gitcnt)
        commits = commit_count.get_commit_cnt()
        if cumulative == 0:
            rev1 = rev2
        # if get back 0 then its an invalid revision number
        if commits:
            daytag_count = GitCount(gittag)
            days = daytag_count.get_tag_days(base_time)
            sl_list.append(sl)
            days_list.append(days)
            commits_list.append(commits)
            print("Recursion: %d %d %d" % (sl, days, commits))
        else:
            break

        # create a dataframe
        re = np.array([sl_list, days_list, commits_list])
        data = re.transpose()
        print(data)
        c = ["1v", "hour", "bugs"]
        df = pd.DataFrame(data=data, columns=c)

        # write in csv file
        data_file = 'data_v4.4'
        csv_data = data_file + ".csv"
        df.to_csv(csv_data)
# Output is
#    1v  hour  bugs
# 0  1   500   16
# 1  2   909   300
# 2  3   1509  460


if __name__ == '__main__':
    main()
