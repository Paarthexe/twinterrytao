---
categories:
- research_paper
date: ''
source: Tao, T. (2022). 'Almost all orbits of the Collatz map attain almost bounded
  values.' Forum of Mathematics, Pi, 10, e12.
title: Almost all orbits of the Collatz map attain almost bounded values
url: ''
---
This paper, published in Forum of Mathematics, Pi in 2022 (preprint 2019), makes partial
progress on the Collatz conjecture — one of the most famous unsolved problems in mathematics.

The Collatz conjecture (or 3n+1 problem) states that starting from any positive integer N and
repeatedly applying the map n ↦ n/2 (if n even) or n ↦ 3n+1 (if n odd), the orbit eventually
reaches 1. Despite its elementary statement, no proof is known.

My result establishes that for any function f(N) tending to infinity (no matter how slowly),
the minimum value Col_min(N) attained by the Collatz orbit of N satisfies Col_min(N) ≤ f(N)
for almost all N, in the sense of logarithmic density. In other words, almost all Collatz
orbits eventually descend to values that are arbitrarily small relative to the starting point.

The proof takes a probabilistic approach: rather than tracking individual orbits deterministically,
I study the statistical distribution of orbits from random starting points. The key technical
tool is analysis of the Syracuse random variable — a probabilistic model for one step of the
Collatz iteration — via its characteristic function on a 3-adic cyclic group.

The result significantly strengthens earlier bounds (such as Korec's Col_min(N) ≤ N^θ for
θ ≈ 0.79) but does not prove the full conjecture. The final step — showing orbits reach
exactly 1 — appears to require fundamentally new ideas beyond current methods.
