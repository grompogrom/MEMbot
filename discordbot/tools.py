from const import YTB_DIR


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


def remove_file(directory= YTB_DIR):
    import os
    print(f'[remove] {directory}')
    try:
        files = os.listdir(directory)
        if directory == YTB_DIR:
            for file in files:
                way = r'{0}\{1}'.format(directory, file)
                os.remove(way)
        else:
            os.remove(directory)
    except Exception as e:
        print('deleting files error')
        print(e)


if __name__ == '__main__':
    remove_file()