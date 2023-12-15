import sys
import re
import shutil
from pathlib import Path


graphic_files = list()
video_files = list()
audio_files = list()
docs_files = list()
folders = list()
archives = list()
others = list()
unknown = set()
extensions = set()

registered_extensions = {
    'JPEG':  graphic_files,
     'PNG':  graphic_files,
     'JPG':  graphic_files,
     'SVG':  graphic_files,
     'TXT':  docs_files,
     'DOCX': docs_files,
     'DOC':  docs_files,
     'PDF':  docs_files,
     'XLSX': docs_files,
     'PPTX': docs_files,
     'MP4':  video_files,
     'AVI':  video_files,
     'MOV':  video_files,
     'MKV':  video_files,
     'MP3':  audio_files,
     'OGG':  audio_files,
     'WAV':  audio_files,
     'AMR':  audio_files,
     'ZIP':  archives,
     'GZ':   archives,
     'TAR':  archives,
     'OTHERS': others
}

def get_extensions(file_name):
    return Path(file_name).suffix[1:].upper()

def scan(folder):
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in registered_extensions:
                folders.append(item)
                scan(item)
            continue

        extension = get_extensions(file_name=item.name)
        new_name = folder/item.name
        if not extension:
            others.append(new_name)
        else:
            try:
                container = registered_extensions[extension]
                extensions.add(extension)
                container.append(new_name)
            except KeyError:
                unknown.add(extension)
                others.append(new_name)

UKRAINIAN_SYMBOLS = 'абвгдеєжзиіїйклмнопрстуфхцчшщьюя'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "je", "zh", "z", "y", "i", "ji", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "ju", "ja")

TRANS = {}

for key, value in zip(UKRAINIAN_SYMBOLS, TRANSLATION):
    TRANS[ord(key)] = value
    TRANS[ord(key.upper())] = value.upper()

def normalize(name):
    name, *extension = name.split('.')
    new_name = name.translate(TRANS)
    new_name = re.sub(r'\W', '_', new_name)
    return f"{new_name}.{'.'.join(extension)}"

def handle_file(path, root_folder, dist):
    target_folder = root_folder/dist
    target_folder.mkdir(exist_ok=True)
    path.replace(target_folder/normalize(path.name))

def handle_archive(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)
    norm_name = normalize(path.stem)
    if "." in norm_name and norm_name.index(".") < len(norm_name) - 1:
        result = norm_name.split('.')
        norm_name = result[0]

    archive_folder = target_folder / norm_name
    archive_folder.mkdir(exist_ok=True)

    try:
        shutil.unpack_archive(str(path.resolve()), str(archive_folder.resolve()))

    except shutil.ReadError:
        archive_folder.rmdir()
        return
    
    except FileNotFoundError:
        archive_folder.rmdir()
        return
    
    path.unlink()


def remove_empty_folders(path):
    for item in path.iterdir():
        if item.is_dir():
            remove_empty_folders(item)
            try:
                item.rmdir()
            except OSError:
                pass
                #print(path)
                #print(f'Error. Can not remove folder. {OSError} \n {path}')

def main(folder_path):
    #print(folder_path)
    scan(folder_path)

    for file in graphic_files:
        handle_file(file, folder_path, "Graphic")

    for file in audio_files:
        handle_file(file, folder_path, "Audio")

    for file in video_files:
        handle_file(file, folder_path, "Video")

    for file in docs_files:
        handle_file(file, folder_path, "Documents")

    for file in others:
        handle_file(file, folder_path, "Other")

    for file in archives:
        handle_archive(file, folder_path, "Arhives")

    remove_empty_folders(folder_path)

if __name__ == '__main__':
    path = sys.argv[1]
    print(f'Start in {path}')

    folder = Path(path)
    main(folder.resolve())

    #scan(folder)

    print(f"{len(graphic_files)} Graphics files found: {graphic_files} \n")
    print(f"Audio: {audio_files} \n")
    print(f"Video: {video_files} \n")
    print(f"Ddocx: {docs_files} \n")
    print(f"Archive: {archives} \n")
    if others:
        print(f"Unknown files: {others} \n")
    if unknown:
        print(f"Unknown extensions: {unknown} \n")
    print(f"All extensions: {extensions} \n")
    #print(f"Folder: {folders} \n")





