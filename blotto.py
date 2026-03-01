import random
# import numpy as np

tower_pts = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
champion_pool = []
# Score is positive in the direction of solution 1 (s1)
# def score(s1, s2):
#     score = 0
#     for i in range(10):
#         if s1[i] > s2[i]:
#             score += tower_pts[i]
#         elif s1[i] < s2[i]:
#             score -= tower_pts[i]
#     return score

# The last (highest-indexed) tower a player wins is worth negative points equal to its index
def score(s1, s2, verbose = False):
    s1_score = []
    s2_score = []

    for i in range(10):
        if s1[i] > s2[i]:
            s1_score.append(tower_pts[i])
        elif s1[i] < s2[i]:
            s2_score.append(tower_pts[i])
    if s1_score:
        s1_score[-1] *= -1
    if s2_score:
        s2_score[-1] *= -1

    if verbose:
        print(s1)
        print(s2)
        print(s1_score, s2_score)

    return sum(s1_score) - sum(s2_score)


# ── Strategy generation ────────────────────────────────────────────────────────

def random_strategy(total: int = 100, towers: int = 10) -> list[int]:
    """Generate a random valid allocation: non-negative integers summing to `total`."""
    # Stars-and-bars: place (total) soldiers across (towers) bins
    towers = 9
    cuts = sorted(random.sample(range(1, total + towers), towers - 1))
    cuts = [0] + cuts + [total + towers]
    strat = [cuts[i + 1] - cuts[i] - 1 for i in range(towers)]
    return strat + [0]


def mutate(strategy: list[int], strength: int = 10) -> list[int]:
    """
    Create a variant of `strategy` by moving `strength` soldiers randomly.
    Picks a random donor tower, takes soldiers from it, and gives them to
    a random recipient tower, then clamps all values to ≥ 0 and keeps total = 100.
    """
    s = strategy[:]
    towers = len(s)

    # Shift up to `strength` soldiers from one random tower to another
    moves = random.randint(1, strength)
    for _ in range(moves):
        donor = random.randrange(towers)
        recipient = random.randrange(towers)
        if donor == recipient:
            continue
        transfer = random.randint(0, s[donor])
        s[donor] -= transfer
        s[recipient] += transfer

    return s


def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0


# ── Evaluation ────────────────────────────────────────────────────────────────

def tournament_score(strategy: list[int], pool: list[list[int]]) -> float:
    """Average score of `strategy` against every opponent in `pool`."""
    return sum(sign(score(strategy, opponent)) for opponent in pool)


# ── Main optimizer ────────────────────────────────────────────────────────────

