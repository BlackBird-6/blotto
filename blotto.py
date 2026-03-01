import random
import numpy as np
import time
import json

# useful regex to filter algo text files: ^[^[].+$\n
tower_pts = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
champion_pool = []
SCORE_MODE: str = "w11"

def main():
    global SCORE_MODE
    set_seed(42)
    
    scenario = "w22"
    extend_algos = ["w11", "w12", "w21"]

    SCORE_MODE = f"{scenario}"
    MODE = 2

    assert score([0, 1, 1, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 20

    print(f"[Blotto] scenario={scenario}  mode={MODE}  extend_algos={extend_algos}")
    # algos_in = open(f"{scenario}_algos.txt", "r").read().splitlines()
    
    # w21:
    # [0, 0, 0, 0, 0, 0, 0, 5, 44, 51] # mode=1
    # [0, 0, 0, 0, 3, 8, 32, 37, 18, 2] # mode-1 with w12_algos extend
    # [0, 0, 1, 2, 5, 7, 31, 34, 14, 6] mode-1 with good_algos extend
    # [0, 0, 0, 0, 1, 1, 22, 27, 26, 23] arena on w11+w12
    # [0, 0, 0, 0, 0, 1, 0, 5, 44, 50] # winner of good
    # [0, 0, 1, 2, 6, 13, 28, 9, 0, 41] # arena on good


    # w22:
    # [0, 1, 4, 15, 22, 22, 23, 2, 7, 4] # arena on w11+w12

    if MODE == 1:
        # Add player data to list?
        # champion_pool.extend([json.loads(a) for a in open("w11_algos.txt", "r").read().splitlines()])
        # champion_pool.extend([json.loads(a) for a in open("good_algos.txt", "r").read().splitlines()])
        
        champion, champ_score = optimize(k=500, pool_size=100, mutation_strength=30, max_transfer=100)
        scores = [(s, tournament_score(s, champion_pool)) for s in champion_pool]
        sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)

        for l in sorted_scores[:10]:
            print(l)
        print("[...]")
        for l in sorted_scores[-10:]:
            print(l)   


        write_algos(sorted_scores)

        # # add the main pool to the champion pool
        # for a in algos_in:
        #     champion_pool.append(json.loads(a))
        # scores = [(s, tournament_score(s, champion_pool)) for s in champion_pool]
        # sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
        
        # for l in sorted_scores:
        #     print(l)
    elif MODE == 2:

        # Add player data to list?
        # champion_pool.extend([json.loads(a) for a in open("w11_algos.txt", "r").read().splitlines()])
        for e in extend_algos:
            champion_pool.extend([json.loads(a) for a in open(f"{e}_algos.txt", "r").read().splitlines()])
        
        champion, champ_score = optimize_arena(k=200, pool_size=100, mutation_strength=30, max_transfer=100)
        print()
        print("=" * 60)
        print(f"Champion strategy : {champion}")
        print(f"Soldiers used     : {sum(champion)} / 100")
        print(f"Tournament score  : {champ_score:.4f}")
        print("=" * 60)

        champion_pool.append(champion)
        scores = [(s, tournament_score(s, champion_pool)) for s in champion_pool]
        sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)

        for l in sorted_scores[:10]:
            print(l)
        print("[...]")
        for l in sorted_scores[-10:]:
            print(l)   

        write_algos(sorted_scores)

    elif MODE == 3:
        #add the main pool  
        for e in extend_algos:
            champion_pool.extend([json.loads(a) for a in open(f"{e}_algos.txt", "r").read().splitlines()])

        scores = [(s, tournament_score(s, champion_pool)) for s in champion_pool]
        sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    
        for l in sorted_scores:
            print(l)

        write_algos(sorted_scores)

def write_algos(sorted_scores):
    algos_out = open("out_algos.txt", "w")
    for l in sorted_scores:
        algos_out.write(str(l[0]) + "\n")
    algos_out.close()
 

def set_seed(seed: int = 42) -> None:
    """Seed every random source used by this module for reproducibility."""
    random.seed(seed)

# ── Pairwise scoring (single match) ──────────────────────────────────────────

def score(s1, s2):
    """Dispatch to the active scoring function (controlled by SCORE_MODE)."""
    if SCORE_MODE == "w11":
        return w11_score(s1, s2)
    elif SCORE_MODE == "w12":
        return w12_score(s1, s2)
    elif SCORE_MODE == "w21":
        return w21_score(s1, s2)
    elif SCORE_MODE == "w22":
        return w22_score(s1, s2)
    else:
        raise ValueError(f"Unknown SCORE_MODE: {SCORE_MODE!r}")

# How much does s1 score in a game against s2?
def w11_score(s1, s2):
    score = 0
    for i in range(10):
        if s1[i] > s2[i]:
            score += tower_pts[i]
    return score

# The last (highest-indexed) tower a player wins is worth negative points equal to its index
def w12_score(s1, s2):
    s1_score = []
    for i in range(10):
        if s1[i] > s2[i]:
            s1_score.append(tower_pts[i])
    if s1_score:
        s1_score[-1] *= -1
    return sum(s1_score)

