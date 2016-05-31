#!/bin/bash
# Python runner & wallpaper changer

/Library/Frameworks/Python.framework/Versions/3.4/bin/python3 wallscraper.py wallpapers

osascript changewallpaper.scpt

killall Dock

open wallpapers