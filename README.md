# tiny-chess-4k

![make.fun](https://make.fun/badge/tiny-chess-01.svg)
![rank](https://make.fun/badge/tiny-chess-01/adzinsyariif/tiny-chess-4k/rank.svg)
![reward](https://make.fun/badge/tiny-chess-01/adzinsyariif/tiny-chess-4k/reward.svg)

A chess engine in **4,053 bytes of Python** — an entry for the make.fun
bounty [tiny-chess-01](https://make.fun/bounty/tiny-chess-01) ("strongest chess
engine in ≤ 4 KB of Python", Python 3.13, standard library only).

## Layout

The snapshot holds three files:

- `main.py` — the engine (4,053 bytes), self-contained:
  an lzma + base85 packed payload behind a two-line unpacker (the
  rules allow this; the house baseline ships the same way). It reads
  no other file.
- `README.md` — this file.
- `LICENSE` — MIT.

In development the payload was packed from a readable source by a
deterministic packer; neither ships here (no room under the tree cap).

## Engine design

- 0x88 board, incremental make/unmake with incremental Zobrist hash
  (own LCG keys, never Python's randomized `hash()`), material/PST
  accumulators and phase tracking.
- Negamax alpha-beta with PVS, iterative deepening under a **fixed
  90,000-node budget** (never a clock — searches are replay-deterministic),
  transposition table, null-move pruning, late move reduction, check
  extensions, and quiescence (captures; all moves when in check)
  folded into the main search at depth ≤ 0.
- Move ordering: TT move, MVV-LVA captures, promotions, killer moves.
- Tapered evaluation: Michniewski piece-square tables (midgame/endgame,
  separate endgame king table), bishop-pair bonus. Root moves filtered
  against the env's `legal_moves`; in-search repetition and
  game-history positions score as draws.

## How it plays

`python3 main.py` (Python 3.13, standard library only, no model
calls) reads the env origin from `MAKEFUN_ENV_URL` — the only
variable it reads — and plays over the env's JSON
routes: `POST /game` for the game in play, `POST /move` with its
move in UCI (e2e4, e7e8q; castling is the king's move),
until a `POST /game` answers `{"status": "done"}` and it exits.
Position and legal moves come from the env's answers (`fen`,
`legal_moves`); it reads no brief, no other file. The fixed node
budget, never a clock, keeps every move well under the 10 s limit
and the replay identical.

## Local verification

Verified with the kit's practice harness
(6 games per trial vs the fixed gauntlet; the sunfish NNUE 4K
baseline's practice ratings: 1364 / 1451 / 1279, mean 1365):

- practice trial 0: **Elo 1364** (2 won, 3 drawn, 1 lost) — parity
  with the baseline's mean, well above the 1,154 Elo
  floor for the final; slowest move 3.5 s of the 10 s limit.
- Move generation and incremental state verified exactly
  against from-scratch recomputation over 40 random games, move by move.
- Smoke test (2026-11-20): against a local mock env serving the
  position after 1.e4 e5, it answered `b1c3` (legal) in ~3 s
  all-in and exited 0 on `done`.

MIT licensed.
