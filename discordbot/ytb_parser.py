import asyncio
from const import YTB_DIR
URL = 'https://www.youtube.com/channel/'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/83.0.4103.116 Safari/537.36',
    'accept': '*/*'}

downloaded_jokes = {}


async def get_videos_url(url):
    '''gets channel url and returns list of video's url'''
    import requests
    import re

    def create_ful_url(urls):
        done_urls = []
        for url in urls:
            done_urls.append(r'https://www.youtube.com/' + url)
        return done_urls

    if url.startswith('https://www.youtube.com/c'):
        url += r'/videos'
        html = requests.get(url, HEADERS)
        print(html.status_code)
    else:
        return False
    if html.status_code == 200:
        hrefs = re.findall(r"watch\?v=...........", str(html.content))
        hrefs = create_ful_url(hrefs)
        print(hrefs)
        return  hrefs
    else:
        return False


def download_ytb_video(url, trackIndex):
    '''gets ytb url and number of track returns name of file'''
    import youtube_dl
    name = 'track'+str(trackIndex)
    ydl_ops = {
        'format': 'bestaudio/best',
        'outtmpl': r'D:/python/MEMbot/audiodata/ytb/{0}.%(ext)s'.format(name),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
                }]
                }

    with youtube_dl.YoutubeDL(ydl_ops) as ydl:
        print(f'[log] Загружаю трек ...')

        video_title = rf'{YTB_DIR}\{name}.mp3'
        print(video_title)
        ydl.download([url])
    return video_title


def test_name():
    download_ytb_video('https://www.youtube.com/channel/UC7yMBOeBTcPhlTdI-PS-_Xg')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(get_videos_url('https://www.youtube.com/channel/UC7yMBOeBTcPhlTdI-PS-_Xg'))

    loop.run_forever()