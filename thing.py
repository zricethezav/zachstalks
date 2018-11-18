import sys
import os
from subprocess import Popen, PIPE

def dl():
    if len(sys.argv) != 2:
        print('give me a youtube url')
        return -1
    print('downloading ', sys.argv[1])
    cmd = 'youtube-dl -f \'bestaudio[ext=m4a]\' %s' % sys.argv[1]
    result = Popen(cmd, shell=True, stdout=PIPE)
    for line in result.stdout:
        if 'ffmpeg' in str(line): 
            file_name = str(line).split("Correcting container in ")[1][:-3]
            file_name = file_name.replace('\"', '')

    if file_name is None:
        print('bad download')
        return None
    os.rename(file_name, file_name.replace(' ', '_'))
    return file_name.replace(' ', '_')

def ul(fn):
    print(fn)
    cmd = 'ipfs add %s -Q' % fn
    result = Popen(cmd, shell=True, stdout=PIPE)
    for line in result.stdout:
        return line.decode('utf-8').replace('\n', '')

def clean(fn, h):
    if os.path.exists('TALKS.md'):
        a_w = 'a'
    else:
        a_w = 'w'

    talks = open('TALKS.md', a_w)
    talks.write('\nhttps://ipfs.io/ipfs/%s %s\n' % (h, fn))
    talks.close()
    os.remove(fn)


if __name__ == '__main__':
    fn = dl()
    if fn is None:
        exit(1)
    clean(fn, ul(fn))

