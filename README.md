# identify-by-color

identify-by-color is a webapp that lets you search the [Digital Public Library
of America] by color. It was inspired by similar work done at the Cooper-Hewitt
around using color for access. You can see the application running [here].

The app is a Python flask application that uses Redis to store color
information. To populate the database you'll need to run `download.py`
with a DPLA export, which will fetch an image for an object and then 
process it with [py-cooperhewitt-swatchbook] to get the dominant colors.

## Install

1. Install [Python 2.7], [Git] and [Redis]
1. git clone https://github.com/bibliotechy/identify-by-color.git
1. cd identify-by-color
1. pip install -r requirements.txt
1. download `all.json.gz` [DPLA data snapshot]
1. ./download.py all.json.gz
1. ./server.py

[Digital Public Library of America]: http://dp.la
[here]: http://colorbrowse.club/
[Cooper-Hewitt]: https://collection.cooperhewitt.org/objects/colors/
[Python 2.7]: http://python.org/download/
[Git]: https://git-scm.com/
[Redis]: http://redis.io
[DPLA data snapshot]: http://dp.la/info/developers/download/
[py-cooperhewitt-swatchbook]: https://github.com/cooperhewitt/py-cooperhewitt-swatchbook
