Following are a bunch of notes that I took over the course of the tournament, some from backtesting and some from trying to find submissions for the actual tournament (they get more organized as it progresses)

## w11 strategies
    [1, 3, 3, 3, 3, 2, 24, 27, 29, 5] # w11
    [2, 3, 4, 4, 3, 21, 26, 28, 4, 5] # all
    [2, 3, 4, 5, 12, 3, 24, 4, 30, 13] # later
    [2, 5, 6, 7, 14, 18, 2, 1, 16, 29] # w73

## w12 strategies
    [3, 5, 8, 13, 17, 22, 26, 2, 2, 2] current champion
    [2, 4, 7, 12, 17, 23, 26, 4, 3, 2] all, trivial

## the game theory is strong with this one

## w21:
    [2, 4, 5, 5, 4, 18, 25, 4, 28, 5] arena
    [0, 0, 6, 6, 6, 6, 6, 31, 31, 8] manual

    hypotheses: people will put 5 a lot to capture 0s
    people will play a number around 4 in their unused 8/9/10
    the average 8/9/10 allocation is around high 20s


## w22:
    [0, 0, 0, 1, 3, 2, 2, 28, 35, 29] arena
    [1, 2, 3, 4, 8, 3, 3, 1, 37, 38] arena (top cut)
    [0, 1, 1, 2, 2, 2, 2, 0, 51, 39] manual

    hypotheses:
    k=1: [0, 0, 0, 0, 0, 0, 0, 33, 34, 33]
    8+9+10 + 14 = 41
    k=2: [0, 1, 1, 1, 1, 1, 1, 0, 48, 47]
    k=3: [0, 1, 1, 2, 2, 2, 2, 0, 51, 39]