# The first (lowest-indexed) tower a player wins is worth triple points
def w21_score(s1, s2):
    s1_score = []
    for i in range(10):
        if s1[i] > s2[i]:
            s1_score.append(tower_pts[i])
    if s1_score:
        s1_score[0] *= 3
    return sum(s1_score)

# If you own tower N and you win N towers in total your score is doubled
def w22_score(s1, s2):
    s1_score = []
    for i in range(10):
        if s1[i] > s2[i]:
            s1_score.append(tower_pts[i])
    if len(s1_score) in s1_score:
        s1_score *= 2
        # if s1 == [0, 1, 4, 15, 22, 22, 23, 2, 7, 4]:
        #     print(f"s1: {s1}, s2: {s2}, s1_score: {s1_score} with {len(s1_score)} towers won")
    return sum(s1_score)

# ── Strategy generation ────────────────────────────────────────────────────────

def random_strategy(total: int = 100, towers: int = 10) -> list[int]:
    """Generate a random valid allocation: non-negative integers summing to `total`."""
    # Stars-and-bars: place (total) soldiers across (towers) bins
    towers = 9
    cuts = sorted(random.sample(range(1, total + towers), towers - 1))
    cuts = [0] + cuts + [total + towers]
    strat = [cuts[i + 1] - cuts[i] - 1 for i in range(towers)]
    return strat + [0]


def mutate(strategy: list[int], strength: int = 10, max_transfer: int = 5) -> list[int]:
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
        transfer = random.randint(0, min(max_transfer, max(0, s[donor])))
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
    return sum(score(strategy, opponent) for opponent in pool)/(len(pool)-1)


# ── Main optimizer ────────────────────────────────────────────────────────────

def optimize(k: int = 10, pool_size: int = 1000, mutation_strength: int = 10,
             max_transfer: int = 5, total: int = 100, towers: int = 10) -> tuple[list[int], float]:
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
        pool = [mutate(champion, mutation_strength, max_transfer) for _ in range(pool_size)]
        pool += champion_pool
        scores = [tournament_score(s, pool) for s in pool]

        best_idx = max(range(len(scores)), key=lambda i: scores[i])
        new_champion = pool[best_idx]
        new_score = scores[best_idx]

        print(f"  iter {iteration:>2}         -> champion score = {new_score:.4f}  strategy = {new_champion}")
        champion = new_champion
        champion_score = new_score
        champion_pool.append(champion)


        print("Submission score: " + str(tournament_score([2, 4, 6, 9, 11, 17, 24, 22, 2, 3], pool)))
        # print("Submission score: " + str(tournament_score([3, 1, 2, 6, 14, 23, 24, 17, 10, 0], pool)))

    # ── Sanity checks ─────────────────────────────────────────────────────────
    assert all(s >= 0 for s in champion), "Strategy has negative values!"
    assert sum(champion) <= total, f"Strategy uses {sum(champion)} > {total} soldiers!"

    return champion, champion_score

def optimize_arena(k: int = 10, pool_size: int = 1000, mutation_strength: int = 10,
             max_transfer: int = 5, total: int = 100, towers: int = 10) -> tuple[list[int], float]:
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

    print(f"[Blotto Optimizer (Arena)]  k={k}  pool_size={pool_size}  mutation_strength={mutation_strength}")

    # ── Iteration 0: random seed pool ─────────────────────────────────────────
    pool = [random_strategy(total, towers) for _ in range(pool_size)]
    scores = [tournament_score(s, champion_pool) for s in pool]

    best_idx = max(range(pool_size), key=lambda i: scores[i])
    champion = pool[best_idx]
    champion_score = scores[best_idx]

    print(f"  iter 0 (seed)  -> champion score = {champion_score:.4f}  strategy = {champion}")

    # ── Iterations 1..k: mutate & evolve ──────────────────────────────────────
    for iteration in range(1, k + 1):
        pool = [mutate(champion, mutation_strength, max_transfer) for _ in range(pool_size)]
        pool.append(champion)
        scores = [tournament_score(s, champion_pool) for s in pool]
        best_idx = max(range(len(scores)), key=lambda i: scores[i])
        new_champion = pool[best_idx]
        new_score = scores[best_idx]

        print(f"  iter {iteration:>2}         -> champion score = {new_score:.4f}  strategy = {new_champion}")
        champion = new_champion
        champion_score = new_score

        print("Submission score: " + str(tournament_score([1, 3, 7, 10, 6, 17, 23, 3, 2, 28], pool)))
        # print("Submission score: " + str(tournament_score([3, 1, 2, 6, 14, 23, 24, 17, 10, 0], pool)))

    # ── Sanity checks ─────────────────────────────────────────────────────────
    assert all(s >= 0 for s in champion), "Strategy has negative values!"
    assert sum(champion) <= total, f"Strategy uses {sum(champion)} > {total} soldiers!"

    return champion, champion_score

# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    main()
