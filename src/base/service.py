import os


def delete_old_file(path_file):
    """ Удаление старого файла """
    if 'default/' not in path_file and os.path.exists(path_file):
        os.remove(path_file)


def post_view_count(instance):
    instance.view_count += 1
    instance.save()
    return instance
