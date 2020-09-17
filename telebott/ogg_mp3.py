def convert(file):
    import pydub
    import os
    ogg_file = file
    mp3_file = os.path.splitext(ogg_file)[0] + '.mp3'
    sound = pydub.AudioSegment.from_ogg(ogg_file)
    sound.export(mp3_file, format="mp3")
    os.remove(ogg_file)
