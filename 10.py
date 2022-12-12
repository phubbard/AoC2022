
test_program = """noop
addx 3
addx -5"""


def calc_ss(signal):
    ss = 0
    for idx in [20, 60, 100, 140, 180, 220]:
        reg_val = signal[idx]
        cur_ss = idx * reg_val
        ss += cur_ss

    return ss


def cpu_sim():
    signal = [1,1]
    x = 1

    medium_datafile = "./data/10-b.txt"
    datafile = "./data/10.txt"

    for instruction in open(datafile, 'r'):
    # for instruction in test_program.split('\n'):
        if len(instruction) == 0:
            continue

        tokens = instruction.strip().split(' ')
        if tokens[0] == 'noop':
            signal.append(x)
        else:
            signal.append(x)
            x = x + int(tokens[1])
            signal.append(x)

    # print(signal)
    # assert signal == [1, 1, 1, 4, 4, -1]
    print(calc_ss(signal))


if __name__ == '__main__':
    cpu_sim()