import argparse
import random
import numpy as np
import time
import json

import scoring
from scoring import score
from sanity_checks import sanity_check
# useful regex to filter algo text files: ^[^[].+$\n
champion_pool = []
SCORE_MODE: str

MIN_SOLDIERS = 0 # Enforce minimum soldiers per tower
DONT_ENFORCE_SOLDIER_CAP = False # Only used for w63
all_algos = ["wo11", "wo12", "wo21", "wo22", "wo31", "wo32", "wo41", "wo42", "wo51", "wo52", "wo53", "wo61", "wo62", "wo63", "wo71", "wo72", "wo73"]
later_algos = ["wo41", "wo42", "wo51", "wo52", "wo53", "wo61", "wo62", "wo63", "wo71", "wo72", "wo73"]
def main():
    global SCORE_MODE
    set_seed(42)

    # SCORE_MODE: Algorithm to use for scoring (e.g. w71 for week 7 scenario 1)
    # extend_algos: Algorithms to add to the pool as a list of strings (e.g. ["w11", "w12"])
    # MODE: 1 -- Optimize, 2 -- Optimize (Arena), 3 -- Tournament Simulation, 4 -- Arena Verbose
    # SHOW_ALL_SCORES: Whether to show all scores or just the top and bottom 10 (Modes 1/2)
    # SHOW_ALL_TOURNEY_SCORES: SHOW_ALL_SCORES (Modes 3/4)

    ############### EDIT THESE ##############    
    SCORE_MODE = "w21"
    extend_algos = ["w11"]
    MODE = 3
    SHOW_ALL_SCORES = False
    SHOW_ALL_TOURNEY_SCORES = True
    #########################################

    # Parse args
    parser = argparse.ArgumentParser()
    parser.add_argument("--SCORE_MODE", type=str)
    parser.add_argument("--extend_algos", type=str, nargs="*")
    parser.add_argument("--MODE", type=int, choices=[1, 2, 3, 4])
    parser.add_argument("--SHOW_ALL_SCORES", action=argparse.BooleanOptionalAction)

    args, _ = parser.parse_known_args()

    if args.SCORE_MODE is not None:
        SCORE_MODE = args.SCORE_MODE
    if args.extend_algos is not None:
        extend_algos = args.extend_algos
    if args.MODE is not None:
        MODE = args.MODE
    if args.SHOW_ALL_SCORES is not None:
        SHOW_ALL_SCORES = args.SHOW_ALL_SCORES
        SHOW_ALL_TOURNEY_SCORES = args.SHOW_ALL_SCORES

    scoring.SCORE_MODE = SCORE_MODE

    sanity_check(SCORE_MODE)
    print(f"[Blotto] scenario={SCORE_MODE}  mode={MODE}  extend_algos={extend_algos}")
        
    if MODE == 1:   
        champion, champ_score = optimize(k=200, pool_size=100, mutation_strength=30, max_transfer=100)
        scores = [(s, tournament_score(s, champion_pool)) for s in champion_pool]
        sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)

        if SHOW_ALL_SCORES:
            for l in sorted_scores:
                print(l)
        else:
            for l in sorted_scores[:10]:
                print(l)
            print("[...]")
            for l in sorted_scores[-10:]:
                print(l)   

        write_algos(sorted_scores)

    elif MODE == 2:

        for e in extend_algos:
            champion_pool.extend([json.loads(a) for a in open(f"algos/{e}_algos.txt", "r").read().splitlines()])
        
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

        if SHOW_ALL_SCORES:
            for l in sorted_scores:
                print(l)
        else:
            for l in sorted_scores[:10]:
                print(l)
            print("[...]")
            for l in sorted_scores[-10:]:
                print(l)   

        write_algos(sorted_scores)

    elif MODE == 3 or MODE == 4:
        verbose = (MODE == 4)
        if verbose:
            print(f"[Blotto Tournament Verbose]  arena_size={len(champion_pool)}")
        else:
            print(f"[Blotto Tournament]  arena_size={len(champion_pool)}")

        for e in extend_algos:
            champion_pool.extend([json.loads(a) for a in open(f"algos/{e}_algos.txt", "r").read().splitlines()])

        scores = arena(champion_pool, verbose=verbose)
        sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    
        if SHOW_ALL_TOURNEY_SCORES:
            for l in sorted_scores:
                print(l)
        else:
            for l in sorted_scores[:10]:
                print(l)
            print("[...]")
            for l in sorted_scores[-10:]:
                print(l)   

        write_algos(sorted_scores)

