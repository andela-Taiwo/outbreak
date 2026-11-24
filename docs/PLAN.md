# Plan

Outbreak is built in sessions, each with a clear success test. Later sessions build on
earlier ones.

| # | Session | Success |
|---|---|---|
| 1 | Synthetic town generator: people with ages, households, schools and workplaces, from a seeded configuration | Household sizes and the age mix match the configured targets; every child is in a school and every working adult in a workplace; a bad configuration lists every error |
| 2 | Deterministic SEIR model (ODE) and a stochastic version (Gillespie) for a well-mixed population | The ODE matches a reference solver; the mean of many stochastic runs matches the ODE; growth rate and final size match the closed forms in `outbreak.epi` |
| 3 | Agent-based spread through households, schools and workplaces, with seeded randomness | In a large, well-mixed setting the agent model matches the SEIR results; R0 from the town's contacts matches the next-generation estimate; runs replay exactly |
| 4 | Testing and isolation: test sensitivity and delays, symptom-based and contact-traced testing, isolation compliance | Every intervention has a test showing its effect in the expected direction; a perfect, instant test with full isolation stops spread in the tested scenarios |
| 5 | Closures and vaccination, compared on the same seeds, with costs (days of school lost, tests used) | A comparison report gives cases, peak and costs per policy with confidence intervals across seeds |
| 6 | Live engine and web UI: clock, town map, case curves, policy changes during a run, and replay | Playwright covers closing schools mid-run and comparing two policies |
| 7 | Scale: a town of a few hundred thousand people, profiling and benchmarks | A 180-day run of the large town finishes within a set budget; benchmarks fail the build on regression |

## Rules

- The references are the closed-form results in `outbreak.epi` and a standard ODE solver
  (SciPy) run in a separate tool environment. The simulator never calls SciPy.
- All randomness comes from named, seeded streams. Every run replays exactly.
- No fitting to real outbreak data and no forecasting. The town and its parameters are made up.
