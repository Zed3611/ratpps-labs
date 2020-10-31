import json
from xml.etree.ElementTree import Element, SubElement, tostring
from Input import Input


class Output:                                                                   # Объект выходных данных
    def __init__(self, _input: Input):                                          # Инициализируется из объекта Input
        self.serialization_type = _input.serialization_type
        self.sorted_inputs: list[float] = sorted(_input.sums + _input.muls)
        self.mul_result: int = production(_input.muls)
        self.sum_result: float = round(sum(_input.sums) * _input.k, 2)

    def to_json(self):                                                          # Метод для получения json
        return json.dumps({
            'SumResult': self.sum_result,
            'MulResult': self.mul_result,
            'SortedInputs': self.sorted_inputs
        }, separators=(',', ':'))

    def to_xml(self):                                                            # Метод для получения xml
        output = Element('Output')
        sum_result = SubElement(output, 'SumResult')
        sum_result.text = str(self.sum_result)
        mul_result = SubElement(output, 'MulResult')
        mul_result.text = str(self.mul_result)
        sorted_inputs = SubElement(output, 'SortedInputs')
        for i in self.sorted_inputs:
            decimal = SubElement(sorted_inputs, 'decimal')
            decimal.text = str(i)
        return tostring(output, encoding='unicode')

    def __str__(self):
        if self.serialization_type == 'Json':
            return self.to_json()
        else:
            return self.to_xml()


def production(lst: list[int]):
    result = 1
    for i in lst:
        result *= i
    return result
