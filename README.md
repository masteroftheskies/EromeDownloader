# eromedownloader

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/eromedownloader)
![PyPI - Status](https://img.shields.io/pypi/status/eromedownloader)
![PyPI - Downloads](https://img.shields.io/pypi/dm/eromedownloader)
![PyPI - License](https://img.shields.io/pypi/l/eromedownloader)

__Downloader for erome.com hosted as python package installable via pip__

## Installation

- *eromedownloader* uses python 3.11, so make sure you're using it prior to installing the package via pip

```shell
pip install eromedownloader
```

## Basic Usage

```shell
python eromedownloader --url https://www.erome.com/a/{ALBUM_ID}  
```

## Optional Arguments

- *--path*: str, path/to/save/dir
- *--override*: bool, whether to override album if already exists instead of downloading it under an incremented name version; __Default=False__
- *--concurrent-requests-max*: int, max number of requests to be sent; sending too many requests at once may comprise the risk of getting your IP banned by erome; __Default=4__
- *--ignore-images*: bool; __Default=False__
- *--ignore-videos*: bool; __Default=False__