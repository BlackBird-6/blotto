from scoring import score

# Copy paste:
# assert score([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 0
def sanity_check(scenario):

    if scenario == "w11":
        assert score([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 55
        assert score([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]) == 0

    if scenario == "w12":
        assert score([0, 1, 1, 1, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 44
        assert score([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 143

    # w21: towers won by at most 5 more soldiers are worth double
    if scenario == "w21":
       # All towers won by 1 (≤5), so all doubled: 2*55 = 110
       assert score([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 110
       # Tower 1 won by 5 (≤5) → doubled: 2*1 = 2
       assert score([5, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 2
       # Tower 1 won by 6 (>5) → not doubled: 1
       assert score([6, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 1
       # Tower 1 won by 6 (not doubled)=1, tower 2 won by 1 (doubled)=4. Total=5
       assert score([6, 2, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0, 0]) == 5

    # w22: if a player wins strictly fewer towers, they receive 2n extra points (n = opponent's tower wins)
    if scenario == "w22":
       # s1 wins 1 tower, s2 wins 2 → fewer, bonus = 2*2 = 4. Base = 1. Total = 5
       assert score([1, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 1, 0, 0, 0, 0, 0, 0, 0]) == 1 + 2*2
       # s1 wins 2, s2 wins 2 → not strictly fewer, no bonus. Total = 1+2 = 3
       assert score([1, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 1, 0, 0, 0, 0, 0, 0]) == 3
       # s1 wins 3, s2 wins 1 → more, no bonus. Total = 1+2+3 = 6
       assert score([1, 1, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0]) == 6
       # s1 wins 0, s2 wins 5 → fewer, bonus = 2*5 = 10. Base = 0. Total = 10
       assert score([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 0, 0, 0, 0, 0]) == 10
       # s1 wins 1 tower (tower 10, worth 10), s2 wins 9 → bonus = 2*9 = 18. Total = 28
       assert score([0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 0]) == 10 + 2*9

    # w31: towers won by 15 or more are worthless
    if scenario == "w31":
        # s1 allocates 14 on tower 1 (win by 14) -> gets 1 pt
        assert score([14, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 1
        # s1 allocates 15 on tower 1 (win by 15) -> gets 0 pts
        assert score([15, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 0
        # s1 allocates 16 on tower 1 (win by 16) -> gets 0 pts
        assert score([16, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 0
        # s1 allocates 10 on tower 1 (win by 9), 14 on tower 2 (win by 14) -> gets 1+2 = 3 pts
        assert score([10, 14, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 3

    # w32: if both players allocate at least 15 soldiers to a tower, then that tower is worth half the amount of points
    if scenario == "w32":
        # both >= 15: s1 allocates 16, s2 allocates 15 on tower 1 -> win, worth 1/2 = 0.5 pts
        assert score([16, 0, 0, 0, 0, 0, 0, 0, 0, 0], [15, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 0.5
        # s1 >= 15 but s2 < 15: s1 allocates 16, s2 allocates 14 on tower 1 -> win, worth 1 pt
        assert score([16, 0, 0, 0, 0, 0, 0, 0, 0, 0], [14, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 1.0
        # both < 15: s1 allocates 14, s2 allocates 10 on tower 1 -> win, worth 1 pt
        assert score([14, 0, 0, 0, 0, 0, 0, 0, 0, 0], [10, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 1.0

    if scenario == "wo11":
        assert score([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 55
        assert score([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]) == 0

    if scenario == "wo12":
        assert score([1, 1, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 1+2-3
        assert score([1, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == -1

    if scenario == "wo21":
        assert score([1, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 3+2
        assert score([0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 6

    if scenario == "wo22":
        assert score([1, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == (1+2)*2
        assert score([1, 0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 1+3

    if scenario == "wo31":
        assert score([1, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 1*2+2
        assert score([0, 0, 0, 1, 1, 1, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 4*2+5+6+8

    if scenario == "wo32":
        assert score([1, 1, 0, 1, 0, 1, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 1+2-4-6-8

    if scenario == "wo41":
        assert score([1, 1, 0, 1, 1, 0, 1, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 0+1+3+4+6+8
        assert score([1, 1, 0, 1, 1, 0, 1, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]) == 0+1+3+4+6+8+6

    if scenario == "wo42":
        assert score([1, 1, 0, 1, 1, 0, 1, 0, 2, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 1+2+4+5+7+18
        assert score([1, 1, 0, 1, 1, 0, 1, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 2+2+4+5+7+9
    
    if scenario == "wo51":
        assert score([1, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 0
        assert score([1, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0, 0]) == 1
        assert score([1, 0, 1, 0, 1, 0, 1, 0, 1, 0], [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]) == 1+3+5+7+9
        assert score([1, 0, 1, 0, 1, 0, 1, 0, 1, 0], [0, 1, 0, 1, 0, 1, 0, 1, 0, 0]) == 0+2+4+6+8
    
    if scenario == "wo52":
        assert score([1, 0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 1
        assert score([1, 0, 1, 0, 1, 0, 1, 0, 1, 0], [0, 1, 0, 1, 0, 1, 0, 1, 0, 0]) == 1+3+5+7+0
        assert score([1, 0, 1, 0, 1, 0, 2, 0, 1, 0], [0, 1, 0, 1, 0, 1, 0, 1, 0, 0]) == 1+3+5+0+9
    
    if scenario == "wo53":
        assert score([11, 0, 0, 0, 0, 0, 0, 0, 0, 10], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 10
        assert score([10, 0, 0, 0, 0, 0, 0, 0, 0, 10], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 1+10
        assert score([11, 11, 11, 0, 0, 0, 0, 0, 0, 0], [11, 11, 10, 0, 0, 0, 0, 0, 0, 0]) == 0
        assert score([5, 5, 5, 5, 11, 11, 0, 0, 0, 0], [11, 11, 11, 0, 11, 10, 0, 0, 0, 0]) == 4

    if scenario == "wo61":
       assert score([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 1+2+3+4+5+6+7+8+9+10+3+6+9+12+15+18+21+24+27
       assert score([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 1, 0, 0, 1, 0, 0, 1, 0]) == 1+2+3+4+5+3+7+8+3+10

    if scenario == "wo62":
       assert score([1, 1, 0, 0, 0, 0, 0, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 2+8
       assert score([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 0
       assert score([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 0, 0, 0, 0, 1, 1, 0, 0]) == 3+4+9+10

    if scenario == "wo63":
       assert score([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 50
       assert score([0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 59.5
       assert score([0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]) == 49.5
    
    if scenario == "wo71":
       assert score([20, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 2
       assert score([20, 0, 0, 0, 0, 0, 0, 0, 0, 0], [22, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == -1
       assert score([0, 20, 0, 20, 0, 20, 0, 20, 0, 20], [0, 0, 0, 0, 0, 0, 0, 0, 0, 20]) == 4+8+12+16

    if scenario == "wo72":
       assert score([1, 1, 0, 1, 0, 1, 0, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 1
       assert score([1, 1, 1, 0, 1, 0, 1, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 2
       assert score([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 1]) == 44
    
    if scenario == "wo73":
       assert score([1, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 0.5
       assert score([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 27.5
       assert score([2, 4, 6, 8, 10, 11, 13, 15, 17, 19], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) == 0.5+1+1.5+2+2.5+6+7+8+9+10

    # There is no sanity check for omni-score scenario because it is not sane.
