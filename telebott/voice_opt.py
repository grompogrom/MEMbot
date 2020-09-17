def voice_record(user_name, voice_date, file, name_server):
    import os
    from telebott import ogg_mp3
    directory_name0 = r"D:\python\MEMbot\audiodata\{0}".format(name_server)
    directory_name1 = r'D:\python\MEMbot\audiodata\{0}\{1}'.format(name_server, user_name)
    directory_name2 = r'D:\python\MEMbot\audiodata\{0}\{1}\{2}.ogg'.format(name_server, user_name, str(voice_date))
    if not os.path.exists(directory_name0):
        os.mkdir(directory_name0)

    if not os.path.exists(directory_name1):
        os.mkdir(directory_name1)

    with open(directory_name2, 'wb') as r:
        r.write(file)
        print('файл записан ' + user_name)
    ogg_mp3.convert(directory_name2)
    print('файл конвертирован ' + user_name)
