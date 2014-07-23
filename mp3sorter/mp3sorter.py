#!/usr/bin/env pythong
'''
Created on Jul 22 2014

@author: shireenrao
'''

import os
import sys
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import errno
import shutil


def create_dir_if_not_exist(path):
    """ Create the directory for given path if not exists """
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST:
            pass
        else:
            raise

if len(sys.argv) < 3:
    print 'Usage: %s <source dirname> <target dirname>' % sys.argv[0]
    exit()

print "Process dir %s" % sys.argv[1]
print "Target dir %s" % sys.argv[2]
dirname = sys.argv[1]
if not os.path.isdir(dirname):
    print '%s is not a valid source directory' % dirname
    exit(1)

targetdir = sys.argv[2]
create_dir_if_not_exist(targetdir)

abs_path = os.path.abspath(dirname)
files = []
for dirpath, dirnames, filenames in os.walk(abs_path):
    pathnames = [os.path.join(dirpath, name) for name in filenames]
    files.extend(pathnames)

print 'Total Files to process: %d' % len(files)
for mp3file in files:
    if 'mp3' in mp3file.lower():
        file_id3 = MP3(mp3file, ID3=EasyID3)
        album = file_id3['album'][0]
        # print album
        if album:
            targetalbumdir = os.path.join(targetdir, album)
            create_dir_if_not_exist(targetalbumdir)
            dest_file = os.path.join(targetalbumdir, os.path.basename(mp3file))
            if not os.path.isfile(dest_file):
                try: 
                    shutil.copy2(mp3file, targetalbumdir)
                    print "Processing '%s' to '%s'" % (mp3file, targetalbumdir)
                except OSError as exc:
                    print 'Error copying %s' % mp3file
                    pass






