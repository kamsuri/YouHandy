from __future__ import unicode_literals
import youtube_dl
import os.path


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print d['filename']

def down(link):
    ydl_opts = {
    'progress_hooks': [my_hook],
    'outtmpl': 'downloads/%(title)s'
    }
    #link += " '-o', 'downloads/%(title)s.(ext)s"
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(link, download = False)
    if 'entries' in result  : 
    # in case it is a playlist
        video = result['entries'][0]
    else: 
        video = result
    for k, v in video.iteritems(): # print out the info
        if k == 'title':
            name = v
            print name
            status = os.path.isfile('downloads/'+name)
            print status
            if status == True:
                text = "Video %s already exists" % v
                return text

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])
    text = "Video %s downloaded successfully" % name
    return text
