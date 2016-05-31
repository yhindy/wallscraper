#!/usr/bin/env python3 -tt
"""
File: wallscraper.py
--------------------
Assignment 3: Wallscraper
Course: CS 41
Name: <Yousef Hindy>
SUNet: <yhindy>

This program downloads one page of pictures from any subreddit
given to it from the command line. It makes use of the requests
third party library to query Reddit for the data.

Extensions:
1. ability to specify subreddit in the command line
2. Wallpapers are not downloaded twice if they already exist

"""

import wallscraperutils as utils
from fractions import Fraction
import os
import sys
import requests
import shutil


class RedditPost:
    """
    This class abstracts a reddit post into its component parts.
    It has a title, url, is_self field, score, id, and field "isalbum"
    For pictures, it also keeps track of the width, height, and
    aspect ratio of the image.

    It also defines functionality for downloading a certain post
    and finding where in the local directory the picture should be placed.

    Finally, it has a string representation of itself.

    Probably should have made a separate class for RedditImagePost
    that inherits from this class, but I did not have time to do that.
    """

    def __init__(self, data):
        """
        This init method sets the data fields outlined above
        for the redditpost.
        """
        self.title = data['title']  # TODO convert title to something better
        self.url = data['url']
        self.is_self = data['is_self']
        try:
            self.width = data['preview']['images'][0]['source']['width']
            self.height = data['preview']['images'][0]['source']['height']
            self.aspectratio = Fraction(self.width, self.height)
            self.ispic = True

        except KeyError:
            self.ispic = False
            pass
        self.isalbum = (data['media_embed'] != {})
        self.score = data['score']
        self.id = data['id']
        pass

    def download(self):
        """
        This method takes a RedditPost object and downloads the
        image behind it if possible. It does not yet know how to
        download albums or images that aren't .jpg or .png
        """
        if self.is_self:
            return
        if self.isalbum:
            print("Dont know how to download albums yet!!!")
            return
        if self.url[-3:] != 'jpg' or self.url[-3:] != 'png':
            self.url = self.url + ".jpg"
        if self.ispic:
            pathname = self.findPath()
        else:
            pathname = 'wallpapers/unknown/'
        finalpath = pathname + self.id + '.' + self.url[-3:]
        if os.path.isfile(finalpath):
            return
        r = requests.get(self.url, headers={
                         'User-Agent': 'Wallscraper Script by yhindy'})

        if r.ok:
            if not os.path.exists(pathname):
                os.makedirs(pathname)
            with open(finalpath, 'wb') as f:
                for chunk in r:
                    f.write(chunk)
        pass

    def findPath(self):
        """
        This method returns where in the local directory the
        image should be stored. Images are stored as "{id}.{imagetype}"
        """
        pathname = '/Users/yhindy/Google Drive/Freshman Year/Spring/CS41/python-assignments/assign3/wallpapers/'
        pathname = pathname + \
            str(self.aspectratio.numerator) + 'x' + \
            str(self.aspectratio.denominator) + "/"
        pathname = pathname + str(self.width) + 'x' + str(self.height) + '/'
        return pathname

    def __str__(self):
        """
        Returns a string representation of a post

        e.g. "Funny Cat Photo (5000): http://i.imgur.com/rcuIpt4.jpg?1"
        """
        return self.title + " (" + str(self.score) + "): " + self.url


def findBest(posts):
    """
    This function takes in a list of RedditPost objects and returns the one with
    the most upvotes
    """
    posts = [post for post in posts if not post.isalbum or not post.is_self]
    bestpost = max(posts, key=lambda p: p.score)
    return bestpost


def downloadBest(post):
    if os.path.exists('wallpapers/best'):
        shutil.rmtree(
            '/Users/yhindy/Google Drive/Freshman Year/Spring/CS41/python-assignments/assign3/wallpapers/best')
    if post.url[-3:] != 'jpg' or post.url[-3:] != 'png':
        post.url = post.url + ".jpg"
    pathname = '/Users/yhindy/Google Drive/Freshman Year/Spring/CS41/python-assignments/assign3/wallpapers/best/'
    finalpath = pathname + 'best.jpg'

    r = requests.get(post.url, headers={
                     'User-Agent': 'Wallscraper Script by yhindy'})

    if r.ok:
        if not os.path.exists(pathname):
            os.makedirs(pathname)
        with open(finalpath, 'wb') as f:
            for chunk in r:
                f.write(chunk)


def main():
    """
    Main method:

    Gets subredditjson data from the wallscraperutils query method and
    then goes through each one and downloads the post if possible.
    """
    if os.path.exists('/Users/yhindy/Google Drive/Freshman Year/Spring/CS41/python-assignments/assign3/wallpapers'):
        shutil.rmtree(
        '/Users/yhindy/Google Drive/Freshman Year/Spring/CS41/python-assignments/assign3/wallpapers')
    """ Since this script only runs once a week, 
    it should dump the old wallpapers and download new ones """
    subredditjson = utils.query(sys.argv[1])
    if subredditjson is not None:
        posts = [RedditPost(childdata.get('data'))
                 for childdata in subredditjson.get('children')]
        #for post in posts:
            #post.download()

        best = findBest(posts)
        downloadBest(best)

    pass

if __name__ == '__main__':
    main()
