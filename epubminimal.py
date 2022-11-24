from os import getcwd, path, sep, walk
from pathlib import Path
from PIL import Image
from zipfile import ZIP_DEFLATED, ZipFile


def percentage(part: int, whole: int) -> int:
    return int(100 * part / whole)

def sizeof_fmt(num: int, suffix: str = 'B') -> str:
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return f'{num:3.1f}{unit}{suffix}'
        num /= 1024.0
    return f'{num:.1f}Yi{suffix}'

def zipdir(name: str, zipr: ZipFile):
    for folder_name, _, file_names in walk(name):
        for file_name in file_names:
            file_path = path.join(folder_name, file_name)
            zipr.write(file_path, arcname=path.relpath(file_path, name))

def compress(root: str, file: str, image: Image, percentage_input: int):
    w = percentage(percentage_input, image.width)
    h = percentage(percentage_input, image.height)

    image.resize((w, h))
    image.save(root + sep + file)


file_input = input('File: ')
if file_input.endswith('/'):
    file_input = file_input.removesuffix('/')

percentage_input = 40
percentage_input = int(input('Compression % (Default 40, 0-100): '))


if not file_input == '' and path.exists(file_input) and file_input.endswith('.epub'):
    head, tail = path.split(file_input)
    ext_dir = getcwd() + sep + 'extracted_epub'

    with ZipFile(file_input, 'r') as zipf:
        zipf.extractall(ext_dir)

    for root, dirs, files in walk(ext_dir):
        for index, file in enumerate(files):
            if file.endswith('.png') or file.endswith('.jpg') or file.endswith('.jpeg'):
                extension = file.split('.')[1]
                print(f'[INFO]: Found .{extension}')

                image = Image.open(root + sep + file)
                file_path = Path(root + sep + file)

                old_size = sizeof_fmt(file_path.stat().st_size)
                compress(root, file, image, percentage_input)
                new_size = sizeof_fmt(file_path.stat().st_size)

                print(f'[INFO]: Compressed {file} from {old_size} to {new_size}')
    print('[INFO]: Done!')
    print('[INFO]: Overwrote the original .epub.')

    with ZipFile(file_input, 'w', ZIP_DEFLATED) as zipf:
        zipdir(ext_dir, zipf)
else:
    print('File does not exist at the provided path or is not a .epub.')