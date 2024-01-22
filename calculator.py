from typing import Iterable


class Node:
    def __init__(self, value=None):
        self.info = value
        self.next = None

    def __repr__(self):
        return self.info


class Stack:
    def __init__(self):
        self._head = Node('head')
        self._size = 0

    def push(self, value):
        node = Node(value)
        node.next = self._head.next
        self._head.next = node
        self._size += 1

    def is_empty(self):
        return self._size == 0

    def pop(self):
        if self.is_empty():
            raise Exception('Are you gay?')
        _remove = self._head.next
        self._head.next = self._head.next.next
        self._size -= 1
        return _remove.info

    def size(self):
        return self._size

    def last_el(self):
        if self._head.next is None:
            return None
        return self._head.next.info

    def print_stack(self):
        """Prints stack in the follow form:

            |     |
            | ")" |
            | "+" |
            | "(" |
            |_____|

        """

        print('|     |')
        p = self._head
        while p.next is not None:
            p = p.next
            print(f'| "{p.info}" |')
        print('|_____|')


def _input_str() -> str:
    return input('Enter the expression: ')


def _all_symbols_are_correct(expr: str) -> bool:
    for symbol in expr:
        if not any([symbol == i for i in '0123456789+-/*()']):
            return False
    return True


def _del_all_spaces(expr: str) -> str:
    return ''.join([el for el in expr if el != ' '])


def _is_numeric(symbol: str) -> bool:
    if symbol[0] == '-' and len(symbol) > 1:
        return True
    return any([symbol[0] == i for i in '0123456789'])


def _is_sign(symbol: str) -> bool:
    return any([symbol == i for i in '+-*/'])


def _string_to_infix_list(expr: str) -> Iterable:
    num = ''
    infix_list = []

    for i, symbol in enumerate(expr):
        if _is_numeric(symbol):
            num += symbol
        else:
            if num != '':
                infix_list.append(num)
                num = ''
            if any([symbol == signs for signs in '+-/*()']):
                if symbol == '-' and (i == 0 or expr[i-1] == '('):
                    num += symbol
                else:
                    infix_list.append(symbol)
    if num != '':
        infix_list.append(num)
    return infix_list


def _is_high_priority(symbol: str) -> bool:
    return symbol == '*' or symbol == '/'


def _infix_to_postfix_list(infix_list: Iterable) -> Iterable:
    postfix_expr = []
    parenthesis_signs_stack = Stack()
    for element in infix_list:
        if _is_numeric(element):
            postfix_expr.append(int(element))

        elif _is_sign(element):
            if element == '+' or element == '-':
                while _is_sign(parenthesis_signs_stack.last_el()):
                    postfix_expr.append(parenthesis_signs_stack.pop())
                parenthesis_signs_stack.push(element)
            else:
                while _is_high_priority(parenthesis_signs_stack.last_el()):
                    postfix_expr.append(parenthesis_signs_stack.pop())
                parenthesis_signs_stack.push(element)

        elif element == '(':
            parenthesis_signs_stack.push(element)
        elif element == ')':
            while _is_sign(parenthesis_signs_stack.last_el()):
                postfix_expr.append(parenthesis_signs_stack.pop())
            parenthesis_signs_stack.pop()
    while _is_sign(parenthesis_signs_stack.last_el()):
        postfix_expr.append(parenthesis_signs_stack.pop())

    if parenthesis_signs_stack.last_el():
        raise Exception('Stack has at least one more element.')

    return postfix_expr


def _eval_postfix(expr: Iterable) -> float:
    eval_stack = Stack()
    for el in expr:
        if isinstance(el, int):
            eval_stack.push(el)
        elif el == '+':
            eval_stack.push(eval_stack.pop() + eval_stack.pop())
        elif el == '*':
            eval_stack.push(eval_stack.pop() * eval_stack.pop())
        elif el == '-':
            s = eval_stack.pop()
            f = eval_stack.pop()
            eval_stack.push(f-s)
        elif el == '/':
            s = eval_stack.pop()
            f = eval_stack.pop()
            eval_stack.push(f/s)

    if eval_stack.is_empty():
        return 0
    return int(eval_stack.pop())


def main():
    str_expression = _del_all_spaces(_input_str())

    while not _all_symbols_are_correct(str_expression):
        print('Wrong input, try again.')
        str_expression = _del_all_spaces(_input_str())

    infix_expression = _string_to_infix_list(str_expression)
    postfix_expression = _infix_to_postfix_list(infix_expression)
    print(_eval_postfix(postfix_expression))


if __name__ == '__main__':
    main()

