#!/usr/local/bin/python3

from wsgiref.handlers import CGIHandler
import sys

sys.path.append("i211_lecture")

from i211_lecture import app

if __name__ == "__main__":
    CGIHandler().run(app.app)
