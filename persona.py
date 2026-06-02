SYSTEM_PROMPT = """
STAY STRICLY UNDER THE 1500 WORD LIMIT PLEASE PLEASE
## Personality and Voice

You are Terence Tao, the famous mathematician. You are curious, reflective, collaborative, and intellectually humble. You enjoy exploring ideas rather than merely presenting conclusions. You frequently frame opinions as intuitions rather than certainties.

You are approachable and patient, but you do not sound like a motivational speaker or lecturer. You sound like a working mathematician thinking aloud, identifying obstacles, testing ideas, and refining intuitions.

You value understanding over memorization, explanation over verification, and insight over performance.

## How You Reason

Begin with intuition, toy models, special cases, or motivating examples.
Focus on what makes a problem difficult and identify the key obstruction.
Look for connections between seemingly unrelated areas.
Prefer conceptual understanding to technical complexity.
Use rigor to verify intuition, not replace it.
Freely discuss uncertainty, failed approaches, and open questions.
Explain not only why something is true, but why one might have discovered it.

## Communication Style

Use first-person language naturally ("I think...", "My intuition is...", "One way to think about it is...").
Use analogies when they genuinely clarify an idea.
Use mathematical notation when helpful, but explain it.
Be conversational rather than essay-like.
Do not automatically structure answers as numbered lists.

## Using Retrieved Context

Retrieved sources are supporting material, not a checklist.

Do NOT attempt to use every retrieved source.

Do NOT attempt to mention every relevant theorem, technique, or concept.

Use only the information that genuinely helps answer the question.

Prefer one deep idea to several shallow observations.

Do not force signature phrases.

Use them only when they naturally illuminate the discussion.

## Important Rules

Don't start questions with my intution keep it varied.
Never fabricate theorems, papers, proofs, or results.
Never present conjectures or open problems as settled facts.
Acknowledge uncertainty when appropriate.
Stay in character as Terence Tao.
When relevant, connect ideas to your own work, collaborators, or writings, but only when it adds value.

## Context from Retrieved Sources
{rag_context}

## Conversation Memory
{memory_context}
STRICTLY KEEP THE RESPONSE UNDER 1500 WORDS
"""

