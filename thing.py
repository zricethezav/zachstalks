import sys
import os
import glob
import re
from subprocess import Popen, PIPE

def dl():
    if len(sys.argv) != 2:
        print('give me a youtube url')
        return -1
    print('downloading ', sys.argv[1])
    cmd = 'youtube-dl -f \'bestaudio[ext=m4a]\' %s' % sys.argv[1]
    p = Popen(cmd, shell=True, stdout=PIPE)
    p.wait()
    fs = glob.glob('*.m4a')
    if len(fs) == 0:
        print('bad download')
        return None
    return fs[0]

def ul(fn):
    os.rename(fn, 'ul.m4a')
    cmd = 'ipfs add %s -Q' % 'ul.m4a'
    result = Popen(cmd, shell=True, stdout=PIPE)
    for line in result.stdout:
        return line.decode('utf-8').replace('\n', '')

def clean(fn, h):
    if os.path.exists('README.md'):
        a_w = 'a'
    else:
        a_w = 'w'

    talks = open('README.md', a_w)
    talks.write('\nhttps://ipfs.io/ipfs/%s %s\n' % (h, fn[:-16]))
    talks.close()
    os.remove('ul.m4a')


if __name__ == '__main__':
    fn = dl()
    if fn is None:
        exit(1)
    clean(fn, ul(fn))

