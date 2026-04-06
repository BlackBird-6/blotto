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
MIN_SOLDIERS = 0
DONT_ENFORCE_SOLDIER_CAP = False # Only used for w63

all_algos = ["w11", "w12", "w21", "w22", "w31", "w32", "w41", "w42", "w51", "w52", "w53", "w61", "w62", "w63"]
later_algos = ["w41", "w42", "w51", "w52", "w53", "w61", "w62", "w63"]
def main():
    global SCORE_MODE
    set_seed(42)

    # SCORE_MODE: Algorithm to use for scoring (e.g. w71 for week 7 scenario 1)
    # extend_algos: Algorithms to add to the pool as a list of strings (e.g. ["w11", "w12"])
    # MODE: 1 -- Optimize, 2 -- Optimize (Arena), 3 -- Tournament Simulation
    # SHOW_ALL_SCORES: Whether to show all scores or just the top and bottom 10 (Modes 1/2)
    # SHOW_ALL_TOURNEY_SCORES: SHOW_ALL_SCORES (Mode 3)

    ############### EDIT THESE ##############    
    SCORE_MODE = "w11"
    extend_algos = all_algos + ["extra"]
    MODE = 3
    SHOW_ALL_SCORES = False
    SHOW_ALL_TOURNEY_SCORES = True
    #########################################


    # w71
    # [1, 2, 3, 2, 2, 2, 26, 27, 33, 2] current champion
    # [1, 1, 2, 2, 2, 2, 27, 28, 2, 33] arena all
    # [0, 0, 1, 1, 2, 1, 0, 28, 34, 33] arena on w41 onwards
    # [1, 1, 1, 2, 3, 2, 2, 3, 43, 42] arena on w62

    # previously arena all has worked pretty well but I am skeptical that the
    # distribution will probably be irregular and front-focused due to the gimmick
    # w62 follows essentially exactly what I expect the distribution to be like,
    # and so I will choose arena on that for my strategy

    # w72
    # [0, 1, 1, 2, 2, 1, 24, 23, 23, 23] current champion
    # [2, 2, 9, 0, 0, 21, 26, 1, 2, 37] arena all
    # [1, 1, 4, 4, 11, 11, 2, 2, 32, 32] strategy I made up
    
    # I feel like anything I come up with in arena is going to be overfitted
    # and wont have any relation to what people will put in the actual tournament
    # so this will be another time I submit manually
    # I suspect people will want to pair all of their soldiers, and if everyone
    # does this, then anyone who does not do this puts themselves
    # at a disadvantage (because you won't win/lose towers in even pairs and thus lose score)
    # So, I will also pair my soldiers for essentially 5 tower blotto 

    # w73
    # [2, 3, 3, 4, 4, 4, 22, 27, 28, 3] current champion (this is also current champion on w11 vs all algos)
    # [1, 3, 3, 3, 3, 2, 24, 27, 29, 5] arena all (this also wins on w11 rules vs all algos) (seed 402 b/c I forgot to change it back)
    # [1, 3, 3, 3, 13, 19, 23, 27, 3, 5] arena all (seed 42) (this also wins on w11 vs all algos)
    # [1, 3, 4, 4, 3, 22, 24, 28, 6, 5] arena all ON W11 RULES (this also wins on w73 vs all algos)
    # [3, 3, 5, 5, 3, 19, 25, 29, 3, 5] arena on later algos

    # As expected this scenario is practically identical to w11, since you will in
    # practice never encounter the gimmick if you just play soldiers which are close
    # to what other people play, which is already what you should be doing anyway
    # so I will just use arena all and that's a wrap on Colonel Blotto!

    scoring.SCORE_MODE = SCORE_MODE
    sanity_check(SCORE_MODE)
    print(f"[Blotto] scenario={SCORE_MODE}  mode={MODE}  extend_algos={extend_algos}")
    
    # algos_in = open(f"algos/{scenario}_algos.txt", "r").read().splitlines()
    
   
    

    
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

        # # add the main pool to the champion pool
        # for a in algos_in:
        #     champion_pool.append(json.loads(a))
        # scores = [(s, tournament_score(s, champion_pool)) for s in champion_pool]
        # sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
        
        # for l in sorted_scores:
        #     print(l)
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

    elif MODE == 3:
        #add the main pool  
        print(f"[Blotto Tournament]  arena_size={len(champion_pool)}")

        for e in extend_algos:
            champion_pool.extend([json.loads(a) for a in open(f"algos/{e}_algos.txt", "r").read().splitlines()])

        scores = [(s, tournament_score(s, champion_pool)) for s in champion_pool]
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

        if iteration % 10 == 0:
            print(f"  iter {iteration:>2}         -> champion score = {new_score:.4f}  strategy = {new_champion}")
        champion = new_champion
        champion_score = new_score
        champion_pool.append(champion)


        # print("Submission score: " + str(tournament_score([2, 4, 6, 9, 11, 17, 24, 22, 2, 3], pool)))
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

        # print("Submission score: " + str(tournament_score([0, 0, 2, 2, 2, 2, 10, 18, 30, 34], pool)))
        # print("Submission score: " + str(tournament_score([3, 1, 2, 6, 14, 23, 24, 17, 10, 0], pool)))

    # ── Sanity checks ─────────────────────────────────────────────────────────
    assert all(s >= 0 for s in champion), "Strategy has negative values!"
    assert sum(champion) <= total, f"Strategy uses {sum(champion)} > {total} soldiers!"

    return champion, champion_score

# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    main()
