__author__ = 'cbn'

import json
from re import match
from flask import Flask, render_template, redirect, request, url_for
from redis import StrictRedis
import colorsys
import cooperhewitt.swatchbook as sb
from flask_paginate import Pagination

app = Flask(__name__)
app.redis = StrictRedis()
app.palette = sb.load_palette('css3')

@app.route("/")
def browse():

    return render_template("home.html")

@app.route("/<color>")
@app.route("/<color>/page/<int:page>")
def single_color(color, page=1, per_page=50 ):


    if not match("[0-9a-fA-F]{6}$", color):
        try:
            color = app.palette.hex(color).strip("#")
        except:
            return "Better error handling coming soon, but there are a lot of ways to spell a color, yaknowwhaddamean!",  404

    total = app.redis.zcount("#" + color,0,100)

    if not total:
        color = app.palette.closest("#" + color)

    startAt = (page -1) * per_page
    records = app.redis.zrevrange("#" + color,startAt, startAt + per_page -1)

    hex,name = sb.closest('css3', "#" + color)
    href="/" + hex.strip("#") + "/page/{0}"

    pagination = Pagination(page=page, total=total, per_page=per_page, href=href, bs_version=3 )

    return render_template("color.j2", records=[json.loads(record) for record in records ],
                           hex=hex,name=name, pagination=pagination, orig_color=request.args.get("color",None))

@app.route("/color")
def redirect_param_to_color():
    color = request.args.get('color','')
    if color:
        return redirect(url_for('single_color',color=color))
    else:
        return "Nope", 404

@app.route("/colors")
def list_available_colors():
    stored_colors = app.redis.keys("#*")
    stored_colors.sort(key=hex_to_hsv)
    palette = sb.load_palette('css3')
    hex_and_name = [[hex.strip("#"), palette.name(hex)] for hex in stored_colors ]
    return json.dumps(hex_and_name)


@app.route("/color/<color>")
@app.route("/color/<color>/page/<int:page>")
def images_for_a_color(color, page=0, per_page=50):
    if not match("[0-9a-fA-F]{6}$", color):
        return json.dumps({"error": "Not a valid hex color"}), 500

    startAt = page * per_page
    # can I do the offsets in redis itself and still maintain order?
    records = app.redis.zrevrangebyscore("#" + color,100,0)[startAt:startAt + per_page]
    return json.dumps([json.loads(record) for record in records]), 200

@app.route("/bubble")
def bubble_viz():
    count = {}
    count['children'] = [
                {
                'hex' : hex,
                'name': app.pallette.name(hex),
                'count': app.redis.zcount(hex, 0,100)
                } for hex in app.redis.keys("#*")
            ]

    return render_template('bubble.j2', count=json.dumps(count))

def hex_to_hsv(color):
    color =  color.strip("#")
    r,g,b = (int(color[i:i+2], 16) / 255.0 for i in xrange(0,5,2))
    return colorsys.rgb_to_hsv(r,g,b)


if __name__ == '__main__':
    app.run(debug=True)
