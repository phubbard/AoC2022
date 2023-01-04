
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

def parse_data(data_lines):
    lines = data_lines.strip().split("\n")
    out_lines = []

    for line in lines:
        splitted = line.split(": ")
        monkey = splitted[0]
        rest   = splitted[1]

        rest_split = rest.split(" ")

        if False:
            pass
        elif len(rest_split) == 1:
            out_lines += [ f"def {monkey}(): return {rest}" ]
        elif len(rest_split) == 3:
            out_lines += [ f"def {monkey}(): return {rest_split[0]}() {rest_split[1]} {rest_split[2]}()" ]
        else:
            out_lines += [ f"raise Exception('ddd')"]

    out_lines += [ "print (root())"]
    return out_lines


if __name__ == '__main__':

    if False:
        pure_input = sample_data
    else:
        pure_input = open(DATAFILE, 'r').read()

    gen_lines = parse_data(pure_input)

    as_file = '\n'.join(gen_lines)

    with open("21_generated.py", 'w') as dest_file:
        dest_file.write(as_file)

