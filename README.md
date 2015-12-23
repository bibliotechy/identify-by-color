# identify-by-color

identify-by-color is a webapp that lets you search the [Digital Public Library
of America] by color. It was inspired by similar work done at the Cooper-Hewitt
around using color for access. You can see the application running [here].

## Install

1. Install [Python 2.7], [Git] and [Redis]
1. `git clone https://github.com/bibliotechy/identify-by-color.git`
1. `cd identify-by-color`
1. `pip install -r requirements.txt`
1. download an `all.json.gz` [DPLA data snapshot]
1. `gunzip all.json.gz`
1. `./download.py all.json`
1. `./server.py`

[Digital Public Library of America]: http://dp.la
[here]: http://colorbrowse.club/
[Cooper-Hewitt]: https://collection.cooperhewitt.org/objects/colors/
[Python]: http://python.org/download/
[Git]: https://git-scm.com/
[Redis]: http://redis.io
[DPLA data snapshots]: http://dp.la/info/developers/download/
