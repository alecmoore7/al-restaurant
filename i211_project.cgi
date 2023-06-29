#!/usr/local/bin/python3

from wsgiref.handlers import CGHandler
import sys

sys.path.append("i211_project")

from i211_project import app

if __name__ == "__main__":
    CGIHandler().run(app.app)
