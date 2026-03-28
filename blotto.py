import random
import numpy as np
import time
import json

# useful regex to filter algo text files: ^[^[].+$\n
tower_pts = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
champion_pool = []
SCORE_MODE: str
MIN_SOLDIERS = 0
DONT_ENFORCE_SOLDIER_CAP = True

all_algos = ["w11", "w12", "w21", "w22", "w31", "w32", "w41", "w42", "w51", "w52", "w53"]

def main():
    global SCORE_MODE
    set_seed(42)
    
    SCORE_MODE = "w63"
    extend_algos = ["w63", "extra"]
    MODE = 3

    # SCORE_MODE: Algorithm to use for scoring
    # extend_algos: Algorithms to add to the pool
    # MODE: 1 -- Optimize, 2 -- Optimize Arena, 3 -- Tournament Simulation

    sanity_check(SCORE_MODE)
    print(f"[Blotto] scenario={SCORE_MODE}  mode={MODE}  extend_algos={extend_algos}")
    
    # algos_in = open(f"algos/{scenario}_algos.txt", "r").read().splitlines()
    
   
    # w61
    # [5, 7, 10, 15, 18, 20, 22, 1, 1, 1] current champion
    # [3, 5, 8, 13, 17, 22, 26, 2, 2, 2] arena all

    # Looks reasonable enough, 2 on last towers to claim them if others put 0 or 1 is good too


    # w62
    # [0, 0, 0, 0, 0, 2, 24, 26, 26, 22] current champion (ah yes, from w32)
    # [0, 0, 0, 4, 0, 22, 0, 28, 34, 12] arena all 
    # [0, 0, 0, 2, 0, 22, 0, 28, 34, 14] arena all (modified)

    # It is impossible to go off strictly past precedent because the first 5 towers will be
    # devoid of any soldier allocations, though arena all still gives a valid looking allocation

    # I also love the investment of soldiers in the 4th tower and think that's brilliant,
    # so it's staying as the final solution (modified since dont think many others will come up with that)
    # (it is also quite interesting that arena came up with that on its own)

    # w63
    # [3, 7, 2, 8, 1, 9, 5, 5, 2, 8] current champion (why did someone run this before this scenario?)
    # [0, 0, 0, 1, 1, 1, 1, 1, 1, 1] arena all after I modified mutate function

    # There is absolutely no past precedent and it might as well be impossible to simulate this one
    # The worth of each tower in soldiers is [2, 4, 6, 8, 10, 12, 14, 16, 18, 20] so allocating
    # any less than that and winning is strictly beneficial (losing is non-beneficial)
    # However, if everyone else allocates a lot, then it is optimal to allocate practically nothing
    
    # (via level-k thinking):
    # (k=0) Normal strategy as done before
    # (k=1) Allocating practically nothing is optimal if everyone else allocates a lot
    # (k=2) We'll allocate at least 1 to everything (except tower 1) to farm the all-0/1 strategies
    # and then slowly increase from there and see how it goes

    # [0, 1, 2, 2, 3, 3, 3, 4, 6, 6] strategy that I made up

    
    if MODE == 1:   
        champion, champ_score = optimize(k=200, pool_size=100, mutation_strength=30, max_transfer=100)
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
    
        for l in sorted_scores:
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

# ── Pairwise scoring (single match) ──────────────────────────────────────────

def score(s1, s2):
    """Dispatch to the active scoring function (controlled by SCORE_MODE)."""
    
    SCORE_FUNCTIONS = {
    "w11": w11_score,
    "w12": w12_score,
    "w21": w21_score,
    "w22": w22_score,
    "w31": w31_score,
    "w32": w32_score,
    "w41": w41_score,
    "w42": w42_score,
    "w51": w51_score,
    "w52": w52_score,
    "w53": w53_score,
    "w61": w61_score,
    "w62": w62_score,
    "w63": w63_score,
    "omni": omni_score,
    }
    
    try:
        return SCORE_FUNCTIONS[SCORE_MODE](s1, s2)
    except KeyError:
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


