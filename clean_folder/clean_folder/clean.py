import re
import sys
import shutil
from pathlib import Path

# FILES:
JPEG_IMAGES = []
JPG_IMAGES = []
PNG_IMAGES = []
SVG_IMAGES = []
MP3_AUDIO = []
MP4_VIDEO = []
PDF_DOC = []
TORRENTS = []
MY_OTHER = []
ARCHIVES = []

DICT_OF_FORMATS = {
    'JPEG': JPEG_IMAGES,
    'JPG': JPG_IMAGES,
    'PNG': PNG_IMAGES,
    'SVG': SVG_IMAGES,
    'MP3': MP3_AUDIO,
    'MP4': MP4_VIDEO,
    'PDF': PDF_DOC,
    'ZIP': ARCHIVES,
    'TORRENT': TORRENTS
}

KNOWN_FORMAT = set()
UNKNOWN_FORMAT = set()
WITHOUT_FORMAT = list()

# path_to_dir = '/Users/slavon/Trash'
DIRS_RESULT = ('archives', 'video', 'audio', 'documents',
               'images', 'torrents', 'archives', 'MY_OTHER')
DIR_TEMP = []

# NORMALIZE
CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
LATIN_SYMBOLS = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                 "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")
TRANS = {}
for c, l in zip(CYRILLIC_SYMBOLS, LATIN_SYMBOLS):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()


def normalize(name: str) -> None:
    CHARACHTER = name.translate(TRANS)
    if Path(CHARACHTER).suffix:
        PREFIX = Path(CHARACHTER).stem
        SUFFIX = Path(CHARACHTER).suffix
        CHARACHTER = re.sub(r'\W', '_', PREFIX)
        return CHARACHTER + SUFFIX
    else:
        CHARACHTER = name.translate(TRANS)
        CHARACHTER = re.sub(r'\W', '_', CHARACHTER)
        return CHARACHTER


# __________________________________________________________________________________________________________________________________

# CONVERT_.format_to_DIR

def convert_FORMAT_to_DIR(name_file: str) -> str:
    # print(name_file)                                               # <= for debug
    if Path(name_file).suffix:
        return Path(name_file).suffix.upper().replace('.', '')

# __________________________________________________________________________________________________________________________________


def main(path_to_dir: Path) -> None:
    check_dir(Path(path_to_dir))
    # print(Path(path_to_dir))

    for file in JPEG_IMAGES:
        handle_media(file, path_to_dir / 'images' / 'JPEG')
    for file in JPG_IMAGES:
        handle_media(file, path_to_dir / 'images' / 'JPG')
    for file in PNG_IMAGES:
        handle_media(file, path_to_dir / 'images' / 'PNG')
    for file in SVG_IMAGES:
        handle_media(file, path_to_dir / 'images' / 'SVG')
    for file in MP3_AUDIO:
        handle_media(file, path_to_dir / 'audio' / 'MP3')
    for file in MP4_VIDEO:
        handle_media(file, path_to_dir / 'video' / 'MP4')
    for file in PDF_DOC:
        handle_media(file, path_to_dir / 'documents' / 'PDF')
    for file in TORRENTS:
        handle_media(file, path_to_dir / 'torrents')
    for file in MY_OTHER:
        handle_media(file, path_to_dir / 'MY_OTHER')
    for file in ARCHIVES:
        handle_archive(file, path_to_dir / 'archives')

    for folder in DIR_TEMP:
        handle_folder(Path(folder))


# __________________________________________________________________________________________________________________________________

# ITERATION_OPS_DIR

def check_dir(name_dir: Path) -> None:
    for dir in name_dir.iterdir():
        if dir.is_dir():
            if dir.name not in DIRS_RESULT and dir.name not in DICT_OF_FORMATS:
                if not 'archives' in str(dir.parent):
                    DIR_TEMP.append(dir)
            check_dir(dir)
            continue
        # print(dir.name)                                                            # <= debug
        EXT_FORMAT = convert_FORMAT_to_DIR(dir.name)
        print(EXT_FORMAT, dir.name)
        FULL_PATH_TO_FILE = name_dir / dir.name
        if not EXT_FORMAT:
            WITHOUT_FORMAT.append(dir.name)

        else:
            try:
                ITEM_TO_ADD = DICT_OF_FORMATS[EXT_FORMAT]
                KNOWN_FORMAT.add(EXT_FORMAT)
                ITEM_TO_ADD.append(FULL_PATH_TO_FILE)
            except KeyError:
                UNKNOWN_FORMAT.add(EXT_FORMAT)
# __________________________________________________________________________________________________________________________________

# HANDLE FILE


def handle_media(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))


def handle_other(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))


def handle_archive(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)  # робимо папку для архіва
    folder_for_file = target_folder / \
        normalize(filename.name.replace(filename.suffix, ''))
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(filename, folder_for_file)
    except shutil.ReadError:
        print('It is not archive')
        folder_for_file.rmdir()
    filename.unlink()


def handle_folder(folder: Path):
    try:
        folder.rmdir()
    except OSError:
        print(f"Can't delete folder: {folder}")


if __name__ == "__main__":
    if sys.argv[1]:
        FOLDER_TO_SCAN = Path(sys.argv[1])
        print(f'Start in path_to_dir: {FOLDER_TO_SCAN.resolve()}')
        main(FOLDER_TO_SCAN.resolve())

print(f'DIR_TEMP => {DIR_TEMP}')
print(f'KNOWN_FORMATS => {KNOWN_FORMAT}')
print(f'UNKNOWN_FORMATS => {UNKNOWN_FORMAT}')
print(f'ARCHIVES: {ARCHIVES}')
print(f'WITHOUT_FORMAT: {WITHOUT_FORMAT}')
