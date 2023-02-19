import argparse
import asyncio
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse

import aiofiles
import aiohttp
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from eromedownloader.save_dir import get_save_dir

_HOST_NAME = "www.erome.com"
_USER_AGENT = {"User-Agent": "Mozilla/5.0"}


def run(album_url: str, save_dir_parent: str | None, override: bool, concurrent_requests_max: int, ignore_images: bool,
        ignore_videos: bool):
    if urlparse(args.url).hostname != _HOST_NAME:
        raise ValueError(f"Host must be {_HOST_NAME}")

    album_title, urls = _scrape_data(album_url, ignore_images, ignore_videos)

    save_dir = get_save_dir(save_dir_parent, album_title, override)

    asyncio.run(_download_media(urls, album_url, concurrent_requests_max, save_dir))


async def _download_media(urls: Iterable[str], album_url: str, concurrent_requests_max: int, dst_dir: Path):
    semaphore = asyncio.Semaphore(concurrent_requests_max)

    async with aiohttp.ClientSession(headers={
        "Referer": album_url,
        **_USER_AGENT
    }) as session:
        for url in urls:
            await _download_url_content(url, dst_dir, session, semaphore)


async def _download_url_content(url: str, dst_dir: Path, session: aiohttp.ClientSession, semaphore: asyncio.Semaphore):
    CHUNK_SIZE = 1024

    async with semaphore, session.get(url) as r:
        if r.ok:
            file_name = Path(urlparse(url).path).name
            pbar = tqdm(desc=f"[+] Downloading {file_name}",
                        total=int(r.headers["content-length"]),
                        unit="iB",
                        unit_scale=True,
                        unit_divisor=CHUNK_SIZE,
                        colour="green")
            async with aiofiles.open(Path(dst_dir, file_name), "wb") as f:
                async for chunk in r.content.iter_chunked(CHUNK_SIZE):
                    written_size = await f.write(chunk)
                    pbar.update(written_size)
        else:
            print(f"[ERROR] Download of {url} failed with {r}")


def _scrape_data(album_url: str, ignore_images: bool, ignore_videos: bool):
    r = requests.get(album_url, headers=_USER_AGENT)

    if r.status_code != 200:
        raise ConnectionError(f"Request Error {r.status_code}")

    soup = BeautifulSoup(r.content, "html.parser")

    album_title = soup.find("meta", property="og:title")["content"]
    print(f"Scraping {album_title}")

    urls = []
    if not ignore_images:
        image_urls = {image["data-src"] for image in soup.find_all("img", {"class": "img-back"})}
        print(f"Found {len(image_urls)} Image(s)")
        urls.extend(image_urls)
    if not ignore_videos:
        video_urls = {video_source["src"] for video_source in soup.find_all("source")}
        print(f"Found {len(video_urls)} Video(s)")
        urls.extend(video_urls)

    return album_title, urls


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="Album URL", type=str, required=True)
    parser.add_argument("--path", help="Save destination path", type=str, default=None)
    parser.add_argument("--override", help="Save destination path", type=bool, default=False)
    parser.add_argument("--concurrent-requests-max", help="Max number of concurrent requests to be made", type=int,
                        default=4)
    parser.add_argument("--ignore-images", type=bool, default=False)
    parser.add_argument("--ignore-videos", type=bool, default=False)

    args = parser.parse_args()

    run(album_url=args.url,
        save_dir_parent=args.path,
        override=args.override,
        concurrent_requests_max=args.concurrent_requests_max,
        ignore_images=args.ignore_images,
        ignore_videos=args.ignore_videos)
