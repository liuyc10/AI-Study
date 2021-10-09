import functools
import heapq
import math
import random

from gomoku_score_sheet import score_sheet

inf = float('inf')
delta_xy = [(1, 1), (1, 0), (0, 1), (1, -1)]


def distance(a, b):
    """The distance between two (x, y) points."""
    xA, yA = a
    xB, yB = b
    return math.hypot((xA - xB), (yA - yB))


def memoize(fn, slot=None, maxsize=32):
    """Memoize fn: make it remember the computed value for any argument list.
    If slot is specified, store result in that slot of first argument.
    If slot is false, use lru_cache for caching the values."""
    if slot:
        def memoized_fn(obj, *args):
            if hasattr(obj, slot):
                return getattr(obj, slot)
            else:
                val = fn(obj, *args)
                setattr(obj, slot, val)
                return val
    else:
        @functools.lru_cache(maxsize=maxsize)
        def memoized_fn(*args):
            return fn(*args)

    return memoized_fn


class PriorityQueue:

    def __init__(self, order='min', f=lambda x: x):
        self.heap = []
        if order == 'min':
            self.f = f
        elif order == 'max':
            self.f = lambda x: -f(x)
        else:
            raise ValueError('min or max only')

    def append(self, item):
        heapq.heappush(self.heap, (self.f(item), item))

    def extend(self, items):
        for item in items:
            self.append(item)

    def pop(self):
        if self.heap:
            return heapq.heappop(self.heap)[1]  # heapq.heappush(self.heap)return a tuple（priority, item）
        else:
            raise Exception('empty queue')

    def __len__(self):
        return len(self.heap)

    def __contains__(self, key):
        return any([item == key for _, item in self.heap])  # ‘_’ underline is a var which useless here

    def __getitem__(self, key):
        for value, item in self.heap:
            if item == key:
                return value
        raise KeyError(str(key) + 'is not in queue')

    def __delitem__(self, key):
        try:
            del self.heap[[item == key for _, item in self.heap].index(True)]
            """
            result = []
            for _, item in self.heap:
                if key == item:
                    result.append(True)
                else:
                    result.append(false)                    
                index = result.index(True)
                del self.heap[index]
                """
        except ValueError:
            raise KeyError(str(key) + 'is not in queue')
        heapq.heapify(self.heap)


def move_reverse(moves):
    x = reversed(moves)
    reverse_list = []
    for move in x:
        if move == 'UP':
            reverse_list.append('DOWN')
        elif move == 'DOWN':
            reverse_list.append('UP')
        elif move == 'RIGHT':
            reverse_list.append('LEFT')
        elif move == 'LEFT':
            reverse_list.append('RIGHT')
    return reverse_list


def random_selection(population, weights):
    total = sum(w for _, w in zip(population, weights))
    r = random.uniform(0, total)
    target = 0
    for c, w in zip(population, weights):
        if target + w > r:
            return c
        target += w


def reproduce(x, y):
    n = len(x)
    c = random.randrange(1, n)
    return x[:c] + y[c:]


def mutation(x, dna, rate):
    if random.uniform(0, 1) < rate:
        return x
    len_x = len(x)
    c = random.randrange(1, len_x)
    m = random.choice(dna)

    return x[:c] + [m] + x[c + 1:]


def seq_to_score(seq):
    score = 0
    for k, v in score_sheet.items():
        for a, b in v.items():
            x = list(a)
            r = [x == seq[i:i + len(x)] for i in range(0, len(seq) - len(x) + 1)]

            if any(r):
                # print(x)
                score = score + b
    return score


def get_score(board, move, player):
    score = 0
    for (delta_x, delta_y) in delta_xy:
        x, y = move
        seq = []
        for i in range(5):
            point = board.get((x, y))
            if point == player:
                seq.append(1)
            elif point is None:
                seq.append(0)
            else:
                seq.append(-1)
                break
            x = x + delta_x
            y = y + delta_y
        seq.reverse()
        x, y = move
        seq = seq[0:-1]
        for i in range(5):
            point = board.get((x, y))
            if point == player:
                seq.append(1)
            elif point is None:
                seq.append(0)
            else:
                seq.append(-1)
                break
            x = x - delta_x
            y = y - delta_y
        score = score + seq_to_score(seq)
    return score


def k_in_row(board, move, player, delta_x_y, k=5):
    (delta_x, delta_y) = delta_x_y
    x, y = move
    n = 0  # n is number of moves in row
    while board.get((x, y)) == player:
        n += 1
        x, y = x + delta_x, y + delta_y
    x, y = move
    while board.get((x, y)) == player:
        n += 1
        x, y = x - delta_x, y - delta_y
    n -= 1  # Because we counted move itself twice
    return n >= k


def compute_utility(board, move, player):
    if (k_in_row(board, move, player, (0, 1)) or
            k_in_row(board, move, player, (1, 0)) or
            k_in_row(board, move, player, (1, -1)) or
            k_in_row(board, move, player, (1, 1))):
        return 100000

        # return +100000 if player == 'X' else -100000
    else:
        score = get_score(board, move, player)
        return score
        # return score if player == 'X' else -score


def extend_moves(move, moves, in_6_step):
    x_0, y_0 = move
    for key in moves.keys():
        if moves[key] == 1:
            continue
        (x, y) = key
        if in_6_step:
            offset = 1
        else:
            offset = 2
        if abs(x - x_0) <= offset and abs(y - y_0) <= offset:
            moves[key] = 1

    return moves


def ucb(n, C=1.4):
    return inf if n.N == 0 else n.U / n.N + C * math.sqrt(math.log(n.parent.N) / n.N)
