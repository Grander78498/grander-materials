from typing import Any
import random
import re


class OntologyObject:
    shown_field = 'name'

    def __str__(self) -> str:
        return getattr(self, self.shown_field)


class Performer(OntologyObject):
    instances = []

    def __init__(self, name: str, country: str) -> None:
        self.name = name
        self.country = country
        Performer.instances.append(self)


class MusicRecord(OntologyObject):
    instances = []

    def __init__(self, name: str):
        self.name = name
        MusicRecord.instances.append(self)


class Group(Performer):
    instances = []

    def __init__(self, name: str, country: str):
        super().__init__(name, country)
        Group.instances.append(self)


class Musician(Performer):
    instances = []

    def __init__(self, name: str, country: str, in_group: Group):
        super().__init__(name, country)
        self.in_group = in_group
        Musician.instances.append(self)


class Album(MusicRecord):
    instances = []

    def __init__(self, name: str, release_year: int, performed_by: Performer):
        super().__init__(name)
        self.release_year = release_year
        self.performed_by = performed_by
        Album.instances.append(self)


class Song(MusicRecord):
    instances = []

    def __init__(self, name: str, in_album: Album):
        super().__init__(name)
        self.in_album = in_album
        Song.instances.append(self)


def find_related_objects_by_value(cls: OntologyObject.__class__,
                                  lookup_field: str, value: Any):
    instances = cls.instances
    result = []
    for instance in instances:
        if isinstance(getattr(instance, lookup_field), OntologyObject):
            if not isinstance(value, OntologyObject):
                value = find_object_by_name(
                    getattr(instance, lookup_field).__class__, value)
                if value is None:
                    return None

        if getattr(instance, lookup_field) == value:
            result.append((instance, type(instance).__name__))
    return result


def get_class(class_name: str):
    classes = {
        'musician': Musician,
        'group': Group,
        'album': Album,
        'song': Song
    }
    class_name = class_name.lower().strip()
    if class_name in classes:
        return classes[class_name]
    else:
        return None


def find_object_by_name(cls: OntologyObject.__class__, name: str):
    instances = cls.instances
    for instance in instances:
        if instance.name == name:
            return instance

    return None


def get_random_class_instance(cls: OntologyObject.__class__):
    instances = cls.instances
    return random.choice(instances)


def get_related_class(obj: OntologyObject):
    classes = [Album, Song, Musician, Group]
    class_types = set()
    for cls in classes:
        cls_instances = cls.instances
        for instance in cls_instances:
            fields = [
                key for key in instance.__dict__.keys()
                if not re.match(r"__\w*__", key)
            ]
            for field in fields:
                field_value = getattr(instance, field)
                if field_value == obj:
                    class_types.add((cls, field))
    return list(class_types)


def main():
    groups = [Group('Queen', 'Great Britain'), Group('Metallica', 'USA')]
    musicians = [
        Musician('Freddie Mercury', 'Zanzibar', groups[0]),
        Musician('John Deacon', 'UK', groups[0]),
        Musician('Brian May', 'UK', groups[0]),
        Musician('Roger Taylor', 'UK', groups[0]),
        Musician('James Hetfield', 'USA', groups[1]),
        Musician('Kirk Hammett', 'USA', groups[1]),
        Musician('Lars Ulrich', 'USA', groups[1]),
        Musician('Robert Trujilio', 'USA', groups[1])
    ]
    albums = [
        Album('Mr.Bad Guy', 1985, musicians[0]),
        Album('A Night At The Opera', 1975, groups[1]),
        Album('Innuendo', 1991, groups[0]),
        Album('Ride The Lightning', 1984, groups[1]),
        Album('Master Of Puppets', 1986, groups[1])
    ]
    songs = [
        Song('Living On My Own', albums[0]),
        Song('Bohemiarn Rhapsody', albums[1]),
        Song('Love Of My Life', albums[1]),
        Song('Innuendo', albums[2]),
        Song('Ride The Lightning', albums[3]),
        Song('For Wthom The Bell Tolls', albums[3]),
        Song('Master Of Puppets', albums[4]),
        Song('Battery', albums[4])
    ]

    while True:
        while True:
            class_name = input('Введите класс получаемых объектов: ')
            cls: OntologyObject.__class__ | None = get_class(class_name)
            if cls is None:
                print('Такого класса не существует\n\n')
            else:
                break

        while True:
            instance = get_random_class_instance(cls)
            available_fields = [
                key for key in instance.__dict__.keys()
                if not re.match(r"__\w*__", key)
            ]
            field = input(
                f'Введите требуемое поле ( {", ".join(available_fields)} ): ')
            try:
                getattr(instance, field)
                break
            except Exception:
                print('Такого поля в классе не существует\n\n')

        value = input('Введите значение поля: ')
        res = find_related_objects_by_value(cls, field, value)

        while True:
            flag = False
            if res is None or len(res) == 0:
                print('Объекты по введённому запросу не найдены')
                while True:
                    _type = input(
                        '1 - повторить ввод запроса\nq - завершить выполнение программы\n'
                    )
                    if _type == 1:
                        break
                    elif _type == 'q':
                        exit(0)
            else:
                str_objects = [
                    "\033[32m" + str(obj) + "\033[0m (\033[33m" +
                    str(obj_type) + "\033[0m)" for obj, obj_type in res
                ]
                print(f'Полученные объекты: {", ".join(str_objects)}')
                while True:
                    _type = input('1 - повторить ввод запроса\n'
                                  '2 - посмотреть связанные объекты\n'
                                  'q - завершить выполнение программы\n')
                    if _type == '1':
                        flag = False
                        break
                    elif _type == '2':
                        flag = True
                        break
                    elif _type == 'q':
                        exit(0)

                if flag:
                    if len(res) == 1:
                        obj_number = 1
                    else:
                        while True:
                            obj_number = int(
                                input(
                                    f'Выберите номер нужного объекта (1-{len(res)}): '
                                ))
                            if obj_number not in range(1, len(res) + 1):
                                print('Введён неправильный номер')
                            else:
                                break

                    instance = res[obj_number - 1][0]
                    related_classes = get_related_class(instance)
                    res = []
                    for rel_class, field_name in related_classes:
                        res.extend(
                            find_related_objects_by_value(
                                rel_class, field_name, instance))
                else:
                    break
            if not flag:
                break


main()
