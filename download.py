#! /usr/bin/env python
__author__ = 'cbn'


import cStringIO
import simplejson
import urllib
from PIL import Image
from redis import StrictRedis
from sys import argv
from os.path import abspath
import logging

logging.basicConfig(filename='logs/thumb-dl.log',level=logging.DEBUG)

def get_item_details(filename):
    filepath = abspath(filename)
    f = open(filepath)
    data = simplejson.loads(f.read())
    f.close()
    essentials = []
    for x in data:
        if x.get('object',None):
            essentials.extend([{
                'id'    : x['@id'],
                'thumb' : x['object'],
                'url'   : x['isShownAt'],
                'title' : x['originalRecord']['title']
            }])
    return essentials

def load_remote_image(url):
    try:
        file = cStringIO.StringIO(urllib.urlopen(url).read())
        return Image.open(file)
    except Exception as e:
        logging.debug("Error while trying to get thumbanil at %s".format(url))
        logging.debug(e)
        return False


def get_image_colors(image):
    if image.mode != "RGB":
        image = image.convert("RGB")

    size = image.size[0] * image.size[1]
    colors = image.getcolors(size)
    # calculate what percentage the color is of total image
    # and transform RGB value to hex.
    hex_colors = map(
        lambda color: (color[0] * 1.0 / size, "#%02x%02x%02x" % color[1]), colors)

    return filter(lambda c: c[0] > .025, hex_colors)

def add_to_redis(record, colors):
    r = StrictRedis()
    value = "|".join([record['thumb'],record['id'],record['url'],record['title']])
    for score, color in colors:
        r.zadd(color, score, value)


def main():

    deets = get_item_details(argv[1])
    for deet in deets:
        image = load_remote_image(deet['thumb'])
        if image:
            colors = get_image_colors(image)
            add_to_redis(deet, colors)

if __name__ == "__main__":
    main()