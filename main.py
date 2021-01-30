import numpy as np


class State:
    def __init__(self):
        self.data = np.array([[3, 3], [0, 0]])
        self.rule = 0
        self.shore = 0
        self.terminal = False
        self.next = None

    def copy(self) -> 'State':
        s = State()
        s.shore = self.shore
        s.terminal = self.terminal
        s.data = self.data.copy()
        return s

    def __eq__(self, other: 'State'):
        return np.all(self.data == other.data) and self.shore == other.shore

    def __repr__(self):
        return f"Состояние:" \
               f" лодка у берега #{self.shore + 1}," \
               f" левый берег {self.data[0, :]}," \
               f" правый берег {self.data[1, :]}"

    @staticmethod
    def change_shore(shore: int) -> int:
        return 0 if shore else 1


def main():
    print("\t *** Миссионеры и людоеды ***\n")

    # Начальное состояние
    print("Начальное состояние:")
    rule, rules = 0, 5
    state = State()
    print(state)

    # Решение
    print("Идёт моделирование...\n")
    story = [state]
    solve(state, story, rule, rules)

    # Результаты
    print("Результат:")
    print_result(state)

    return 0


def solve(s: State, story: list, rule: int, rules: int):
    if is_terminal(s):
        s.terminal = True
        return

    for i in range(1, rules + 1):
        if i == rule:
            continue

        if i == 1 and is_rule_1(s):
            ns = make_rule_1(s)
        elif i == 2 and is_rule_2(s):
            ns = make_rule_2(s)
        elif i == 3 and is_rule_3(s):
            ns = make_rule_3(s)
        elif i == 4 and is_rule_4(s):
            ns = make_rule_4(s)
        elif i == 5 and is_rule_5(s):
            ns = make_rule_5(s)
        else:
            ns = None

        if ns:
            if check_in(story, ns):
                continue
            story.append(ns)

            solve(ns, story, i, rules)

            if ns.terminal:
                s.rule = i
                s.next = ns
                s.terminal = True
                return


def is_rule_1(s: State) -> bool:
    if s.data[s.shore, 0] == 0:
        return False
    if s.data[s.shore, 1] > s.data[s.shore, 0] - 1 != 0:
        return False
    other_shore = State.change_shore(s.shore)
    if s.data[other_shore, 1] > s.data[other_shore, 0] + 1:
        return False
    return True


def make_rule_1(s: State) -> State:
    ns = s.copy()
    ns.data[s.shore, 0] -= 1
    ns.shore = State.change_shore(s.shore)
    ns.data[ns.shore, 0] += 1
    return ns


def is_rule_2(s: State) -> bool:
    if s.data[s.shore, 1] == 0:
        return False
    other_shore = State.change_shore(s.shore)
    if s.data[other_shore, 1] + 1 > s.data[other_shore, 0] != 0:
        return False
    return True


def make_rule_2(s: State) -> State:
    ns = s.copy()
    ns.data[s.shore, 1] -= 1
    ns.shore = State.change_shore(s.shore)
    ns.data[ns.shore, 1] += 1
    return ns


def is_rule_3(s: State) -> bool:
    if s.data[s.shore, 0] == 0 or s.data[s.shore, 1] == 0:
        return False
    if s.data[s.shore, 1] - 1 > s.data[s.shore, 0] - 1 != 0:
        return False
    other_shore = State.change_shore(s.shore)
    if s.data[other_shore, 1] + 1 > s.data[other_shore, 0] + 1:
        return False
    return True


def make_rule_3(s: State) -> State:
    ns = s.copy()
    ns.data[s.shore, :] -= 1
    ns.shore = State.change_shore(s.shore)
    ns.data[ns.shore, :] += 1
    return ns


def is_rule_4(s: State) -> bool:
    if s.data[s.shore, 0] < 2:
        return False
    if s.data[s.shore, 1] > s.data[s.shore, 0] - 2 != 0:
        return False
    other_shore = State.change_shore(s.shore)
    if s.data[other_shore, 1] > s.data[other_shore, 0] + 2:
        return False
    return True


def make_rule_4(s: State) -> State:
    ns = s.copy()
    ns.data[s.shore, 0] -= 2
    ns.shore = State.change_shore(s.shore)
    ns.data[ns.shore, 0] += 2
    return ns


def is_rule_5(s: State) -> bool:
    if s.data[s.shore, 1] < 2:
        return False
    if s.data[s.shore, 1] - 2 > s.data[s.shore, 0] != 0:
        return False
    other_shore = State.change_shore(s.shore)
    if s.data[other_shore, 1] + 2 > s.data[other_shore, 0] != 0:
        return False
    return True


def make_rule_5(s: State) -> State:
    ns = s.copy()
    ns.data[s.shore, 1] -= 2
    ns.shore = State.change_shore(s.shore)
    ns.data[ns.shore, 1] += 2
    return ns


def check_in(story, s: State) -> bool:
    for st in story:
        if st == s:
            return True
    return False


def is_terminal(s: State) -> bool:
    return np.all(s.data[1, :] == 3)


def print_result(s: State):
    arrows = "->", "<-"
    x = s
    i = 1
    while x.next:
        print(f"Шаг #{i}\t{arrows[x.shore]}: {get_rule_text(x.rule)} ==> {x.next}")
        x = x.next
        i += 1


def get_rule_text(rule: int) -> str:
    if rule == 0: return "ничего не делать"
    if rule == 1: return "(П1) переправить 1 миссионера"
    if rule == 2: return "(П2) переправить 1 людоеда"
    if rule == 3: return "(П3) переправить миссионера и людоеда"
    if rule == 4: return "(П4) переправить 2 миссионера"
    if rule == 5: return "(П5) переправить 2 людоеда"
    return "Ошибка! Неизвестное правило..."


if __name__ == '__main__':
    main()
