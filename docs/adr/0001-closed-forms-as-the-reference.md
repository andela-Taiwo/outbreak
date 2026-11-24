# 0001: Closed-form SEIR results are the reference

## Status

Accepted

## Context

An agent-based epidemic model has many moving parts and is easy to get subtly wrong: an
off-by-one in the infectious period, contacts counted twice, or randomness that is not
independent between people. Such errors still produce plausible-looking curves. The SEIR
model has exact results for a large, well-mixed population: the early growth rate for a
given R0, the final size, and the herd immunity threshold. A deterministic ODE solution and
the mean of many stochastic runs must agree with them.

## Decision

- The closed forms live in `outbreak.epi` and are tested against published values.
- Every simulator, from the ODE up to the agent model, is checked against them in the limit
  where they apply: a large, well-mixed population with exponential periods.
- A standard ODE solver (SciPy) is used only to produce reference curves, in a separate,
  pinned tool environment. `make check` never needs it.

## Consequences

- Statistical checks need many seeded runs and stated tolerances, so some are slow and must be
  marked so that `make check` stays fast.
- Places (households, schools) break the well-mixed assumption on purpose. Those results are
  checked against the next-generation R0 of the town's own contact matrix instead.