def write_algos(sorted_scores):
    algos_out = open("algos/out_algos.txt", "w")
    for l in sorted_scores:
        algos_out.write(str(l[0]) + "\n")
    algos_out.close()
 

def set_seed(seed: int = 42) -> None:
    """Seed every random source used by this module for reproducibility."""
    random.seed(seed)

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
        transfer = random.randint(0, min(max_transfer, max(0, s[donor]-MIN_SOLDIERS)))
        s[donor] -= transfer

        if DONT_ENFORCE_SOLDIER_CAP and random.randint(0, 1) == 1:
            continue
        
        s[recipient] += transfer

    return s

# ── Evaluation ────────────────────────────────────────────────────────────────

def tournament_score(strategy: list[int], pool: list[list[int]]) -> float:
    """Average score of `strategy` against every opponent in `pool`."""
    return sum(score(strategy, opponent) for opponent in pool)/(len(pool)-1)


def arena(pool: list[list[int]], verbose: bool = False) -> list[tuple[list[int], float]]:
    """
    Run a tournament/arena simulation for all strategies in the pool.
    Returns a list of tuples (strategy, tournament_score) computed in a single pass.
    If verbose is True, prints every matchup grouped by strategy in consistent order.
    """
    n = len(pool)
    if n <= 1:
        return [(s, 0.0) for s in pool]

    accumulated_scores = [0.0] * n
    
    # Pre-calculate self-matchups
    for i in range(n):
        accumulated_scores[i] += score(pool[i], pool[i])

    for i in range(n):
        for j in range(i + 1, n):
            s1, s2 = pool[i], pool[j]
            res_12 = score(s1, s2)
            res_21 = score(s2, s1)
            
            accumulated_scores[i] += res_12
            accumulated_scores[j] += res_21
                    
    denominator = n - 1
    results = [(pool[i], accumulated_scores[i] / denominator) for i in range(n)]

    if verbose:
        strat_width = max(len(str(s)) for s in pool)
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                s1, s2 = pool[i], pool[j]
                res_a = score(s1, s2)
                res_b = score(s2, s1)
                wld = 'W' if res_a > res_b else ('L' if res_a < res_b else 'D')
                print(f"{str(s1):<{strat_width}} vs {str(s2):<{strat_width}}: {res_a:>6} - {res_b:<6} {wld}")
            print("")
    return results


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

        if iteration % 10 == 0:
            print(f"  iter {iteration:>2}         -> champion score = {new_score:.4f}  strategy = {new_champion}")
        champion = new_champion
        champion_score = new_score
        champion_pool.append(champion)

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

    print(f"[Blotto Optimizer (Arena)]  k={k}  pool_size={pool_size}  mutation_strength={mutation_strength}  arena_size={len(champion_pool)}")

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

        if iteration % 10 == 0:
            print(f"  iter {iteration:>2}         -> champion score = {new_score:.4f}  strategy = {new_champion}")
        champion = new_champion
        champion_score = new_score

    # ── Sanity checks ─────────────────────────────────────────────────────────
    assert all(s >= 0 for s in champion), "Strategy has negative values!"
    assert sum(champion) <= total, f"Strategy uses {sum(champion)} > {total} soldiers!"

    return champion, champion_score

# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    main()
