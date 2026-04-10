# Colonel Blotto Evolutionary Strategy Optimizer

An evolutionary optimization toolkit for the [Colonel Blotto](https://en.wikipedia.org/wiki/Blotto_game) game, built to discover high-performing soldier allocation strategies across a variety of weekly scoring scenarios. This project won first place out of 175 participants in the Waterloo Quant Club's Colonel Blotto Tournament.

## The Game

Colonel Blotto is a resource-allocation game. Two players simultaneously distribute **100 soldiers** across **10 towers**. Each tower is worth points equal to its index (Tower 1 = 1 pt, Tower 10 = 10 pts). Whoever allocates more soldiers to a tower wins that tower's points. The player with the higher total score wins.

This project extends the base game with **17 scoring variants** (labeled `w11` through `w73`) from the Waterloo Quant Club's 2026 Colonel Blotto Tournament each introducing a twist negative-value towers, win bonuses, multipliers, and more.

There is also an omni-scenario (`omni`) that scores all 17 variants simultaneously, just for fun.

## Project Structure

```
blotto/
├── blotto.py              # Main optimizer & tournament runner
├── scoring.py             # All 17 scoring functions + dispatcher
├── sanity_checks.py       # Assertion-based correctness tests per scenario
├── avg_interactive.py     # Matplotlib strategy viewer & cumulative average browser
├── notes.ipynb            # Analysis notebook
└── algos/                 # Strategy pools (one file per scenario)
    ├── w11_algos.txt      #   ↳ Weekly scenario strategy banks
    ├── ...
    ├── w73_algos.txt
    ├── my_algos.txt       #   ↳ My strategies
    ├── extra_algos.txt    #   ↳ User-curated additional strategies
    └── out_algos.txt      #   ↳ Output: ranked results from the last run from best to worst
```

## How It Works

### Modes

| Mode | Name | Description |
|------|------|-------------|
| **1** | **Optimize (Co-evolutionary)** | Generates its own metagame. Produces a random seed pool, picks a champion, then iteratively mutates it. Each generation is evaluated against the mutant pool *plus* all historical champions, creating a co-evolving fitness landscape. Best for discovering robust generalist strategies from scratch. Largely became redundant after I discovered that arena mode was better at generating winning strategies. |
| **2** | **Optimize (Arena)** | Hill-climbs against a fixed opponent pool. Loads existing strategies from `algos/` files into a static arena, then evolves mutations scored strictly against that arena. Best for backtesting off previous human data. |
| **3** | **Tournament Simulation** | No optimization. Loads all specified strategy files and runs a round-robin tournament, ranking every strategy by average score. Useful for evaluating pools or specific strategies. |

### Evolutionary Loop (Modes 1 & 2)

```
1.  Generate pool_size random strategies (stars-and-bars sampling)
2.  Evaluate each against the reference pool → pick champion
3.  Repeat k iterations:
      a. Generate pool_size mutations of the champion
         (random soldier transfers between towers)
      b. Score mutations against the reference pool
      c. Promote the best mutant to champion
4.  Return champion + score
```

**Key parameters:**

| Parameter | Default | Purpose |
|-----------|---------|---------|
| `k` | 200 | Number of evolutionary iterations |
| `pool_size` | 100 | Candidate strategies per generation |
| `mutation_strength` | 30 | Max random soldier-transfer moves per mutation |
| `max_transfer` | 100 | Max soldiers moved in a single transfer |

## Scoring Scenarios

Each scenario (`w{week}{variant}`) modifies how tower victories translate into points:

| Scenario | Rule |
|----------|------|
| `w11` | **Baseline** - win a tower, earn its point value |
| `w12` | The *last* (highest-index) tower you win is worth **negative** points |
| `w21` | The *first* (lowest-index) tower you win is worth **triple** |
| `w22` | If you win exactly N towers and one of them *is* Tower N, your score **doubles** |
| `w31` | First tower in each consecutive winning **streak** is worth **double** |
| `w32` | An **isolated** win (no adjacent towers won) is worth **negative** |
| `w41` | If your highest-index win beats the opponent's, each tower is worth **1 less** |
| `w42` | The tower you won by the **largest margin** is worth **double** |
| `w51` | If you win strictly **more towers** than the opponent, each is worth **1 less** |
| `w52` | The won tower where you allocated the **most soldiers** is worth **0** |
| `w53` | The *first* tower you win with **>10 soldiers** is worth **0** |
| `w61` | Consecutive wins earn an **arithmetic bonus** (+0, +3, +6, …) |
| `w62` | Winning both Tower *i* and Tower *11−i* makes **both worth 0** |
| `w63` | Each **unused soldier** earns **0.5 points** |
| `w71` | Towers with ≥20 soldiers are **high risk**: double if won, negative if lost |
| `w72` | If you win more even-indexed than odd (or vice versa), the **majority group scores 0** |
| `w73` | Winning by ≥2× the opponent's allocation makes that tower worth **half** |
| `omni` | All of `w11`–`w73` scored **simultaneously** (very fun) |

## Usage

### Running the Optimizer

You can configure the tool by editing the default configuration block at the top of `main()` in `blotto.py`:

```python
SCORE_MODE = "w11"                       # Scoring scenario
extend_algos = all_algos + ["extra"]     # Strategy files to load into the arena
MODE = 2                                 # 1 = Co-evolutionary, 2 = Arena, 3 = Tournament
SHOW_ALL_SCORES = False                  # Print full or truncated leaderboard (when MODE=1 or 2)
SHOW_ALL_TOURNEY_SCORES = False          # Print full or truncated leaderboard (when MODE=3)
```

Alternatively, you can override these defaults dynamically via CLI arguments without modifying the file.

```bash
python blotto.py --SCORE_MODE w41 --extend_algos w11 w12 extra --MODE 3 --SHOW_ALL_SCORES
```

**Available CLI Arguments:**
- `--SCORE_MODE <scenario>`: Override the scoring scenario (e.g., `w71`).
- `--extend_algos <list>`: Override the imported strategy files (space-separated, e.g., `w11 w12 extra`).
- `--MODE <int>`: Override the execution mode (`1`, `2`, or `3`).
- `--SHOW_ALL_SCORES`: Prints the full leaderboard (`--no-SHOW_ALL_SCORES` to truncate).

Results are written to `algos/out_algos.txt`, ranked best-to-worst.

### Viewing Strategies

Browse the ranked output interactively with a dark-themed matplotlib viewer:

```bash
python avg_interactive.py                    # loads out_algos.txt
python avg_interactive.py algos/w42_algos.txt  # loads a specific file
```

**Controls:** ◀/▶ buttons or arrow keys to step, slider to scrub. Shows each strategy's allocation as a bar chart alongside the cumulative average of all higher-ranked strategies.

## Requirements

- Python 3.10+
- `numpy`
- `matplotlib` (for `avg_interactive.py`)
