from collections import deque

#
# items = [
#     deque([79, 98]),
#     deque([54, 65, 75, 74]),
#     deque([79, 60, 97]),
#     deque([74])
# ]
#
# operators = [
#     lambda x: x * 19,
#     lambda x: x + 6,
#     lambda x: x * x,
#     lambda x: x + 3
# ]
#
# # divisor, true dest, false dest
# tests = [
#     (23,2,3),
#     (19,2,0),
#     (13,1,3),
#     (17,0,1)
# ]
#
# inspection_counts = [0, 0, 0, 0]

items = [
    deque([77, 69, 76, 77, 50, 58]),
    deque([75, 70, 82, 83, 96, 64, 62]),
    deque([53]),
    deque([85, 64, 93, 64, 99]),
    deque([61, 92, 71]),
    deque([79, 73, 50, 90]),
    deque([50, 89]),
    deque([83, 56, 64, 58, 93, 91, 56, 65])
]

operators = [
    lambda x: x * 11,
    lambda x: x + 8,
    lambda x: x * 3,
    lambda x: x + 4,
    lambda x: x * x,
    lambda x: x + 2,
    lambda x: x + 3,
    lambda x: x + 5
]

tests = [
    (5,1,5),
    (17,5,6),
    (2,0,7),
    (7,7,2),
    (3,2,3),
    (11,4,6),
    (13,4,3),
    (19,1,0)
]

inspection_counts = [0 for x in range(8)]


def game_rounds(num_rounds: int):
    global tests, inspection_counts, items
    lcm = 1
    for idx in range(len(tests)):
        lcm *= tests[idx][0]
    print(f'LCM {lcm}')

    for round in range(num_rounds):
        for idx in range(len(items)):
            while len(items[idx]) > 0:
                inspection_counts[idx] += 1
                initial_worry_level = items[idx].popleft()
                f = operators[idx]
                # yay remainder theorem
                worry_level = f(initial_worry_level) % lcm
                if worry_level % tests[idx][0] == 0:
                    next_monkey = tests[idx][1]
                else:
                    next_monkey = tests[idx][2]
                items[next_monkey].append(worry_level)
        if round % 250 == 0:
            print(f"Round {round}")

    for monkey in items:
        print(f"monkey {monkey}")
    print(f"counts {inspection_counts}")

    inspection_counts.sort(reverse=True)
    print(f"sorted counts {inspection_counts}")
    monkey_business = inspection_counts[0] * inspection_counts[1]
    print(monkey_business)


if __name__ == '__main__':
    game_rounds(10000)

