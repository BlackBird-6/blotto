Following are a bunch of notes that I took over the course of the tournament, some from backtesting and some from trying to find submissions for the actual tournament (they get more organized as it progresses)

## w11 strategies
    [2, 4, 6, 9, 11, 17, 24, 22, 2, 3]
    [2, 4, 11, 2, 21, 22, 27, 2, 6, 3]
    [2, 3, 3, 8, 11, 2, 22, 22, 24, 3]
    [2, 3, 6, 9, 11, 15, 22, 27, 2, 3]

## w12 strategy optimized off w11 arena
    [2, 4, 6, 8, 11, 21, 22, 22, 2, 2]

## w11 strategy optimized off w11+w12 arena
    [2, 3, 3, 9, 2, 22, 23, 27, 6, 3]

# w21:
    [0, 0, 0, 0, 0, 0, 0, 5, 44, 51] mode=1
    [0, 0, 0, 0, 3, 8, 32, 37, 18, 2] mode-1 with w12_algos extend
    [0, 0, 1, 2, 5, 7, 31, 34, 14, 6] mode-1 with good_algos extend
    [0, 0, 0, 0, 1, 1, 22, 27, 26, 23] arena on w11+w12
    [0, 0, 0, 0, 0, 1, 0, 5, 44, 50] winner of good
    [0, 0, 1, 2, 6, 13, 28, 9, 0, 41] arena on good

# w22:
    [0, 1, 4, 15, 22, 22, 23, 2, 7, 4] arena on w11+w12
    [0, 2, 4, 11, 16, 21, 22, 21, 1, 2] arena on w11

# w31:
    [1, 4, 5, 1, 12, 15, 2, 1, 28, 31] arena off w11 min_soldiers=1
    [0, 5, 6, 0, 12, 17, 2, 27, 28, 3] arena off w11
    [0, 3, 4, 0, 17, 22, 0, 23, 28, 3] arena off w11+w12
    [0, 2, 3, 0, 17, 22, 1, 23, 28, 4] arena off all
    [2, 3, 3, 2, 2, 22, 24, 3, 28, 11] arena off all min_soldiers=2
    [1, 2, 3, 1, 17, 22, 1, 23, 26, 4] arena off all but w21 min_soldiers=1
    [1, 5, 7, 1, 11, 17, 3, 22, 31, 2] arena off w11 + some mode 1 samples

# w32:
    [2, 5, 7, 2, 2, 23, 27, 24, 6, 2] arena off w11+w12
    [2, 2, 2, 2, 2, 2, 23, 32, 29, 4] arena off all probably killed by w21
    [2, 3, 3, 2, 2, 3, 25, 27, 28, 5] arena off all but w21 so maybe not
    [2, 4, 6, 9, 11, 21, 25, 21, 1, 0] arena off w11

better w31 strategy optimized off w11+w21
    [0, 3, 4, 0, 14, 17, 2, 27, 31, 2]

# w41:
    [1, 2, 6, 9, 2, 22, 23, 27, 6, 2] arena w11+w12
    [1, 1, 4, 5, 7, 4, 31, 1, 43, 3] arena w12
    [1, 2, 3, 2, 2, 2, 27, 28, 31, 2] arena all
    [1, 1, 4, 5, 7, 4, 31, 1, 43, 3] arena on w32
    [1, 2, 3, 2, 2, 15, 22, 23, 28, 2] arena w11+w21
    [1, 2, 3, 2, 3, 23, 27, 28, 7, 4] arena w12+w21

# w42:
    [2, 4, 3, 2, 2, 2, 23, 27, 3, 32] arena w11+w12 AND w11+w21 (yeah they gave the same strategy)
    [2, 2, 3, 2, 3, 2, 23, 28, 3, 32] arena all
    [2, 3, 3, 4, 4, 4, 22, 27, 28, 3] existing champion (ACTUALLY wins in w42)


# w51:
    [1, 1, 2, 2, 1, 2, 22, 26, 32, 11] existing champion
    [0, 0, 3, 2, 2, 2, 27, 23, 35, 6] arena all
    [0, 1, 1, 2, 2, 17, 23, 22, 28, 4] arena w11+w21
    [0, 0, 0, 0, 10, 4, 15, 22, 9, 40] optimized w51
    [0, 0, 1, 2, 2, 17, 23, 22, 29, 4] arena w11+w21 but I added one more zero

    I hypothesize the distribution will be largely regular, thus the distribution will
    approximate w11+w21 (standard) distribution and we will go with arena w11+w21

# w52:
    [3, 3, 4, 13, 25, 21, 19, 3, 5, 4] existing champion
    [23, 2, 3, 4, 14, 22, 22, 2, 3, 5] arena all (6th overall)
    [25, 2, 3, 9, 2, 2, 23, 24, 6, 4] arena w11+w12 (2nd overall)
    [1, 23, 3, 4, 2, 17, 22, 22, 2, 4] arena w11+w21 (mid)
    [22, 2, 3, 4, 2, 17, 21, 21, 2, 6] arena w11+w21 (seed 4002) (mid)
    [2, 23, 4, 4, 3, 15, 22, 22, 2, 3] arena w11+w21+w42
    [1, 4, 0, 3, 0, 3, 19, 20, 26, 24] optimized w52

    I hypothesize the distribution will be largely regular with a spike on tower 1 (to
    instantly clear the effects of the scenario), this largely doesnt change the strategy
    and there seems to be little benefit to assigning max to other towers,so we will go
    with arena w11+w21 again (with seed 4002 which outperforms others in all_algos tournament)


