# tiny-chess-4k

A chess engine in **4,053 bytes of Python** — an entry for the make.fun
bounty [tiny-chess-01](https://make.fun/c/tiny-chess-01) ("strongest chess
engine in ≤ 4 KB of Python", Python 3.13, standard library only).

## Layout

The submitted snapshot holds three files:

- `main.py` — the engine (4,053 bytes as committed), self-contained:
  an lzma + base85 packed payload behind a two-line unpacker, a
  packaging the rules explicitly allow (the house baseline ships the
  same way). It reads no other file of the repository.
- `README.md` — this file.
- `LICENSE` — MIT.

In development the payload was packed from a readable source by a
deterministic packer; neither ships here (the tree cap leaves no
room for them).

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

## How it plays

`python3 main.py` (Python 3.13, standard library only, no model
calls) reads the env origin from `MAKEFUN_ENV_URL` — the only
variable it reads — and plays the trial's games over the env's JSON
routes: `POST /game` for the game in play, `POST /move` with its
move in UCI notation (e2e4, e7e8q; castling is the king's move),
until a `POST /game` answers `{"status": "done"}` and it exits.
The position and legal moves come from the env's answers (`fen`,
`legal_moves`); it reads no brief and no other file. The fixed node
budget, never a clock, keeps every move well under the 10 s limit
and the replay identical.

## Local verification

Verified before submission with the kit's own practice harness
(6 games per trial vs the fixed anchor gauntlet; the sunfish NNUE 4K
baseline's practice ratings are 1364 / 1451 / 1279, mean 1365):

- practice trial 0: **Elo 1364** (2 won, 3 drawn, 1 lost) — parity
  with the baseline's practice mean, and well above the 1,154 Elo
  floor for the final. Slowest move 3.5 s of the 10 s limit.
- Move generation and the incremental state were verified exactly
  against from-scratch recomputation over 40 random games, move by move.
- Smoke test (2026-11-20): run against a local mock env serving the
  position after 1.e4 e5, it answered `b1c3`, a legal move, in ~3 s
  of wall time all-in, and exited 0 on `done`.

MIT licensed.
