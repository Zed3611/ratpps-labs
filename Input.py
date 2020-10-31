import json
from xml.dom.minidom import parseString, Document


class Input:                                                                            # Объект входных данных
    def __init__(self, serialization_type: str, input_object: str):                     # Инициализируется из xml или json
        self.serialization_type = serialization_type

        result = {}

        if serialization_type == 'Json':
            result = self.from_json(input_object)
        elif serialization_type == 'Xml':
            result = self.from_xml(input_object)

        self.k: int = result['K']
        self.muls: list[int] = result['Muls']
        self.sums: list[float] = result['Sums']

    def __str__(self):
        return f'K={self.k}, Muls={self.muls}, Sums={self.sums}'

    def from_json(self, string: str):                                                   # Используем библиотеку json
        result: dict = json.loads(string)                                               # для парсинга, получаем словарь
        if result.keys().__contains__('K') and \
                result.keys().__contains__('Sums') and \
                result.keys().__contains__('Muls'):                                     # Проверяем, что получили нужный формат
            return result
        else:
            raise TypeError('Json format is incorrect')

    def from_xml(self, string: str):
        document: Document = parseString(string)                                        # Используем библиотеку xml для парсинга
        node = document.documentElement                                                 # получаем дерево Document
        k = document.getElementsByTagName('K')[0]
        if k.firstChild.nodeType == node.TEXT_NODE:                                     # Далее получаем из дерева нужные величины
            k = int(document.getElementsByTagName('K')[0].firstChild.data)
        else:
            raise TypeError('XML format is incorrect')
        sums = document.getElementsByTagName('Sums')[0]
        sumsList = []
        for child in sums.childNodes:
            if child.nodeType == node.ELEMENT_NODE and child.nodeName == 'decimal' \
                    and child.firstChild.nodeType == node.TEXT_NODE:
                sumsList.append(float(child.firstChild.data))
            else:
                raise TypeError('XML format is incorrect')
        muls = document.getElementsByTagName('Muls')[0]
        mulsList = []
        for child in muls.childNodes:
            if child.nodeType == node.ELEMENT_NODE and child.nodeName == 'int' \
                    and child.firstChild.nodeType == node.TEXT_NODE:
                mulsList.append(int(child.firstChild.data))
            else:
                raise TypeError('XML format is incorrect')
        return {
            'K': k,
            'Muls': mulsList,
            'Sums': sumsList
        }