KNOWLEDGE_BASE = [
    {
        "id": "kb_001",
        "title": "The primes contain arbitrarily long arithmetic progressions",
        "source": "Green, B. and Tao, T. (2008). 'The primes contain arbitrarily long arithmetic progressions.' Annals of Mathematics, 167(2), 481–547.",
        "content": """The Green-Tao theorem, published in the Annals of Mathematics in 2008, proves that the
sequence of prime numbers contains arithmetic progressions of arbitrary length. That is, for
every positive integer k, there exist infinitely many arithmetic progressions of k primes.

The key challenge is that the primes have density zero in the integers, so Szemerédi's
theorem — which guarantees arithmetic progressions in sets of positive upper density — does
not directly apply. The proof overcomes this through two main innovations.

First, a transference principle: we show that the primes, while sparse, behave pseudorandomly
relative to a slightly denser set of almost-primes (the 'W-tricked' primes). This allows us
to transfer Szemerédi-type results from the dense setting to the sparse prime setting.

Second, we need quantitative control on the pseudorandomness of the primes. This is measured
using Gowers uniformity norms — specifically, we need certain normalized counts involving the
primes to satisfy the 'linear forms condition' and the 'correlation condition'. The deep
number-theoretic input comes from work of Goldston and Yıldırım on the distribution of primes.

The proof is non-effective: it does not give any explicit bound on where the first arithmetic
progression of length k among the primes begins. Finding such bounds remains open."""
    },
    {
        "id": "kb_002",
        "title": "There's more to mathematics than rigour and proofs",
        "source": "Tao, T. (2007). 'There's more to mathematics than rigour and proofs.' Blog post, terrytao.wordpress.com.",
        "content": """In this blog post from 2007 on my blog 'What's new', I describe three broad stages in a
mathematician's education and development.

In the pre-rigorous stage, typically lasting through school and early undergraduate years,
mathematics is taught informally through examples, computation, and hand-waving. Calculus is
understood through slopes and areas; limits are 'numbers getting really small'. This stage
builds essential mental pictures and computational fluency.

In the rigorous stage, beginning in upper-level undergraduate or early graduate study, students
learn that informal arguments can mislead. Everything must be proved from precise definitions.
Epsilon-delta proofs replace intuitive notions of limits. Intuition is treated with suspicion.
Many students get stuck here, confusing rigor for the ultimate goal of mathematics.

In the post-rigorous stage, which the best mathematicians eventually reach, intuition returns —
but it is now a far more reliable intuition, calibrated by years of careful formal work. The
mathematician knows which heuristics can be trusted, which need checking, and when formal
verification is necessary. Reasoning becomes fast and fluid again, but now backed by deep
understanding of the rigorous foundations.

The point of rigorous training is not to stay rigorous forever. It is to calibrate your
intuition so that you can eventually reason at a higher level with confidence."""
    },
    {
        "id": "kb_003",
        "title": "Robust uncertainty principles and compressed sensing",
        "source": "Candès, E., Romberg, J., and Tao, T. (2006). 'Robust uncertainty principles: exact signal reconstruction from highly incomplete frequency information.' IEEE Transactions on Information Theory, 52(2), 489–509.",
        "content": """This paper, published in IEEE Transactions on Information Theory in February 2006,
established one of the foundational results of compressed sensing. We showed that sparse
signals can be recovered exactly from far fewer measurements than classical sampling theory
(Shannon-Nyquist) would require.

The central question is: given a signal f that is known to be sparse (supported on a small
set T of size |T|), can we reconstruct it from a randomly chosen subset of its Fourier
coefficients? The answer is yes: with high probability, O(|T| log N) randomly selected
frequency samples suffice to recover f exactly by solving an L1 minimization problem.

This is a 'nonlinear sampling theorem' — the recovery procedure (L1 minimization, which is
a convex program) is nonlinear, unlike traditional linear reconstruction. The key mathematical
insight is a robust uncertainty principle: a signal cannot be simultaneously concentrated in
both the time domain and the frequency domain. Random sampling exploits this by ensuring that
sparse signals are 'spread out' enough to be distinguished.

The approach extends to higher dimensions and to recovery of piecewise constant objects using
total variation minimization. This work, together with a companion paper 'Decoding by linear
programming' (Candès and Tao, IEEE Trans. Inform. Theory, 2005), laid the theoretical
foundations for the field of compressed sensing."""
    },
    {
        "id": "kb_004",
        "title": "The Erdős discrepancy problem",
        "source": "Tao, T. (2016). 'The Erdős discrepancy problem.' Discrete Analysis, Article 1.",
        "content": """This paper, published in Discrete Analysis in 2016 (one of the journal's inaugural
articles), resolves the Erdős discrepancy conjecture posed in the 1930s. The conjecture
states that for any function f: N → {-1, +1}, the discrepancy sup_{n,d} |Σ_{j=1}^n f(jd)|
is infinite — one cannot assign ±1 values to integers so that all partial sums along
arithmetic progressions remain bounded.

The proof proceeds through three main steps. First, building on ideas from the collaborative
Polymath5 project, I reduce the problem from arbitrary ±1 sequences to the case of
completely multiplicative functions. This is a Fourier-analytic reduction: if the discrepancy
were bounded, then f would need to 'pretend' to be a multiplicative function.

Second, I prove a logarithmically averaged version of the Elliott conjecture on correlations
of multiplicative functions. This is the deepest analytic ingredient — it connects the
combinatorial problem to the distribution of prime factors and the behavior of the Liouville
function.

Third, I show that completely multiplicative functions that 'pretend' to be modulated
Dirichlet characters must have unbounded discrepancy. This final step extends arguments
developed during the Polymath5 project.

The result is notable as an example of analytic number theory solving a purely combinatorial
problem — a bridge between very different areas of mathematics."""
    },
    {
        "id": "kb_005",
        "title": "Finite time blowup for an averaged Navier-Stokes equation",
        "source": "Tao, T. (2016). 'Finite time blowup for an averaged three-dimensional Navier-Stokes equation.' Journal of the American Mathematical Society, 29(3), 601–674.",
        "content": """This paper, published in the Journal of the AMS in 2016 (originally a 2014 preprint,
arXiv:1402.0290), demonstrates that an averaged version of the 3D incompressible Navier-Stokes
equations can develop singularities in finite time.

The Navier-Stokes existence and smoothness problem — one of the seven Millennium Prize
Problems — asks whether smooth solutions to the true 3D Navier-Stokes equations can blow up.
My result addresses a modified equation ∂_t u = Δu + B̃(u,u), where B̃ is an averaged
bilinear operator that replaces the standard Navier-Stokes nonlinearity via rotations,
dilations, and Fourier multipliers of order zero.

Crucially, this averaged equation obeys the same energy identity as the true Navier-Stokes
equations. The blowup construction builds a 'machine' from fluid: a carefully designed
sequence of structures that transfer energy to ever-smaller spatial scales at an exponentially
accelerating rate, producing infinite energy density in finite time.

This does not solve the Millennium Problem — the true Navier-Stokes nonlinearity has finer
structure that the averaged version lacks. But the result shows that any proof of global
regularity must exploit properties beyond the energy identity and standard harmonic analysis
estimates. It rules out a broad class of proof strategies and clarifies what the genuine
difficulty is."""
    },
    {
        "id": "kb_006",
        "title": "Random matrices: universality of local eigenvalue statistics",
        "source": "Tao, T. and Vu, V. (2011). 'Random matrices: Universality of local eigenvalue statistics.' Acta Mathematica, 206(1), 127–204.",
        "content": """This paper, published in Acta Mathematica in 2011 (preprint arXiv:0906.0510, 2009),
establishes the universality of local eigenvalue statistics for Wigner matrices.

Random matrix theory studies the eigenvalue distributions of large matrices with random
entries. The phenomenon of universality says that local eigenvalue statistics — such as the
gap distribution between consecutive eigenvalues and k-point correlation functions — depend
only on the first few moments of the entry distribution, not on its specific form.

The main result is the Four Moment Theorem: if two Wigner matrix ensembles match in their
first four moments entry-by-entry, then their local eigenvalue statistics in the bulk of the
spectrum are asymptotically identical. This confirms that the statistics of the Gaussian
Unitary Ensemble (GUE), described by determinantal point processes with the sine kernel,
are universal.

The proof uses a Lindeberg replacement strategy: replace matrix entries one at a time from
one ensemble to another, and control how eigenvalue statistics change at each step. This
requires delicate estimates on eigenvalue perturbations, including a quantitative version
of eigenvalue repulsion — the fact that eigenvalues of random Hermitian matrices tend to
repel each other.

The result applies to both Hermitian and real symmetric Wigner matrices under mild assumptions
(mean zero, unit variance, matching moments)."""
    },
    {
        "id": "kb_007",
        "title": "The inverse conjecture for the Gowers norms",
        "source": "Green, B., Tao, T., and Ziegler, T. (2012). 'An inverse theorem for the Gowers U^{s+1}[N]-norm.' Annals of Mathematics, 176(2), 1231–1372.",
        "content": """This paper, published in the Annals of Mathematics in 2012, proves the Inverse Conjecture
for the Gowers uniformity norms over the integers for all s ≥ 1.

The Gowers uniformity norms ||f||_{U^k} measure higher-order Fourier structure. The U^2 norm
detects correlation with linear exponential phases (classical Fourier analysis). For k ≥ 3,
the U^k norm detects correlation with polynomial phases and, more generally, with nilsequences.

The inverse theorem states: if a bounded function f: [N] → [-1,1] has large U^{s+1}[N] norm
(||f||_{U^{s+1}} ≥ δ), then f must correlate with an s-step nilsequence F(g(n)Γ) of bounded
complexity. Here g is an element of a nilpotent Lie group G, Γ is a lattice, and F is a
Lipschitz function on the nilmanifold G/Γ.

This is a far-reaching generalization of Fourier analysis: classical Fourier analysis captures
degree-1 structure (linear phases e^{2πiαn}), while the inverse conjecture shows that
higher-degree structure is captured by nilsequences — objects arising from nilpotent group
theory.

The cases s = 1 (Fourier analysis) and s = 2 (quadratic phases) were known earlier. The
general case for s ≥ 3 was the new contribution. These norms are foundational tools in
additive combinatorics, particularly in counting arithmetic progressions in dense sets of
integers and in the proof of the Green-Tao theorem."""
    },
    {
        "id": "kb_008",
        "title": "Strategies in problem solving",
        "source": "Tao, T. (2006). 'Solving Mathematical Problems: A Personal Perspective.' 2nd edition, Oxford University Press.",
        "content": """This book, first published by Deakin University Press in 1992 (when I was 15) and expanded
into a second edition by Oxford University Press in 2006, discusses problem-solving strategies
through worked examples from number theory, algebra, analysis, and geometry.

When attacking a hard problem, I follow a rough hierarchy of strategies.

First, understand the problem fully. Solve special cases, try small examples and low
dimensions. Identify the 'enemy': what would the worst-case counterexample look like?

Second, look for analogies. Does this resemble something already solved? Can you reduce it
to a known result? Often the deepest insight is recognizing that two apparently different
problems are really the same problem in disguise.

Third, try to prove something weaker. Can you get the result up to logarithmic factors, or
under additional hypotheses? The weaker result often reveals the key structure needed for
the full problem.

Fourth, work backwards from the desired conclusion. What would you need to assume to make
the proof work? This is what I have sometimes called the 'Italian method'.

Fifth, search for the obstruction. If you cannot prove something, there may be a good reason.
Can you construct a counterexample, or a 'near-counterexample' that reveals the true
difficulty?

Finally, be willing to abandon a wrong approach. Sunk cost fallacy kills mathematical
projects. A clean restart from a fresh perspective often succeeds where patching fails."""
    },
    {
        "id": "kb_009",
        "title": "The Bochner-Riesz conjecture implies the restriction conjecture",
        "source": "Tao, T. (1999). 'The Bochner-Riesz conjecture implies the restriction conjecture.' Duke Mathematical Journal, 96(2), 363–376.",
        "content": """This paper, published in the Duke Mathematical Journal in 1999, establishes that the
Bochner-Riesz conjecture implies the restriction conjecture for the Fourier transform. This
complemented earlier work by Anthony Carbery showing the reverse implication, thereby
proving the two conjectures are logically equivalent.

The restriction conjecture asks: for which exponents p can we meaningfully restrict the
Fourier transform of an Lp function to a curved surface like the sphere? The Bochner-Riesz
conjecture concerns the convergence of certain summability means of Fourier integrals.

Both conjectures are deeply connected to the Kakeya conjecture, which asks whether a compact
set in Rn containing a unit line segment in every direction must have Hausdorff dimension n.
In R^2 this is resolved (Besicovitch sets of measure zero exist), but the dimension question
remains open in dimensions n ≥ 3.

My early work showed that these geometric problems connect to additive combinatorics. The key
quantity is how much a collection of tubes (thickened line segments pointing in different
directions) can overlap, which relates to combinatorial questions about sums and products of
sets. These connections between harmonic analysis, geometric measure theory, and combinatorics
have been a recurring theme throughout my career.

Recently, Hong Wang and Joshua Zahl proved the Kakeya conjecture in three dimensions (2025),
resolving a central open problem in the field."""
    },
    {
        "id": "kb_010",
        "title": "What is good mathematics?",
        "source": "Tao, T. (2007). 'What is good mathematics?' Bulletin of the American Mathematical Society, 44(4), 623–634.",
        "content": """This essay, published in the Bulletin of the AMS in 2007, reflects on how to evaluate
the quality of mathematical work. Rather than a single rigid definition, I propose a list
of criteria — not exhaustive — that characterize 'good' mathematics.

Good mathematics can mean many things: solving a famous open problem, providing an unexpected
new proof of a known result, establishing connections between previously unrelated areas,
introducing a powerful new technique or framework, asking a good question, or giving a
particularly illuminating exposition of known mathematics.

A central observation is that good mathematics in one sense tends to beget good mathematics
in other senses. A good theorem often leads to new conjectures, new techniques, and new
connections. This leads me to tentatively conjecture that there may be a somewhat universal
notion of mathematical quality, of which these various criteria are different facets.

The essay includes a detailed case study of Szemerédi's theorem and its surrounding mathematics
to illustrate how these different aspects of quality interact and build on each other over
decades.

I believe strongly in the value of collaboration — working with Ben Green, Emmanuel Candès,
Van Vu, and many others has been central to my best work. The Polymath project demonstrates
that mathematics can even be done openly and collectively online. And the 'lone genius' model
of mathematical discovery is largely a myth — sustained work, collaboration, and community
matter far more than raw talent."""
    },
    {
        "id": "kb_011",
        "title": "The dichotomy between structure and randomness",
        "source": "Tao, T. (2007). 'The dichotomy between structure and randomness, arithmetic progressions, and the primes.' In: Proceedings of the International Congress of Mathematicians, Madrid, 2006. European Mathematical Society, 581–608. arXiv:math/0512114.",
        "content": """This paper, my ICM 2006 lecture published in the Congress proceedings, surveys a central
theme running through much of modern combinatorics, number theory, and analysis: the
dichotomy between structure and randomness.

In many problems, one can decompose any mathematical object into a 'structured' part (close
to some algebraic, arithmetic, or low-complexity object) and a 'pseudorandom' part (behaving
like random noise for the purposes at hand). The structured part requires algebraic or
number-theoretic tools, while the pseudorandom part can be handled by probabilistic or
ergodic-theoretic arguments.

In the proof of the Green-Tao theorem, the primes are decomposed relative to a pseudorandom
measure. The 'structured' component correlates with nilsequences, while the 'pseudorandom'
component satisfies Gowers uniformity estimates.

This dichotomy appears throughout mathematics: in harmonic analysis as major arcs versus minor
arcs in the Hardy-Littlewood circle method; in additive combinatorics as the contrast between
structured sets (arithmetic progressions, cosets) and random-like sets; in PDE as the
distinction between coherent structures (solitons, vortices) and dispersive radiation.

The key challenge is always making the dichotomy precise and quantitative. What exactly does
'pseudorandom' mean? Different problems require different notions — Gowers uniformity norms
capture one notion, while mixing conditions or discrepancy conditions capture others."""
    },
    {
        "id": "kb_012",
        "title": "Szemerédi's regularity lemma revisited",
        "source": "Tao, T. (2006). 'Szemerédi's regularity lemma revisited.' Contributions to Discrete Mathematics, 1(1), 8–28. arXiv:math/0504472.",
        "content": """This paper, published in Contributions to Discrete Mathematics in 2006, revisits Szemerédi's
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
achieved sub-polynomial bounds, a dramatic recent advance."""
    },
    {
        "id": "kb_013",
        "title": "Nonlinear dispersive equations: local and global analysis",
        "source": "Tao, T. (2006). 'Nonlinear Dispersive Equations: Local and Global Analysis.' CBMS Regional Conference Series in Mathematics, No. 106. American Mathematical Society.",
        "content": """This monograph, published by the AMS in 2006 as CBMS No. 106, is based on lectures from an
NSF-CBMS regional conference at New Mexico State University in June 2005. It covers techniques
for studying nonlinear dispersive and wave equations, with emphasis on global existence,
regularity, and scattering theory.

The core equations studied include the nonlinear Schrödinger equation (NLS), nonlinear wave
equation (NLW), Korteweg-de Vries (KdV) equation, and wave maps. A central question is:
given smooth initial data, does the solution remain smooth for all time (global wellposedness),
or can singularities form?

Key analytical tools developed in the text include: Strichartz estimates (spacetime bounds
that prevent excessive concentration), X^{s,b} spaces for bilinear estimates, gauge
transformations, and conservation laws.

The I-method (method of almost conservation laws), developed with Colliander, Keel, Staffilani,
and Takaoka, is a major technique presented here. It introduces a smoothed-out operator I and
shows that a modified energy E(I[u]) is 'almost conserved' — it changes very slowly — allowing
global wellposedness to be established below the energy threshold.

For energy-critical equations, the text develops concentration-compactness methods: assuming
blowup occurs, one extracts a 'minimal blowup solution' with special compactness properties,
then derives a contradiction from these properties."""
    },
    {
        "id": "kb_014",
        "title": "Bounded gaps between primes (Polymath8 and the Maynard-Tao method)",
        "source": "D.H.J. Polymath (2014). 'Variants of the Selberg sieve, and bounded intervals containing many primes.' Research in the Mathematical Sciences, 1, Article 12. See also: Maynard, J. (2015). 'Small gaps between primes.' Annals of Mathematics, 181(1), 383–413.",
        "content": """In May 2013, Yitang Zhang proved a landmark result: there are infinitely many pairs of
consecutive primes differing by at most 70 million. This was the first-ever finite bound on
gaps between primes — a breakthrough toward the twin prime conjecture.

I initiated the Polymath8 project on my blog to collaboratively optimize Zhang's argument.
The first phase (Polymath8a) refined Zhang's method and reduced the bound to 4,680.

Independently, in late 2013, James Maynard and I discovered (separately) a fundamentally
different approach using a multidimensional Selberg sieve. Unlike the one-dimensional sieve
of Goldston-Pintz-Yıldırım that Zhang had modified, the Maynard-Tao method optimizes over
a higher-dimensional space of sieve weights, achieving much stronger results with a simpler
argument.

The second phase of Polymath (Polymath8b) incorporated Maynard's multidimensional sieve
and further optimized it, reducing the unconditional bound to 246. Under the generalized
Elliott-Halberstam conjecture, the bound drops to 6.

A key additional result of the Maynard-Tao method: for any m, there are infinitely many
bounded intervals containing at least m primes. This goes well beyond pairs — it shows
primes cluster in bounded-length intervals to arbitrary multiplicity. The twin prime conjecture
(gap of 2) remains open."""
    },
    {
        "id": "kb_015",
        "title": "Almost all orbits of the Collatz map attain almost bounded values",
        "source": "Tao, T. (2022). 'Almost all orbits of the Collatz map attain almost bounded values.' Forum of Mathematics, Pi, 10, e12.",
        "content": """This paper, published in Forum of Mathematics, Pi in 2022 (preprint 2019), makes partial
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
exactly 1 — appears to require fundamentally new ideas beyond current methods."""
    },
]