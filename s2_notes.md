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
    [4, 5, 6, 6, 6, 6, 27, 28, 6, 6] arena (top cut) [6th]

    hypotheses: people will put 5 a lot to capture 0s
    people will play a number around 4 in their unused 8/9/10
    the average 8/9/10 allocation is around high 20s


## w22:
    [0, 0, 0, 1, 3, 2, 2, 28, 35, 29] arena
    [1, 2, 3, 4, 8, 3, 3, 1, 37, 38] arena (top cut, pool=200) [wins actually]
    [0, 1, 1, 2, 2, 2, 2, 0, 51, 39] manual

    hypotheses:
    k=1: [0, 0, 0, 0, 0, 0, 0, 33, 34, 33]
    8+9+10 + 14 = 41
    k=2: [0, 1, 1, 1, 1, 1, 1, 0, 48, 47]
    k=3: [0, 1, 1, 2, 2, 2, 2, 0, 51, 39]


## w31:
    [2, 4, 7, 14, 14, 14, 14, 4, 14, 13] arena
    [0, 4, 7, 12, 15, 19, 0, 14, 15, 14] arena topcut
    [2, 3, 3, 3, 8, 16, 16, 16, 16, 17] manual

## w32:
    [2, 4, 6, 11, 15, 16, 22, 4, 7, 13] arena
    [0, 4, 7, 12, 15, 15, 0, 16, 16, 15] arena topcut


## w41:
    [3, 5, 8, 16, 19, 3, 4, 28, 7, 7] arena

## w42:
    [0, 0, 2, 4, 12, 21, 27, 28, 3, 3] arena
    [0, 0, 0, 0, 0, 0, 30, 35, 35, 0] manual

## w51:
    [0, 0, 0, 0, 0, 0, 0, 31, 35, 34] arena all
    [0, 0, 0, 0, 1, 0, 0, 43, 0, 56] manual
    
## w52:
    [0, 0, 11, 13, 3, 3, 26, 3, 36, 5] arena all

## w61:
    [0, 0, 0, 0, 0, 0, 0, 37, 42, 21] norm
    [0, 0, 11, 12, 12, 12, 12, 41, 0, 0] topcut

    [0, 0, 0, 22, 22, 12, 23, 10, 11, 0] off topcut
    [0, 0, 0, 11, 12, 22, 11, 0, 0, 44]
    [0, 0, 0, 22, 22, 12, 24, 10, 10, 0]
    [0, 10, 13, 10, 10, 12, 23, 0, 10, 12]
    [0, 0, 11, 12, 12, 12, 12, 41, 0, 0]
    [0, 0, 0, 0, 0, 0, 0, 33, 34, 33]
    [0, 0, 0, 0, 0, 0, 0, 33, 34, 33]
    [0, 0, 0, 0, 0, 0, 0, 33, 34, 33]
    [1, 1, 1, 1, 1, 1, 1, 30, 42, 21]

## w62
    exact same as ow63 but upped the numbers a bit in case anyone remembers it (update: nobody did)
    [0, 1, 2, 2, 3, 3, 3, 4, 6, 6] strategy that I made up

## w71
    [2, 3, 3, 5, 3, 20, 20, 20, 4, 20] arena all
    
    [3, 5, 3, 8, 7, 0, 2, 22, 27, 23] arena
    trained using (from topcut):
    [3, 4, 7, 7, 6, 3, 1, 21, 26, 22]
    [2, 4, 6, 6, 20, 20, 0, 2, 20, 20]
    [0, 20, 20, 20, 20, 20, 0, 0, 0, 0]
    [1, 2, 2, 5, 20, 20, 20, 20, 5, 5]
    [2, 3, 3, 5, 3, 20, 20, 20, 4, 20]
    [2, 2, 2, 2, 2, 2, 20, 20, 20, 28]
    [3, 5, 6, 0, 0, 20, 20, 20, 25, 1]
    [1, 1, 2, 5, 10, 20, 20, 20, 20, 1]
    [0, 0, 0, 0, 20, 20, 20, 20, 20, 0]

## w72
    [2, 3, 4, 5, 3, 19, 27, 28, 4, 5] arena all
    [2, 2, 2, 2, 2, 23, 27, 28, 6, 6] arena topcut (from all)
    
## w73
    [0, 4, 5, 4, 4, 16, 24, 4, 35, 4] arena all
    [0, 5, 5, 6, 8, 4, 3, 29, 35, 5] arena topcut (from all)

## w81?
    [1, 5, 5, 9, 9, 9, 9, 1, 23, 29]

    arena all, modified
    [2, 6, 9, 9, 9, 9, 9, 29, 9, 9]
    
    trained (topcut) on
    [0, 12, 11, 11, 11, 11, 11, 11, 11, 11]
    [0, 0, 14, 12, 12, 12, 12, 12, 12, 12]
    [0, 0, 0, 16, 14, 14, 14, 14, 14, 14]
    [0, 0, 0, 0, 20, 16, 16, 16, 16, 16]
    [0, 0, 0, 0, 0, 24, 19, 19, 19, 19]
    [0, 0, 0, 0, 0, 0, 28, 24, 24, 24]
    [0, 0, 0, 0, 0, 0, 0, 34, 33, 33]
    [0, 0, 0, 0, 0, 0, 0, 0, 51, 50]

    w82 and w83 made manually

## w82	
    [4, 5, 7, 13, 17, 19, 24, 2, 4, 5] arena

## w83
    [3, 3, 3, 3, 3, 8, 16, 8, 16, 8] manual
    (this is a collaborative strategy, other strategies can play on towers 9/7/5 or 10/8/6,
    which will sabotage each other, this strategy is built to succeed off either of those)