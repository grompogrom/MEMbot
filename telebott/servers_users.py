def save_serversID(ids):
    import pickle
    with open('serversID.pickle', 'wb') as f:
        pickle.dump(ids, f)


def get_serversID():
    import pickle
    with open(r'serversID.pickle', 'rb') as r:
        ids = pickle.load(r)
    return ids


if __name__ == '__main__':
    print(get_serversID())