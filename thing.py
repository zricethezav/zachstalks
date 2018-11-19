import sys
import os
import glob
import re
import random
from internetarchive import upload
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
    print('this might take a couple mins... uploading %s' % fn)
    os.rename(fn, 'ul.m4a')
    md = dict(title=fn[:-16], mediatype='audio')
    h = str(random.getrandbits(128))
    r = upload(h, files={fn: 'ul.m4a'}, metadata=md)
    return h

def clean(fn, h):
    if os.path.exists('README.md'):
        a_w = 'a'
    else:
        a_w = 'w'

    talks = open('README.md', a_w)
    print('give IA a couple mins for post processing: https://archive.org/details/%s ' % h)
    talks.write('\nhttps://archive.org/details/%s %s\n' % (h, fn[:-16]))
    talks.close()
    os.remove('ul.m4a')


if __name__ == '__main__':
    fn = dl()
    if fn is None:
        exit(1)
    clean(fn, ul(fn))

