tower_pts = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
SCORE_MODE: str = "w11"

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