# If a player wins two or more consecutive towers, the first tower of each independent 
# consecutive run is worth double.
def w31_score(s1, s2):
    s1_score = [0]
    for i in range(10):
        s1_score.append(tower_pts[i] if s1[i] > s2[i] else 0)
    s1_score.append(0)
    for i in range(1, len(s1_score)-1):
        # Last tower wasn't won (start of a won) and this tower is, and the next tower is (run)
        if s1_score[i-1] == 0 and s1_score[i] != 0 and s1_score[i+1] != 0:
            s1_score[i] *= 2
        # if s1 == [0, 1, 4, 15, 22, 22, 23, 2, 7, 4]:
        #     print(f"s1: {s1}, s2: {s2}, s1_score: {s1_score} with {len(s1_score)} towers won")
    return sum(s1_score)

# If a player wins a tower not adjacent to any other towers won, it's worth negative
def w32_score(s1, s2):
    s1_score = [0]
    for i in range(10):
        s1_score.append(tower_pts[i] if s1[i] > s2[i] else 0)
    s1_score.append(0)
    for i in range(1, len(s1_score)-1):
        if s1_score[i-1] == 0 and s1_score[i] != 0 and s1_score[i+1] == 0:
            s1_score[i] *= -1
    return sum(s1_score)

#  If the index of the highest-indexed tower won is larger than that of the opponent
#  then each tower you win is worth one point fewer
def w41_score(s1, s2):
    s1_score = []
    highest_won = 0
    for i in range(10):
        if(s1[i] > s2[i]):
            s1_score.append(tower_pts[i])
            highest_won = 1
        if s2[i] > s1[i]:
            highest_won = 2
    if highest_won == 1:
        s1_score = [x - 1 for x in s1_score]
    return sum(s1_score)
    
# For both players, the tower they won by the maximum margin is worth double
def w42_score(s1, s2):
    s1_score = []
    s1_margin = []
    for i in range(10):
        if s1[i] > s2[i]:
            s1_score.append(tower_pts[i])
            s1_margin.append(s1[i] - s2[i])

    if s1_margin:
        max_margin = max(s1_margin)
        for i in range(len(s1_score)):
            if s1_margin[i] == max_margin:
                s1_score[i] *= 2
                break
    return sum(s1_score)

# If a player wins strictly more towers than the opponent, 
# then each tower the player wins is worth one point fewer.
def w51_score(s1, s2):
    s1_score = []
    s1_towers_won_delta = 0
    for i in range(10):
        if(s1[i] > s2[i]):
            s1_score.append(tower_pts[i])
            s1_towers_won_delta += 1
        if s2[i] > s1[i]:
            s1_towers_won_delta -= 1
    if s1_towers_won_delta > 0:
        s1_score = [x - 1 for x in s1_score]
    return sum(s1_score)

# If a player wins more than 1 tower, then the won tower with the maximum 
# number of soldiers allocated by that player is worth 0 points. 
# If there is a tie, the highest-indexed tower among them is worth 0.
def w52_score(s1, s2):
    s1_score = []
    s1_allocatedmax = -1
    s1_allocatedmax_idx = -1
    for i in range(10):
        if(s1[i] > s2[i]):
            s1_score.append(tower_pts[i])
            if s1[i] >= s1_allocatedmax:
                s1_allocatedmax = s1[i]
                s1_allocatedmax_idx = i
    if s1_allocatedmax_idx != -1:
        s1_score.append(-tower_pts[s1_allocatedmax_idx])
    return sum(s1_score)

# For each player, the lowest-indexed tower 
# at which the player allocates more than 10 soldiers AND WINS is worth 0 points.
def w53_score(s1, s2):
    s1_score = []
    s1_won = False
    for i in range(10):
        if(s1[i] > s2[i]):
            if not s1_won and s1[i] > 10:
                s1_won = True
                continue
            s1_score.append(tower_pts[i])
    return sum(s1_score)

