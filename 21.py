from dataclasses import dataclass
from anytree import Node, RenderTree, AsciiStyle, search

sample_data = """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32"""
sample_answer = 152
DATAFILE = './data/21.txt'


@dataclass
class OperatorMonkey:
    name: str
    operator: str
    lhs: str
    rhs: str


@dataclass
class ConstMonkey:
    name: str
    constant: int


def find_by_name(monkey_array, name):
    for monkey in monkey_array:
        if monkey.name == name:
            return monkey


def build_tree(root, monkeys):
    if not root:
        return

    if hasattr(root, 'lhs'):
        # Op monkey - construct left node and recurse
        left_monkey = find_by_name(monkeys, root.lhs)
        left_node = Node(name=left_monkey.name, parent=root)
        if hasattr(left_monkey, 'lhs'):
            left_node.lhs = left_monkey.lhs
            left_node.rhs = left_monkey.rhs
            left_node.operator = left_monkey.operator
            return build_tree(left_node, monkeys)
        else:
            left_node.constant = left_monkey.constant

        right_monkey = find_by_name(monkeys, root.rhs)
        right_node = Node(name=right_monkey.name, parent=root)
        if hasattr(right_monkey, 'rhs'):
            right_node.lhs = right_monkey.lhs
            right_node.rhs = right_monkey.rhs
            right_node.operator = right_monkey.operator
            return build_tree(right_node, monkeys)
        else:
            right_node.constant = right_monkey.constant


def parse_data(data_lines):
    const_monkeys = []
    op_monkeys = []
    all_monkeys = []

    for line in data_lines:
        tokens = line.split(':')
        if tokens[1].strip().isdigit():
            const_monkeys.append(ConstMonkey(tokens[0], int(tokens[1])))
        else:
            line_tokens = tokens[1].strip().split(' ')
            op_monkeys.append(OperatorMonkey(tokens[0], line_tokens[1], line_tokens[0], line_tokens[2]))
    all_monkeys.extend(const_monkeys)
    all_monkeys.extend(op_monkeys)

    # We have arrays of monkeys. Now we need to build a dependency graph
    root_monkey = find_by_name(op_monkeys, 'root')
    root = Node('root', lhs=root_monkey.lhs, rhs=root_monkey.rhs)
    build_tree(root, all_monkeys)
    print(RenderTree(root, style=AsciiStyle()))


if __name__ == '__main__':
    parse_data(sample_data.split('\n'))