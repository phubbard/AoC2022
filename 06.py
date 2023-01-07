

test_data = [
    {'input': 'mjqjpqmgbljsphdztnvjfqwrcgsmlb', 'answer': 7, 'msg': 19},
    {'input': 'bvwbjplbgvbhsrlpgdmjqwftvncz', 'answer': 5, 'msg': 23},
    {'input': 'nppdvjthqldpwncqszvftbrmjlhg', 'answer': 6, 'msg': 23},
    {'input': 'nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 'answer': 10, 'msg': 29},
    {'input': 'zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 'answer': 11, 'msg': 26}
]

DATAFILE = './data/6.txt'


def find_unique(input, seq_len):
    for idx in range(len(input)):
        window = input[idx: idx + seq_len]
        set_buf = set(window)
        if len(set_buf) == seq_len:
            return idx + seq_len


def find_marker(input):
    return find_unique(input, 4)


def find_message(input):
    return find_unique(input, 14)


def run_tests():
    for test in test_data:
        answer = find_marker(test['input'])
        assert answer == test['answer']
        msg = find_message(test['input'])
        assert msg == test['msg']


def run_step_one():
    data = open(DATAFILE, 'r').read()
    print(find_marker(data))
    print(find_message(data))


if __name__ == '__main__':
    run_tests()
    run_step_one()