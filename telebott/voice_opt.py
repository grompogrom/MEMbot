def voice_record(user_name, voice_date, file, name_server):
    import os
    from telebott import ogg_mp3
    from const import VOICE_LINK
    directory_name0 = r"{0}/{1}".format(VOICE_LINK, name_server)
    directory_name1 = r'{0}/{1}'.format(directory_name0, user_name)
    directory_name2 = r'{0}/{1}.ogg'.format(directory_name1, str(voice_date))
    if not os.path.exists(directory_name0):
        os.mkdir(directory_name0)

    if not os.path.exists(directory_name1):
        os.mkdir(directory_name1)

    with open(directory_name2, 'wb') as r:
        r.write(file)
        print('файл записан ' + user_name)
    ogg_mp3.convert(directory_name2)
    print('файл конвертирован ' + user_name)