# w53:
    [11, 2, 3, 3, 3, 18, 24, 28, 3, 5] arena all
    [11, 2, 3, 4, 2, 2, 19, 27, 27, 3] arena w11+w21+w42
    [13, 3, 3, 4, 3, 15, 2, 26, 28, 3] arena w11+w21+w42 iter 50

    I hypothesize everyone will dump 11 on tower 1 (except those who dump 12)
    and the rest will be distributed somewhat regularly (i.e. like w11+w21+w42)
    so we will go with arena w11+w21+w42, iter 50 to beat those who dump 11 or 12
    (Noting if say 90% of people drop 11+ on tower 1, then there is no benefit
    to dropping 11 on tower 2 instead since then you won't gain points on t1 or t2)

    retrospective: w51 and w52 algorithms performed quite mid, the distributions actually
    dont increase linearly anymore but fall for tower 10 interestingly enough, which
    is reflective of "all" distribution and even "w11+w12", which may signal a strategy
    change for future scenarios


 # w61
    [5, 7, 10, 15, 18, 20, 22, 1, 1, 1] current champion
    [3, 5, 8, 13, 17, 22, 26, 2, 2, 2] arena all

    Looks reasonable enough, 2 on last towers to claim them if others put 0 or 1 is good too


# w62
    [0, 0, 0, 0, 0, 2, 24, 26, 26, 22] current champion (ah yes, from w32)
    [0, 0, 0, 4, 0, 22, 0, 28, 34, 12] arena all 
    [0, 0, 0, 2, 0, 22, 0, 28, 34, 14] arena all (modified)

    It is impossible to go off strictly past precedent because the first 5 towers will be
    devoid of any soldier allocations, though arena all still gives a valid looking allocation

    I also love the investment of soldiers in the 4th tower,
    so it's staying as the final solution (modified since dont think many others will come up with that)
    (it is also quite interesting that arena came up with that on its own)

# w63
    [3, 7, 2, 8, 1, 9, 5, 5, 2, 8] current champion (why did someone run this before this scenario?)
    [0, 0, 0, 1, 1, 1, 1, 1, 1, 1] arena all after I modified mutate function

    There is absolutely no past precedent and it might as well be impossible to simulate this one
    The worth of each tower in soldiers is [2, 4, 6, 8, 10, 12, 14, 16, 18, 20] so allocating
    any less than that and winning is strictly beneficial (losing is non-beneficial)
    However, if everyone else allocates a lot, then it is optimal to allocate practically nothing

    [0, 1, 2, 2, 3, 3, 3, 4, 6, 6] strategy that I made up


    retrospective: intuition on w61 was perfect and it won first place
    w62 performed quite mid, this one's on me since the distribution is much more heavily weighted on towers 6-10 which I should have accounted for in training, so that's probably the reason why (note for next time)
    intuition on w63 was also perfect and it won first place, thought that would be a toss up so happy it worked in my favor

# w71
    [1, 2, 3, 2, 2, 2, 26, 27, 33, 2] current champion
    [1, 1, 2, 2, 2, 2, 27, 28, 2, 33] arena all
    [0, 0, 1, 1, 2, 1, 0, 28, 34, 33] arena on w41 onwards
    [1, 1, 1, 2, 3, 2, 2, 3, 43, 42] arena on w62

    previously arena all has worked pretty well but I am skeptical that the
    distribution will probably be irregular and front-focused due to the gimmick
    w62 follows essentially exactly what I expect the distribution to be like,
    and so I will choose arena on that for my strategy

# w72
    [0, 1, 1, 2, 2, 1, 24, 23, 23, 23] current champion
    [2, 2, 9, 0, 0, 21, 26, 1, 2, 37] arena all
    
    I feel like anything I come up with in arena is going to be overfitted
    and wont have any relation to what people will put in the actual tournament
    so this will be another time I submit manually
    I suspect people will want to pair all of their soldiers, and if everyone
    does this, then anyone who does not do this puts themselves
    at a disadvantage (because you won't win/lose towers in even pairs and thus lose score)
    So, I will also pair my soldiers for essentially 5 tower blotto 

    [1, 1, 4, 4, 11, 11, 2, 2, 32, 32] strategy I made up

# w73
    [2, 3, 3, 4, 4, 4, 22, 27, 28, 3] current champion (this is also current champion on w11 vs all algos)
    [1, 3, 3, 3, 3, 2, 24, 27, 29, 5] arena all (this also wins on w11 rules vs all algos) (seed 402 b/c I forgot to change it back)
    [1, 3, 3, 3, 13, 19, 23, 27, 3, 5] arena all (seed 42) (this also wins on w11 vs all algos)
    [1, 3, 4, 4, 3, 22, 24, 28, 6, 5] arena all ON W11 RULES (this also wins on w73 vs all algos)
    [3, 3, 5, 5, 3, 19, 25, 29, 3, 5] arena on later algos

    As expected this scenario is practically identical to w11, since you will in
    practice never encounter the gimmick if you just play soldiers which are close
    to what other people play, which is already what you should be doing anyway
    so I will just use arena all and that's a wrap on Colonel Blotto!
