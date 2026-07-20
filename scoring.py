tower_pts = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
SCORE_MODE: str = "wo11"

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
    "w61": w61_score,
    "w62": w62_score,
    "wo11": wo11_score,
    "wo12": wo12_score,
    "wo21": wo21_score,
    "wo22": wo22_score,
    "wo31": wo31_score,
    "wo32": wo32_score,
    "wo41": wo41_score,
    "wo42": wo42_score,
    "wo51": wo51_score,
    "wo52": wo52_score,
    "wo53": wo53_score,
    "wo61": wo61_score,
    "wo62": wo62_score,
    "wo63": wo63_score,
    "wo71": wo71_score,
    "wo72": wo72_score,
    "wo73": wo73_score,
    "omni": omni_score,
    }
    
    try:
        return SCORE_FUNCTIONS[SCORE_MODE](s1, s2)
    except KeyError:
        raise ValueError(f"Unknown SCORE_MODE: {SCORE_MODE!r}")

# How much does s1 score in a game against s2?
def wo11_score(s1, s2):
    score = 0
    for i in range(10):
        if s1[i] > s2[i]:
            score += tower_pts[i]
    return score

# The last (highest-indexed) tower a player wins is worth negative points equal to its index
def wo12_score(s1, s2):
    s1_score = []
    for i in range(10):
        if s1[i] > s2[i]:
            s1_score.append(tower_pts[i])
    if s1_score:
        s1_score[-1] *= -1
    return sum(s1_score)

# The first (lowest-indexed) tower a player wins is worth triple points
def wo21_score(s1, s2):
    s1_score = []
    for i in range(10):
        if s1[i] > s2[i]:
            s1_score.append(tower_pts[i])
    if s1_score:
        s1_score[0] *= 3
    return sum(s1_score)

# If you own tower N and you win N towers in total your score is doubled
def wo22_score(s1, s2):
    s1_score = []
    for i in range(10):
        if s1[i] > s2[i]:
            s1_score.append(tower_pts[i])
    if len(s1_score) in s1_score:
        s1_score *= 2
    return sum(s1_score)


# If a player wins two or more consecutive towers, the first tower of each independent 
# consecutive run is worth double.
def wo31_score(s1, s2):
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
def wo32_score(s1, s2):
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
def wo41_score(s1, s2):
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
def wo42_score(s1, s2):
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
def wo51_score(s1, s2):
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
def wo52_score(s1, s2):
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
def wo53_score(s1, s2):
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
def wo61_score(s1, s2):
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
def wo62_score(s1, s2):
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
def wo63_score(s1, s2):
    score = 0
    for i in range(10):
        if s1[i] > s2[i]:
            score += tower_pts[i]
    return score + 0.5*(100-sum(s1))

# For each player, if they allocate at least 20 soldiers to a tower, 
# that tower becomes high risk: if they win it, it is worth double; 
# if they lose it, it is worth negative. In case of a tie, the tower is worth 0 points.
def wo71_score(s1, s2):
    s1_score = 0
    for i in range(10):
        if s1[i] >= 20:
            if s1[i] > s2[i]:
                s1_score += 2*tower_pts[i]
            elif s1[i] < s2[i]:
                s1_score -= tower_pts[i]
        elif s1[i] > s2[i]:
            s1_score += tower_pts[i]
    return s1_score

# For each player, if they win more even-indexed towers than odd-indexed towers, 
# all even-indexed towers they win are worth 0 points. If they win more odd-indexed 
# towers than even-indexed towers, all odd-indexed towers they win are worth 0 points. 
# If the counts are equal, no towers are worth 0.
def wo72_score(s1, s2):
    s1_odd_score = []
    s1_even_score = []
    for i in range(10):
        if s1[i] > s2[i]:
            if i % 2 == 0:
                s1_even_score.append(tower_pts[i])
            else:
                s1_odd_score.append(tower_pts[i])

    if len(s1_odd_score) > len(s1_even_score):
        return sum(s1_even_score)
    elif len(s1_even_score) > len(s1_odd_score):
        return sum(s1_odd_score)
    else:
        return sum(s1_odd_score) + sum(s1_even_score)

# For each player, if they win a tower by allocating at least twice as many soldiers
# as the opponent, that tower is worth half its normal value.
def wo73_score(s1, s2):
    s1_score = 0
    for i in range(10):
        if s1[i] > s2[i]:
            if s1[i] >= 2*s2[i]:
                s1_score += tower_pts[i]/2
            else:
                s1_score += tower_pts[i]
    return s1_score

