import sympy

human = sympy.Symbol('human')

def root(): return pppw() + sjmn()
def dbpl(): return 5
def cczh(): return sllz() + lgvd()
def zczc(): return 2
def ptdq(): return humn() - dvpt()
def dvpt(): return 3
def lfqf(): return 4
def humn(): return human # return 5
def ljgn(): return 2
def sjmn(): return drzm() * dbpl()
def sllz(): return 4
def pppw(): return cczh() / lfqf()
def lgvd(): return ljgn() * ptdq()
def drzm(): return hmdt() - zczc()
def hmdt(): return 32

answer = sympy.solveset(human - 5, human)
print(f" The draft is {answer}")

answer = sympy.solveset(pppw() - sjmn(), human)
print(f" The answer is {answer}")
