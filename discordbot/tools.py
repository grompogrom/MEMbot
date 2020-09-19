from const import *
def make_playlist(guild: str):
    import os
    playlist = []
    link = r'D:\python\MEMbot\audiodata\{0}'.format(guild)
    for user in os.listdir(link):
        link1 = link + r'\{0}'.format(user)
        for track in os.listdir(link1):
            link2 = link1 + r'\{0}'.format(track)
            playlist.append(link2)
            del link2
        del link1
    return playlist


def remove_file(dir= YTB_DIR):
    import os
    try:
        files = os.listdir(dir)
        if dir == YTB_DIR:
            for file in files:
                way = r'{0}\\{1}'.format(dir,file)
                os.remove(way)
        else:
            os.remove(dir)
    except Exception as e:
        print('deleting files error')
        print(e)


if __name__ == '__main__':
    remove_file(YTB_DIR)