def optimize(k: int = 10, pool_size: int = 1000, mutation_strength: int = 10,
             total: int = 100, towers: int = 10) -> tuple[list[int], float]:
    """
    Evolutionary optimizer for Colonel Blotto.

    Algorithm
    ---------
    1. Generate `pool_size` random strategies.
    2. Pick the best-scoring one (champion) via intra-pool tournament.
    3. For each of `k` iterations:
       a. Generate `pool_size` mutations from the champion.
       b. Evaluate each mutation against the new pool.
       c. Update champion to the best mutation.
    4. Return (champion, champion_score).

    Parameters
    ----------
    k                : number of evolutionary iterations
    pool_size        : strategies generated per iteration
    mutation_strength: max soldiers shifted per mutation step
    total            : soldier budget (default 100)
    towers           : number of towers (default 10)
    """

    print(f"[Blotto Optimizer]  k={k}  pool_size={pool_size}  mutation_strength={mutation_strength}")

    # ── Iteration 0: random seed pool ─────────────────────────────────────────
    pool = [random_strategy(total, towers) for _ in range(pool_size)]
    scores = [tournament_score(s, pool) for s in pool]

    best_idx = max(range(pool_size), key=lambda i: scores[i])
    champion = pool[best_idx]
    champion_score = scores[best_idx]

    print(f"  iter 0 (seed)  -> champion score = {champion_score:.4f}  strategy = {champion}")

    # ── Iterations 1..k: mutate & evolve ──────────────────────────────────────
    for iteration in range(1, k + 1):
        pool = [mutate(champion, mutation_strength) for _ in range(pool_size)]
        scores = [tournament_score(s, pool) for s in pool]

        best_idx = max(range(pool_size), key=lambda i: scores[i])
        new_champion = pool[best_idx]
        new_score = scores[best_idx]

        print(f"  iter {iteration:>2}         -> champion score = {new_score:.4f}  strategy = {new_champion}")
        champion = new_champion
        champion_score = new_score
        champion_pool.append(champion)


        print("Submission score: " + str(tournament_score([1,11,3,15,5,37,13,15,0,0], pool)))
        print("Submission score: " + str(tournament_score([3, 1, 2, 6, 14, 23, 24, 17, 10, 0], pool)))

    # ── Sanity checks ─────────────────────────────────────────────────────────
    assert all(s >= 0 for s in champion), "Strategy has negative values!"
    assert sum(champion) <= total, f"Strategy uses {sum(champion)} > {total} soldiers!"

    return champion, champion_score


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":

    # sanity check
    # s1 = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10] # -1
    # s2 = [5, 10, 10, 10, 10, 10, 10, 10, 10, 15] # -10
    # print(score(s1, s2))
    # assert score(s1, s2) == 9

    # print(score([0, 2, 1, 4, 16, 17, 19, 12, 13, 16], [0, 3, 1, 8, 11, 12, 15, 18, 19, 13], True))
    #        3     5    7     9  10
    # 00 02 01 04 16 17 19 12 13 16
    # 01 11 03 15 05 37 13 15 00 01
    #  1  2     4    6      8

    # print(score([0, 1, 7, 7, 4, 14, 17, 20, 27, 3], [0, 0, 0, 4, 2, 6, 16, 16, 20, 36]))
    # assert 2 == 3

    # [0, 4, 4, 3, 4, 20, 2, 24, 17, 22])
    # [1, 5, 5, 4, 5, 0, 3, 42, 35, 0]

    # [0, 0, 1, 6, 10, 2, 9, 22, 29, 21]
    # [3, 4, 5, 10, 15, 20, 20, 23, 0, 0]


    champion, champ_score = optimize(k=50, pool_size=1000, mutation_strength=30)

    print()
    print("=" * 60)
    print(f"Champion strategy : {champion}")
    print(f"Soldiers used     : {sum(champion)} / 100")
    print(f"Tournament score  : {champ_score:.4f}")
    print("=" * 60)

    # champion_pool = [[0, 1, 7, 7, 4, 14, 17, 20, 27, 3], [1, 2, 4, 6, 2, 12, 12, 11, 24, 26], [0, 5, 0, 4, 5, 14, 10, 17, 8, 37], [0, 1, 2, 2, 2, 11, 6, 14, 28, 34], [1, 1, 7, 5, 10, 1, 18, 8, 20, 29], [0, 2, 1, 5, 2, 11, 12, 17, 24, 26], [5, 4, 0, 4, 5, 13, 19, 17, 23, 10], [1, 1, 2, 3, 2, 14, 12, 14, 25, 26], [0, 1, 4, 3, 8, 10, 19, 14, 10, 31], [0, 1, 2, 3, 1, 10, 5, 21, 23, 34], [0, 1, 2, 3, 8, 10, 5, 18, 20, 33], [1, 0, 4, 6, 7, 4, 23, 20, 22, 13], [1, 1, 1, 3, 7, 12, 6, 23, 30, 16], [0, 0, 0, 3, 5, 10, 5, 20, 26, 31], [0, 0, 3, 5, 8, 13, 9, 15, 6, 41], [0, 0, 3, 8, 4, 14, 21, 5, 31, 14], [0, 0, 2, 0, 2, 11, 7, 14, 29, 35], [1, 2, 9, 5, 10, 3, 13, 7, 24, 26], [0, 0, 1, 2, 5, 11, 12, 17, 25, 27], [0, 2, 2, 12, 7, 4, 14, 24, 19, 16], [0, 0, 1, 2, 5, 6, 12, 18, 25, 31], [1, 0, 7, 3, 11, 4, 20, 12, 32, 10], [1, 1, 8, 6, 11, 14, 8, 14, 13, 24], [1, 1, 2, 4, 8, 21, 1, 26, 20, 16], [0, 0, 1, 1, 6, 3, 7, 14, 31, 37], [1, 1, 3, 1, 10, 17, 18, 8, 15, 26], [0, 1, 1, 4, 5, 4, 14, 13, 22, 36], [1, 1, 0, 11, 13, 5, 17, 6, 15, 31], [0, 0, 4, 2, 9, 12, 11, 10, 28, 24], [1, 1, 4, 3, 8, 10, 5, 18, 19, 31], [2, 0, 2, 4, 5, 22, 16, 18, 16, 15], [0, 1, 4, 3, 8, 7, 19, 14, 22, 22], [0, 1, 8, 7, 12, 10, 8, 14, 14, 26], [0, 1, 0, 4, 4, 8, 10, 18, 27, 28], [0, 2, 1, 2, 1, 9, 17, 12, 31, 25], [1, 4, 6, 3, 10, 3, 26, 3, 24, 20], [1, 1, 8, 0, 3, 11, 17, 7, 19, 33], [1, 1, 3, 5, 5, 6, 9, 15, 9, 46], [0, 6, 0, 4, 4, 10, 10, 6, 29, 31], [1, 7, 0, 6, 9, 17, 10, 3, 28, 19], [0, 0, 3, 10, 11, 10, 15, 13, 18, 20], [0, 0, 0, 1, 8, 10, 15, 23, 21, 22], [0, 2, 1, 0, 10, 1, 17, 28, 22, 19], [2, 0, 2, 4, 5, 32, 16, 18, 13, 8], [0, 0, 1, 2, 9, 9, 14, 12, 28, 25], [0, 0, 10, 1, 6, 10, 15, 15, 21, 22], [0, 1, 9, 1, 12, 4, 14, 10, 13, 36], [0, 2, 1, 9, 2, 11, 30, 13, 7, 25], [1, 3, 16, 1, 6, 2, 11, 20, 20, 20], [0, 1, 4, 4, 4, 7, 28, 14, 23, 15]]
    champion_pool.append([3, 1, 2, 6, 14, 23, 24, 17, 10, 0])
    champion_pool.append([0, 1, 7, 7, 4, 14, 17, 20, 27, 3])

    print(tournament_score([0,0,0,0,0,20,20,20,20,20], champion_pool))

    scores = [(s, tournament_score(s, champion_pool)) for s in champion_pool]
    print(sorted(scores, key=lambda x: x[1], reverse=True))
