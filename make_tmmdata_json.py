import json
import csv
from pathlib import Path
from typing import Iterable, List, Set
from dataclasses import dataclass, field
from argparse import ArgumentParser, Namespace
from click import confirm, prompt, echo

MY_DIR: Path = Path(__file__).parent
OUTPUT_JSON_FILE_PATH: Path = MY_DIR/'tmmdata_tmmf2n.json'

now_id_num: int = 0


def create_id() -> str:
    global now_id_num
    now_id_num += 1
    return 'tmmf2nid'+'{:04d}'.format(now_id_num)


def parse_args() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        'Make TMMData JSON', description='Create tmmf2n JSON from tmmf2d CSV')
    parser.add_argument('--csv', help='CSV File Path', type=Path)
    args: Namespace = parser.parse_args()
    return args


class OrderedSet:
    '''
    要素を新規に追加した順に配列へ出力することができる集合。
    a, b, c, d, c, aの順に追加した場合、出力される配列は[a, b, c, d]となる。
    '''

    def __init__(self, arr: Iterable = None) -> None:
        self._elements_list: List = arr or []
        self._elements_set: Set = set(arr) if arr else set()

    def add(self, element) -> None:
        if element in self._elements_set:
            return
        self._elements_list.append(element)
        self._elements_set.add(element)

    def tolist(self) -> list:
        return self._elements_list


@dataclass
class Media:
    id: str = field(default_factory=create_id)
    type: str = ''
    payload: str = ''


@dataclass
class Chapter:
    id: str = field(default_factory=create_id)
    name: str = ''
    medias: List[Media] = field(default_factory=list)


@dataclass
class Lesson:
    id: str = field(default_factory=create_id)
    name: str = ''
    chapters: List[Chapter] = field(default_factory=list)


@dataclass
class Shelf:
    id: str = field(default_factory=create_id)
    name: str = ''
    lessons: List[Lesson] = field(default_factory=list)


def csv_to_obj(csv_file_path: Path, encoding: str = 'utf-8') -> List[Shelf]:
    file = open(str(csv_file_path), 'r', encoding=encoding)
    reader = csv.reader(file)

    shelves: List[Shelf] = []
    reading_shelf: Shelf = None
    reading_lesson: Lesson = None
    reading_chapter: Chapter = None
    for i, row in enumerate(reader):
        # ヘッド
        if i == 0:
            continue
        if not row[0] == '':  # シェルフ
            reading_shelf = Shelf(name=row[0])
            shelves.append(reading_shelf)
        elif not row[1] == '':  # レッスン
            if reading_shelf is None:
                raise ValueError(f'{i}行目、シェルフ名よりレッスン名が先行している。')
            reading_lesson = Lesson(name=row[1])
            reading_shelf.lessons.append(reading_lesson)
        elif not row[2] == '':  # チャプター
            if reading_lesson is None:
                raise ValueError(f'{i}行目、レッスン名よりチャプター名が先行している。')
            reading_chapter = Chapter(name=row[2])
            reading_lesson.chapters.append(reading_chapter)
        elif not row[3] == '':  # メディア
            if reading_chapter is None:
                raise ValueError(f'{i}行目、チャプター名よりメディアが先行している。')
            media = Media(type=row[3], payload=row[4])
            reading_chapter.medias.append(media)
    file.close()
    return shelves


def obj_to_normalized_obj(obj: List[Shelf]) -> dict:
    shelfIds_set: OrderedSet = OrderedSet()
    lessonIds_set: OrderedSet = OrderedSet()
    chapterIds_set: OrderedSet = OrderedSet()
    mediaIds_set: OrderedSet = OrderedSet()
    shelves: dict = {}
    lessons: dict = {}
    chapters: dict = {}
    medias: dict = {}
    for shelf in obj:
        shelf: Shelf
        shelfIds_set.add(shelf.id)
        shelves[shelf.id] = {
            'id': shelf.id,
            'name': shelf.name,
            'lessonIds': [lesson.id for lesson in shelf.lessons]
        }
        for lesson in shelf.lessons:
            lesson: Lesson
            lessonIds_set.add(lesson.id)
            lessons[lesson.id] = {
                'id': lesson.id,
                'name': lesson.name,
                'chapterIds': [chapter.id for chapter in lesson.chapters]
            }
            for chapter in lesson.chapters:
                chapter: Chapter
                chapterIds_set.add(chapter.id)
                chapters[chapter.id] = {
                    'id': chapter.id,
                    'name': chapter.name,
                    'mediaIds': [media.id for media in chapter.medias]
                }
                for media in chapter.medias:
                    media: Media
                    mediaIds_set.add(media.id)
                    medias[media.id] = {
                        'id': media.id,
                        'type': media.type,
                        'payload': media.payload
                    }
    tmmData: dict = {
        'shelfIds': shelfIds_set.tolist(),
        'lessonIds': lessonIds_set.tolist(),
        'chapterIds': chapterIds_set.tolist(),
        'mediaIds': mediaIds_set.tolist(),
        'shelves': shelves,
        'lessons': lessons,
        'chapters': chapters,
        'medias': medias
    }
    return tmmData


def normalized_obj_to_json(normalized_obj: dict, json_file_path: Path) -> None:
    json_text: str = json.dumps(normalized_obj, ensure_ascii=False)
    json_file_path.write_text(json_text, encoding='utf-8')


if __name__ == '__main__':
    args: Namespace = parse_args()
    if args.csv:
        csvfile: Path = args.csv
    else:
        csvfile: Path = prompt(
            'Drug the Teaching Material Medias CSV file, then push the Enter key.', type=Path)
    if not csvfile.exists():
        echo('This CSV file does not exist.')
        exit(-1)
    if OUTPUT_JSON_FILE_PATH.exists():
        if not confirm('The JSON file already exists. Overwrite?', default=False):
            exit(0)
    try:
        obj = csv_to_obj(csvfile)
        normalized_obj = obj_to_normalized_obj(obj)
        normalized_obj_to_json(normalized_obj, OUTPUT_JSON_FILE_PATH)
    except:
        echo('An Error Occured.')
        exit(-1)
