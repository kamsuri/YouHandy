from __future__ import unicode_literals
import youtube_dl


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print "Done downloading"

def down(link):
	ydl_opts = {
	    'progress_hooks': [my_hook],
	}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
	    ydl.download([link])