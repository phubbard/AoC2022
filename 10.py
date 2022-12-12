
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


def print_sprite(sprite_pos):
    rc = ''
    for x in range(40):
        if sprite_pos in range(x - 1, x + 2):
            rc += '#'
        else:
            rc += '.'
    print(f'Sprite position: {rc}')


def visualize_signal(signal):
    cycle = 1
    sprite_pos = 1

    for row in range(6):
        output_row = ''
        for col in range(40):
            # print_sprite(sprite_pos)
            if col in range(sprite_pos - 1, sprite_pos + 2):
                  output_row += '#'
            else:
                output_row += '.'
            cycle += 1
            sprite_pos = signal[cycle]

        print(output_row)


def cpu_sim():
    signal = [1, 1]
    x = 1

    medium_datafile = "./data/10-b.txt"
    datafile = "./data/10.txt"

    for instruction in open(medium_datafile, 'r'):
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

    print(signal)
    # assert signal == [1, 1, 1, 4, 4, -1]
    print(calc_ss(signal))
    visualize_signal(signal)

if __name__ == '__main__':
    cpu_sim()