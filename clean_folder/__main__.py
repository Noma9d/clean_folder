from pathlib import Path
import shutil
import sys


CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", 'i', "ji", "g")

TRANS = {}

for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()

def normalize(name) -> str:
    t_name = name.translate(TRANS)
    path_name = Path(t_name)
    stem_name = path_name.stem
    type_name = path_name.suffix
    result = ''
    for i in stem_name:
        if 'a' <= i <= 'z' or 'A' <= i <= 'Z' or '0' <= i <= '9':
            result += i
            continue
        else:
            result += '_'
    result += type_name

    return result


IMAGES = [] #JPEG_IMAGES, JPG_IMAGES, PNG_IMAGES, SVG_IMAGES
DOCUMENTATION = [] #DOC_DOCUMENTATION, DOCX_DOCUMENTATION, TXT_DOCUMENTATION, PDF_DOCUMENTATION, XLSX_DOCUMENTATION, PPTX_DOCUMENTATION
VIDEO = [] #MP4_VIDEO MOV_VIDEO MKV_VIDEO
AUDIO = [] #MP3_AUDIO OGG_AUDIO WAV_AUDIO AMR_AUDIO
ARCHIVES = [] #ZIP_ARCHIVES GZ_ARCHIVES TAR_ARCHIVES
MY_OTHER = []  #Other file extention

REGISTER_EXTENSION = {
    'JPEG': IMAGES,
    'JPG': IMAGES,
    'PNG': IMAGES,
    'SVG': IMAGES,
    'AVI': VIDEO,
    'MP4': VIDEO, 
    'MOV': VIDEO,
    'MKV': VIDEO,
    'DOC': DOCUMENTATION,
    'DOCX': DOCUMENTATION,
    'TXT': DOCUMENTATION,
    'PDF': DOCUMENTATION,
    'XLSX': DOCUMENTATION,
    'PPTX': DOCUMENTATION,
    'MP3': AUDIO,
    'OGG': AUDIO,
    'WAV': AUDIO,
    'AMR': AUDIO,
    'ZIP': ARCHIVES,
    'GZ': ARCHIVES,
    'TAR': ARCHIVES,
}

FOLDERS = []
EXTENSIONS = set()
UNKNOWN = set()

def get_extension(filename: str) -> str:
    return Path(filename).suffix[1:].upper()


def scan(folder: Path):
    for item in folder.iterdir():
        # Робота з папкою
        if item.is_dir():
            # Перевіряємо, щоб папка не була тією в яку ми вже складаємо файли.
            if item.name not in ('archives', 'video', 'audio', 'documents', 'images', 'other'):
                FOLDERS.append(item)
                scan(item)  # скануємо цю вкладену папку - рекурсія
            continue  # переходимо до наступного елемента в сканованій папці
        # else:
        # Робота з файлом
        ext = get_extension(item.name)  # беремо розширення файлу
        # full_name = folder / item.name  # беремо повний шлях до файлу
        if not ext:
            MY_OTHER.append(item)
        else:
            try:
                container = REGISTER_EXTENSION[ext]
                EXTENSIONS.add(ext)
                container.append(item)
            except KeyError:
                UNKNOWN.add(ext)
                MY_OTHER.append(item)




def handle_media(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))

def handle_other(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))

def handle_arhive(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    folder_for_file = target_folder / normalize(filename.name.replace(filename.suffix, ''))
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(str(filename.resolve()), str(folder_for_file.resolve()))
    except shutil.ReadError:
        folder_for_file.rmdir()
        return None
    filename.unlink()

def handle_folder(folder: Path) -> None:
    try:
        folder.rmdir()
    except OSError:
        print(f'Sorry, we can not delete the folder: {folder}')


def main(folder: Path) -> None:
    scan(folder)
    for file in IMAGES:
        handle_media(file, folder / 'images')
    for file in AUDIO:
        handle_media(file, folder / 'audio')
    for file in DOCUMENTATION:
        handle_media(file, folder / 'documentation')
    for file in VIDEO:
        handle_media(file, folder / 'video')
    for file in MY_OTHER:
        handle_other(file, folder / 'MY_OTHER')

    for file in ARCHIVES:
        handle_arhive(file, folder / 'archives')

    for folder in FOLDERS[::-1]:
        handle_folder(folder)

if __name__ == '__main__':
    folder_for_scan = Path(sys.argv[1])
    main(folder_for_scan.resolve())

    scan_folder = sys.argv[1]
    print(scan_folder)
    print(f'Start in folder: {scan_folder}')

    scan(Path(scan_folder))
    print(f'IMAGES : {IMAGES}')
    print(f'AUDIO : {AUDIO}')
    print(f'ARCHIVES: {ARCHIVES}')
    print(f'VIDEO: {VIDEO}')
    print(f'DOCUMENTATION: {DOCUMENTATION}')
    print(f'OTHER FILES: {MY_OTHER}')
    print('*' * 25)
    print(f'Types of file in folder: {EXTENSIONS}')
    print(f'UNKNOWN: {UNKNOWN}')

 