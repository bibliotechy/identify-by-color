__author__ = 'cbn'

import json
from re import match
from flask import Flask, render_template
from redis import StrictRedis
import cooperhewitt.swatchbook as sb

app = Flask(__name__)
app.redis = StrictRedis()

@app.route("/")
def browse():
    return render_template("home.html")

@app.route("/<color>", defaults={'page': 1})
@app.route("/<color>/page/<page>")
def single_color(color,page):
    if not match("[0-9a-fA-F]{6}$", color):
        return json.dumps({"error": "Not a valid hex color"}), 500

    if page == "1":
        records = app.redis.zrevrangebyscore("#" + color,100,0)[:50]
    else:
        records = app.redis.zrevrangebyscore("#" + color,100,0)[int(page)*50:int(page)*50+50]
    hex,name = sb.closest('css3', "#" + color)

    return render_template("color.html", records=[json.loads(record) for record in records],hex=hex,name=name,page=page)


@app.route("/colors")
def list_available_colors():
    return json.dumps(sorted(app.redis.keys("#*")))

@app.route("/color/<color>")
def images_for_a_color(color):
    if not match("[0-9a-fA-F]{6}$", color):
        return json.dumps({"error": "Not a valid hex color"}), 500
    records = app.redis.zrevrangebyscore("#" + color,100,0)
    return json.dumps([json.loads(record) for record in records]), 200


if __name__ == '__main__':
    app.run(debug=True)
