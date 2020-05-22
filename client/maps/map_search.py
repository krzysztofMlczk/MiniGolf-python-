import os


def map_search(directory):
    map_files = []
    for root, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.json') and not filename.startswith('template'):
                map_files.append(os.path.join(root, filename))
    return map_files
