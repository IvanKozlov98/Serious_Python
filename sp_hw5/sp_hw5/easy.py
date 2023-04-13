import asyncio
import aiohttp
import aiofiles
import os
from utils import async_measure_time


async def download_image(url, session, filename):
    async with session.get(url) as response:
        async with aiofiles.open(filename, 'wb') as file:
            while True:
                chunk = await response.content.read(1024)
                if not chunk:
                    break
                await file.write(chunk)


@async_measure_time
async def download_all_images(image_count, directory):
    url = "https://picsum.photos/1000/1000"
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(image_count):
            filename = str(i) + ".jpg"
            full_path = os.path.join(directory, filename)
            task = asyncio.create_task(download_image(url, session, filename=full_path))
            tasks.append(task)
        try:
            await asyncio.gather(*tasks, return_exceptions=True)
        except Exception as ex:
            print(repr(ex))


def main_easy():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(download_all_images(20, directory="../artifacts/easy/"))