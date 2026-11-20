# tiny-chess-4k

A chess engine in **4,053 bytes of Python** — an entry for the make.fun
bounty [tiny-chess-01](https://make.fun/c/tiny-chess-01) ("strongest chess
engine in ≤ 4 KB of Python", Python 3.13, standard library only).

## Layout

- `main.py` — the submitted engine (4,053 bytes as committed). It is an
  lzma + base85 packed form of `engine.py` behind a two-line unpacker,
  a packaging the rules explicitly allow (the house baseline ships the
  same way).
- `engine.py` — the full readable source, and itself a runnable bot.
- `pack.py` — regenerates `main.py` from `engine.py` deterministically.

## Engine design

- 0x88 board, incremental make/unmake with incremental Zobrist hash
  (own LCG keys — never Python's randomized `hash()`), material/PST
  accumulators and phase tracking.
- Negamax alpha-beta with PVS, iterative deepening under a **fixed
  90,000-node budget** (never a clock — searches are replay-deterministic),
  transposition table, null-move pruning, late move reduction, check
  extensions, and quiescence search (captures; all moves when in check)
  folded into the main search at depth ≤ 0.
- Move ordering: TT move, MVV-LVA captures, promotions, killer moves.
- Tapered evaluation: Michniewski piece-square tables (midgame/endgame,
  separate endgame king table), bishop-pair bonus. Root moves are
  filtered against the environment's `legal_moves` list; in-search
  repetition and game-history positions score as draws.
- Protocol: reads `MAKEFUN_ENV_URL`, plays via `POST /game` and
  `POST /move` as the kit specifies.

## Local verification

Verified before submission with the kit's own practice harness
(6 games per trial vs the fixed anchor gauntlet; the sunfish NNUE 4K
baseline's practice ratings are 1364 / 1451 / 1279, mean 1365):

- practice trial 0: **Elo 1364** (2 won, 3 drawn, 1 lost), slowest move
  3.5 s of the 10 s limit, well inside the trial wall budget.
- Move generation and the incremental state were verified exactly
  against from-scratch recomputation over 40 random games, move by move.

MIT licensed.
