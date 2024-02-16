import types


class FlatIterator:

    def __init__(self, list_of_list):
        self.lst = list_of_list  # Текущий список элементов
        self.stack = []  # Список для элемента списка и его индекса
        self.count = 0  # Счетчик элементов в списке (индекс элемента)

    def __iter__(self):
        return self

    def __next__(self):
        if self.count >= len(self.lst):  # Если счетчик равен количеству элементов в списке, дошли до конца списка
            if self.stack:  # Если стек не пустой, достаем элемент и индекс
                self.lst, self.count = self.stack.pop()
                return self.__next__()
            else:
                # Если стек пустой, то прошлись по всем элементам
                raise StopIteration
        # Если счетчик меньше количества элементов в списке, в item помещаем элемент списка с индексом count
        else:
            item = self.lst[self.count]
            self.count += 1
            # Если item не список, возвращаем его
            if type(item) is not list:
                return item
            else:
                # Если item список, то в кортеж из элемента и индекса элемента
                self.stack.append((self.lst, self.count))
                # Вложенный список становится текущим списком
                self.lst = item
                self.count = 0
                return self.__next__()


def flat_generator(list_of_lists):
    #  Генератор, который преобразует вложенные списки в один список
    for item in list_of_lists:
        if isinstance(item, list):
            yield from flat_generator(item)
        else:
            yield item


def test_1():
    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]):
        assert flat_iterator_item == check_item
    assert list(FlatIterator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]


def test_2():

    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', [['f']], 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            flat_generator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):

        assert flat_iterator_item == check_item

    assert list(flat_generator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]

    assert isinstance(flat_generator(list_of_lists_1), types.GeneratorType)


def test_3():

    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_2),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    ):
        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_2)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']


def test_4():

    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

    for flat_iterator_item, check_item in zip(
            flat_generator(list_of_lists_2),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    ):

        assert flat_iterator_item == check_item

    assert list(flat_generator(list_of_lists_2)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']

    assert isinstance(flat_generator(list_of_lists_2), types.GeneratorType)


if __name__ == '__main__':
    test_1()
    test_2()
    test_3()
    test_4()
