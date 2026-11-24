# Outbreak

Simulate an epidemic in a synthetic town: who meets whom at home, school and work, how an
infection spreads, and what testing, isolation and closures change.

> **Status: foundation only.** The project layout, tooling, closed-form SEIR results,
> age-structured contact matrices and seeded random streams exist and are tested. The town
> generator, the spread simulation, interventions and the web UI are not built yet. See
> [the plan](docs/PLAN.md).

## What it will do

- **A synthetic town**: households, schools and workplaces with realistic sizes and ages, so
  contacts come from places rather than from a formula.
- **Spread**: an agent-based SEIR model in which each person moves through exposed, infectious
  and recovered states, with seeded randomness.
- **Checks against theory**: a large, well-mixed town must grow at the rate and reach the final
  size the SEIR equations predict.
- **Interventions**: testing with imperfect tests and delays, isolation, contact tracing,
  school closures and vaccination, compared on the same seeds.
- **Live view**: a map of the town, case curves and a timeline you can replay.

The model is for exploring policies on a made-up town. It is not a forecast for any real place.

## What exists today

| Module | What it does |
|---|---|
| `outbreak.epi` | R0 and growth rate, doubling time, final size and herd immunity threshold |
| `outbreak.contacts` | Contact matrices made reciprocal, and R0 from the next-generation matrix |
| `outbreak.rng` | Named, independent random streams from one run seed |

## Quickstart

Requires [uv](https://docs.astral.sh/uv/) and Python 3.12.

```bash
make setup   # install locked dependencies
make check   # lint, format check, type check and tests
make help    # list every target
```

## Layout

```
src/outbreak/  # the simulator package
tests/         # unit and property tests
docs/PLAN.md   # what is being built, in order
docs/adr/      # architecture decision records
```

## Licence

MIT. See [LICENSE](LICENSE).
