
from operator import itemgetter
from anytree import AnyNode, RenderTree, AsciiStyle, search


MAX_DIRSIZE = 100000
P1_TOTAL = 0
FS_TOTAL = 70_000_000
FS_NEEDED = 30_000_000

root = AnyNode(name='/', type='d', size=0)
cwd: AnyNode = root

DATAFILE = './data/7.txt'

test_data = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""


def cd(dest_dir):
    global cwd

    if dest_dir.startswith('/'):
        # Absolute
        cwd = search.find(root, lambda node: node.name == dest_dir, maxlevel=1)
        return cwd

    # Relative move up or down
    if dest_dir == '..':
        cwd = cwd.parent
        return cwd

    for entry in cwd.children:
        if entry.name == dest_dir and entry.type == 'd':
            cwd = entry
            return cwd


def calc_size(directory):
    # Recursively calculate the size of a directory
    global P1_TOTAL

    if not directory:
        return 0

    if directory.type == 'f':
        return 0

    cur_size = 0
    for entry in directory.children:
        if entry.type == 'f':
            cur_size += entry.size

        if entry.type == 'd':
            cur_size += calc_size(entry)

    if cur_size < MAX_DIRSIZE:
        P1_TOTAL += cur_size
        # print(f"{cur_size} bytes found in {directory.name}")

    directory.size = cur_size
    return cur_size


def parse_history(data_lines):
    global cwd

    for line in data_lines:
        # print(f"Working on {line}")
        # print(RenderTree(root, style=AsciiStyle()))

        if len(line) == 0:
            continue

        tokens = line.strip().split(' ')
        if tokens[0] == '$':
            if tokens[1] == 'cd':
                cd(tokens[2])
                continue
            if tokens[1] == 'ls':
                continue

        # Parsing ls output
        if tokens[0] == 'dir':
            if search.find(cwd, lambda node: node.name == tokens[1], maxlevel=1) is None:
                AnyNode(name=tokens[1], parent=cwd, type='d', size=0)
            continue
        # File
        if search.find(cwd, lambda node: node.name == tokens[1], maxlevel=1) is None:
            AnyNode(name=tokens[1], parent=cwd, size=int(tokens[0]), type='f')
        else:  # Dup - FIXME
            pass

    # print(RenderTree(root, style=AsciiStyle()))
    size = calc_size(root)
    print(f"Total size is {size} {P1_TOTAL} eligible")
    return size

dir_list = []


def flatten_tree(cur_node):
    global dir_list
    if not cur_node:
        return
    if not cur_node.children:
        return

    # Flatten tree into sorted name,size list to solve part two
    for entry in cur_node.children:
        if entry.type == 'd':
            dir_list.append({'size': calc_size(entry), 'name': entry.name})
            flatten_tree(entry)


def find_p2_dir(free):
    global dir_list
    flatten_tree(root)
    dir_list.sort(key=itemgetter('size'))
    # for item in dir_list:
    #     print(item)

    for item in dir_list:
        if item['size'] + free < FS_NEEDED:
            continue
        print(f'{item} wins')
        break


def run_test_data():
    parse_history(test_data.split('\n'))


def run_p1_data():
    free = FS_TOTAL - parse_history(open(DATAFILE, 'r').readlines())
    find_p2_dir(free)


if __name__ == '__main__':
    # run_test_data()
    run_p1_data()