# If a player wins consecutive towers, an arithmetic sequence of difference 3 is added 
# to the consecutive streak. For example, if a player wins towers 5, 6, 7, 8, but not 4 and 9, 
# then they are respectively worth 5 + 0, 6 + 1x3, 7 + 2x3, and 8 + 3x3.
def w61_score(s1, s2):
    s1_score = []
    s1_bonus = 0
    for i in range(10):
        if(s1[i] > s2[i]):
            s1_score.append(tower_pts[i] + s1_bonus)
            s1_bonus += 3
        else:
            s1_bonus = 0
    return sum(s1_score)

# If a player wins both Tower i and Tower (11 - i), then both towers are worth 0.
# (or i and 9-i when 0-indexed)
def w62_score(s1, s2):
    s1_score = []
    s1_won = []
    for i in range(10):
        if(s1[i] > s2[i]):
            if (9-i) in s1_won:
                s1_score.remove(tower_pts[9-i])
                continue
            s1_won.append(i)
            s1_score.append(tower_pts[i])
    return sum(s1_score)

# Any unused soldier is worth 0.5 point each.
def w63_score(s1, s2):
    score = 0
    for i in range(10):
        if s1[i] > s2[i]:
            score += tower_pts[i]
    return score + 0.5*(100-sum(s1))

def omni_score(s1, s2):
    return w11_score(s1, s2) + w12_score(s1, s2) + w21_score(s1, s2) + w22_score(s1, s2) + w31_score(s1, s2) + w32_score(s1, s2) + w41_score(s1, s2) + w42_score(s1, s2) + w51_score(s1, s2) + w52_score(s1, s2) + w53_score(s1, s2)
# Copy paste:
# assert score([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 0
def sanity_check(scenario):
    if scenario == "w41":
        assert score([1, 1, 0, 1, 1, 0, 1, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 0+1+3+4+6+8
        assert score([1, 1, 0, 1, 1, 0, 1, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]) == 0+1+3+4+6+8+6

    if scenario == "w42":
        assert score([1, 1, 0, 1, 1, 0, 1, 0, 2, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 1+2+4+5+7+18
        assert score([1, 1, 0, 1, 1, 0, 1, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 2+2+4+5+7+9
    
    if scenario == "w51":
        assert score([1, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 0
        assert score([1, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0, 0]) == 1
        assert score([1, 0, 1, 0, 1, 0, 1, 0, 1, 0], [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]) == 1+3+5+7+9
        assert score([1, 0, 1, 0, 1, 0, 1, 0, 1, 0], [0, 1, 0, 1, 0, 1, 0, 1, 0, 0]) == 0+2+4+6+8
    
    if scenario == "w52":
        assert score([1, 0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 1
        assert score([1, 0, 1, 0, 1, 0, 1, 0, 1, 0], [0, 1, 0, 1, 0, 1, 0, 1, 0, 0]) == 1+3+5+7+0
        assert score([1, 0, 1, 0, 1, 0, 2, 0, 1, 0], [0, 1, 0, 1, 0, 1, 0, 1, 0, 0]) == 1+3+5+0+9
    
    if scenario == "w53":
        assert score([11, 0, 0, 0, 0, 0, 0, 0, 0, 10], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 10
        assert score([10, 0, 0, 0, 0, 0, 0, 0, 0, 10], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 1+10
        assert score([11, 11, 11, 0, 0, 0, 0, 0, 0, 0], [11, 11, 10, 0, 0, 0, 0, 0, 0, 0]) == 0
        assert score([5, 5, 5, 5, 11, 11, 0, 0, 0, 0], [11, 11, 11, 0, 11, 10, 0, 0, 0, 0]) == 4

    if scenario == "w61":
       assert score([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 1+2+3+4+5+6+7+8+9+10+3+6+9+12+15+18+21+24+27
       assert score([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 1, 0, 0, 1, 0, 0, 1, 0]) == 1+2+3+4+5+3+7+8+3+10

    if scenario == "w62":
       assert score([1, 1, 0, 0, 0, 0, 0, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 2+8
       assert score([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 0
       assert score([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 0, 0, 0, 0, 1, 1, 0, 0]) == 3+4+9+10

    if scenario == "w63":
       assert score([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 50
       assert score([0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 59.5
       assert score([0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]) == 49.5

    # There is no sanity check for omni-score scenario because it is not sane.

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