# All previous scenarios at the same time, combined together (season 1)!!!
def old_omni_score(s1, s2):
    return wo11_score(s1, s2) + wo12_score(s1, s2) + wo21_score(s1, s2) + wo22_score(s1, s2) + wo31_score(s1, s2) + wo32_score(s1, s2) + wo41_score(s1, s2) + wo42_score(s1, s2) + wo51_score(s1, s2) + wo52_score(s1, s2) + wo53_score(s1, s2) + wo61_score(s1, s2) + wo62_score(s1, s2) + wo63_score(s1, s2) + wo71_score(s1, s2) + wo72_score(s1, s2) + wo73_score(s1, s2)

def w11_score(s1, s2):
    score = 0
    for i in range(10):
        if s1[i] > s2[i]:
            score += tower_pts[i]
    return score

def w12_score(s1, s2):
    won = [s1[i] > s2[i] for i in range(10)]
    s1_score = 0
    for i in range(10):
        if won[i]:
            if 0 < i < 9 and won[i-1] and won[i+1]:
                s1_score += tower_pts[i]*3
            else:
                s1_score += tower_pts[i]
    return s1_score

def w21_score(s1, s2):
    score = 0
    for i in range(10):
        if s1[i] > s2[i]:
            score += tower_pts[i]
            if s1[i] <= s2[i]+5:
                score += tower_pts[i]
    return score

def w22_score(s1, s2):
    s1_wins = [s1[i] > s2[i] for i in range(10)]
    s2_wins = [s1[i] < s2[i] for i in range(10)]
    score = 0
    for i in range(10):
        if s1[i] > s2[i]:
            score += tower_pts[i]
    if sum(s2_wins) > sum(s1_wins):
       score += 2 * sum(s2_wins)
    return score

# Towers won by 15 or more are worthless
def w31_score(s1, s2):
    score = 0
    for i in range(10):
        if s1[i] > s2[i] and s1[i] - s2[i] < 15:
            score += tower_pts[i]
    return score

# if both players allocate at least 15 soldiers to a tower, then that tower is worth half the amount of points.
def w32_score(s1, s2):
    score = 0
    for i in range(10):
        if s1[i] > s2[i]:
            if s1[i] >= 15 and s2[i] >= 15:
                score += tower_pts[i]/2
            else:
                score += tower_pts[i]
    return score


# all towers from 1 to 5, inclusive, are worth double.
def w41_score(s1, s2):
    score = 0
    for i in range(10):
        if s1[i] > s2[i]:
            if i < 5:
                score += tower_pts[i] * 2
            else:
                score += tower_pts[i]
    return score

# for a player, if all the towers won form exactly one consecutive run,
# then the last tower of the run is worth double.
def w42_score(s1, s2):
    won_indices = [i for i in range(10) if s1[i] > s2[i]]
    if not won_indices:
        return 0
    
    score = sum(tower_pts[i] for i in won_indices)
    
    # Check if all won towers form exactly one consecutive run
    if len(won_indices) == won_indices[-1] - won_indices[0] + 1:
        score += tower_pts[won_indices[-1]]
        
    return score


# Scenario 1: if a player wins exactly 2 or exactly 3 towers, then their points are doubled.
def w51_score(s1, s2):
    won = [i for i in range(10) if s1[i] > s2[i]]
    base_score = sum(tower_pts[i] for i in won)
    if len(won) in (2, 3):
        return base_score * 2
    return base_score

# Scenario 2: if a player wins the same number of towers among Tower 1 to 5 as among Tower 6 to 10,
# then each tower won is worth +2 points.
def w52_score(s1, s2):
    won = [i for i in range(10) if s1[i] > s2[i]]
    base_score = sum(tower_pts[i] for i in won)
    first_half = sum(1 for i in won if i < 5)
    second_half = sum(1 for i in won if i >= 5)
    if first_half == second_half:
        return base_score + 2 * len(won)
    return base_score


# A player wins a tower iff they place at least 10 more soldiers there than the opponent.
def w61_score(s1, s2):
    score = 0
    for i in range(10):
        if s1[i] >= s2[i] + 10:
            score += tower_pts[i]
    return score

# Exact same as wo63 and reroutes to it
def w62_score(s1, s2):
    return wo63_score(s1, s2)


# All previous scenarios at the same time, combined together!!!
def omni_score(s1, s2):
    return w11_score(s1, s2) + w12_score(s1, s2) + wo11_score(s1, s2) + wo12_score(s1, s2) + wo21_score(s1, s2) + wo22_score(s1, s2) + wo31_score(s1, s2) + wo32_score(s1, s2) + wo41_score(s1, s2) + wo42_score(s1, s2) + wo51_score(s1, s2) + wo52_score(s1, s2) + wo53_score(s1, s2) + wo61_score(s1, s2) + wo62_score(s1, s2) + wo63_score(s1, s2) + wo71_score(s1, s2) + wo72_score(s1, s2) + wo73_score(s1, s2)
