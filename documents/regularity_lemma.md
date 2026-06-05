---
categories:
- research_paper
date: ''
source: "Tao, T. (2006). 'Szemer\xE9di's regularity lemma revisited.' Contributions\
  \ to Discrete Mathematics, 1(1), 8\u201328. arXiv:math/0504472."
title: "Szemer\xE9di's regularity lemma revisited"
url: ''
---
This paper, published in Contributions to Discrete Mathematics in 2006, revisits Szemerédi's
regularity lemma from the perspectives of probability theory and information theory, providing
a slightly stronger variant with a cleaner proof.

Szemerédi's theorem (1975) states that any subset of the integers with positive upper density
contains arbitrarily long arithmetic progressions. The regularity lemma, a key tool in its
combinatorial proof, says that any large dense graph can be partitioned into a bounded number
of parts such that most pairs of parts behave 'quasi-randomly'.

In this paper, I reframe the regularity lemma probabilistically: rather than partitioning a
graph into parts, one conditions on a sigma-algebra that captures the 'structured' information.
This information-theoretic perspective makes the energy increment argument particularly
transparent — each refinement of the partition increases the 'energy' (conditional entropy),
which is bounded, so the process must terminate.

Gowers's quantitative proof of Szemerédi's theorem (1998) established the first reasonable
bounds on how large a progression-free set can be, using Gowers uniformity norms and an
energy increment method. However, the resulting bounds are tower-exponential in the
progression length k. Improving these bounds — for example, to polynomial in 1/δ — remains
a major open problem. For 3-term progressions, the breakthrough of Kelley and Meka (2023)
achieved sub-polynomial bounds, a dramatic recent advance.
