---
title: "Biases between consecutive primes"
source: "terrytao.wordpress.com"
url: "https://terrytao.wordpress.com/2016/03/14/biases-between-consecutive-primes/"
date: "2016-03-14"
categories: ["number theory", "primes", "expository"]
---
There is a very nice recent paper by Lemke Oliver and Soundararajan (complete with a popular science article about it by the consistently excellent Erica Klarreich for Quanta) about a surprising (but now satisfactorily explained) bias in the distribution of pairs of consecutive primes {p_n, p_{n+1}} when reduced to a small modulus {q}.

This phenomenon is superficially similar to the more well known Chebyshev bias concerning the reduction of a single prime {p_n} to a small modulus {q}, but is in fact a rather different (and much stronger) bias than the Chebyshev bias, and seems to arise from a completely different source. The Chebyshev bias asserts, roughly speaking, that a randomly selected prime {p} of a large magnitude {x} will typically (though not always) be slightly more likely to be a quadratic non-residue modulo {q} than a quadratic residue, but the bias is small (the difference in probabilities is only about {O(1/\sqrt{x})} for typical choices of {x}), and certainly consistent with known or conjectured positive results such as Dirichlet’s theorem or the generalised Riemann hypothesis. The reason for the Chebyshev bias can be traced back to the von Mangoldt explicit formula which relates the distribution of the von Mangoldt function {\Lambda} modulo {q} with the zeroes of the {L}-functions with period {q}. This formula predicts (assuming some standard conjectures like GRH) that the von Mangoldt function {\Lambda} is quite unbiased modulo {q}. The von Mangoldt function is mostly concentrated in the primes, but it also has a medium-sized contribution coming from squares of primes, which are of course all located in the quadratic residues modulo {q}. (Cubes and higher powers of primes also make a small contribution, but these are quite negligible asymptotically.) To balance everything out, the contribution of the primes must then exhibit a small preference towards quadratic non-residues, and this is the Chebyshev bias. (See this article of Rubinstein and Sarnak for a more technical discussion of the Chebyshev bias, and this survey of Granville and Martin for an accessible introduction. The story of the Chebyshev bias is also related to Skewes’ number, once considered the largest explicit constant to naturally appear in a mathematical argument.)

The paper of Lemke Oliver and Soundararajan considers instead the distribution of the pairs {(p_n \hbox{ mod } q, p_{n+1} \hbox{ mod } q)} for small {q} and for large consecutive primes {p_n, p_{n+1}}, say drawn at random from the primes comparable to some large {x}. For sake of discussion let us just take {q=3}. Then all primes {p_n} larger than {3} are either {1 \hbox{ mod } 3} or {2 \hbox{ mod } 3}; Chebyshev’s bias gives a very slight preference to the latter (of order {O(1/\sqrt{x})}, as discussed above), but apart from this, we expect the primes to be more or less equally distributed in both classes. For instance, assuming GRH, the probability that {p_n} lands in {1 \hbox{ mod } 3} would be {1/2 + O( x^{-1/2+o(1)} )}, and similarly for {2 \hbox{ mod } 3}.

In view of this, one would expect that up to errors of {O(x^{-1/2+o(1)})} or so, the pair {(p_n \hbox{ mod } 3, p_{n+1} \hbox{ mod } 3)} should be equally distributed amongst the four options {(1 \hbox{ mod } 3, 1 \hbox{ mod } 3)}, {(1 \hbox{ mod } 3, 2 \hbox{ mod } 3)}, {(2 \hbox{ mod } 3, 1 \hbox{ mod } 3)}, {(2 \hbox{ mod } 3, 2 \hbox{ mod } 3)}, thus for instance the probability that this pair is {(1 \hbox{ mod } 3, 1 \hbox{ mod } 3)} would naively be expected to be {1/4 + O(x^{-1/2+o(1)})}, and similarly for the other three tuples. These assertions are not yet proven (although some non-trivial upper and lower bounds for such probabilities can be obtained from recent work of Maynard).

However, Lemke Oliver and Soundararajan argue (backed by both plausible heuristic arguments (based ultimately on the Hardy-Littlewood prime tuples conjecture), as well as substantial numerical evidence) that there is a significant bias away from the tuples {(1 \hbox{ mod } 3, 1 \hbox{ mod } 3)} and {(2 \hbox{ mod } 3, 2 \hbox{ mod } 3)} – informally, adjacent primes don’t like being in the same residue class! For instance, they predict that the probability of attaining {(1 \hbox{ mod } 3, 1 \hbox{ mod } 3)} is in fact

\displaystyle  \frac{1}{4} - \frac{1}{8} \frac{\log\log x}{\log x} + O( \frac{1}{\log x} )

with similar predictions for the other three pairs (in fact they give a somewhat more precise prediction than this). The magnitude of this bias, being comparable to {\log\log x / \log x}, is significantly stronger than the Chebyshev bias of {O(1/\sqrt{x})}.

One consequence of this prediction is that the prime gaps {p_{n+1}-p_n} are slightly less likely to be divisible by {3} than naive random models of the primes would predict. Indeed, if the four options {(1 \hbox{ mod } 3, 1 \hbox{ mod } 3)}, {(1 \hbox{ mod } 3, 2 \hbox{ mod } 3)}, {(2 \hbox{ mod } 3, 1 \hbox{ mod } 3)}, {(2 \hbox{ mod } 3, 2 \hbox{ mod } 3)} all occurred with equal probability {1/4}, then {p_{n+1}-p_n} should equal {0 \hbox{ mod } 3} with probability {1/2}, and {1 \hbox{ mod } 3} and {2 \hbox{ mod } 3} with probability {1/4} each (as would be the case when taking the difference of two random numbers drawn from those integers not divisible by {3}); but the Lemke Oliver-Soundararajan bias predicts that the probability of {p_{n+1}-p_n} being divisible by three should be slightly lower, being approximately {1/2 - \frac{1}{4} \frac{\log\log x}{\log x}}.

Below the fold we will give a somewhat informal justification of (a simplified version of) this phenomenon, based on the Lemke Oliver-Soundararajan calculation using the prime tuples conjecture.


To explain the Lemke Oliver-Soundararajan bias, it is convenient to relax the requirement that the primes {p_{n+1}-p_n} are consecutive, and just look at small prime differences {p''-p'} between primes {p',p'' \sim x} that are somewhat close (in the sense that {p''-p'} is of size {O(\log x)}, which corresponds by the prime number theorem to the mean spacing between primes), but not necessarily consecutive. (This relaxation changes some of the constants in the Lemke Oliver-Soundarajaran analysis, basically by eliminating the need to invoke the inclusion-exclusion principle, but does not affect the qualitative nature of the bias.) The naive Cramér random model for the primes (discussed for instance in this post) suggests, as a first approximation, that for any {h = O(\log x)}, the number of prime differences {p''-p' = h} that are equal to {h} with {p',p'' \sim x} should be on the order of {\frac{x}{\log^2 x}}. Of course, this naive model is well known to require some adjustment: most obviously, prime differences {p''-p'} are almost always even, so the number of solutions to {p''-p'=h} is close to zero when {h} is odd. A little less obviously, values of {h}, such as {6}, which are multiples of three should (all other things being equal) be twice as likely to be prime differences as values of {h} (such as {2}) which are not; that is to say, one expects about twice as many “sexy primes” as “twin primes“. This is ultimately because the lower prime {p'} in a sexy prime pair {p''-p'=6} can lie in either of the two residue classes {1 \hbox{ mod } 3}, {2 \hbox{ mod } 3}, but the lower prime {p'} in a twin prime pair {p''-p'=2} can only lie in the residue class {2 \hbox{ mod } 3} (after excluding the first twin prime pair {(3,5)}).

The Lemke Oliver-Soundararajan bias pushes back against this phenomenon slightly; roughly speaking, it says that a typical number {h=O(\log x)} that is a multiple of {3} is only about {2 - c \frac{\log \log x}{\log x}} times as likely to be a prime difference as a typical number {h} that is a non-multiple of {3}, for some absolute constant {c>0} (which can be computed explicitly from their work, but I will not do so here).

This bias can be established assuming the Hardy-Littlewood prime tuples conjecture (with a sufficiently good error term). This conjecture asserts, roughly speaking, that the number of solutions to {p''-p' = h} with {p',p'' \sim x} and some given even {0 < h \ll \log x} is proportional to {f(h) \frac{x}{\log^2 x}}, where {f(h)} is the quantity

\displaystyle  f(h) := \prod_{p>2: p|h} \frac{p-1}{p-2}. \ \ \ \ \ (1)

The proportionality constant depends on the implicit constants in the relation {p',p'' \sim x}, and also involves the twin prime constant

\displaystyle  \Pi_2 := \prod_{p > 2} (1 - \frac{1}{(p-1)^2}) = 0.66016\dots;

it will not play an important role though in our analysis, so we omit it. The reason for the {\frac{p-1}{p-2}} factor can be explained from the following simple calculation: if {p} is an odd prime, and we select two numbers {p', p''} independently at random that are coprime to {p} (and equally likely to be in each of the {p-1} primitive residue classes mod {p}), then the probability that {p'-p'' = 0 \hbox{ mod } p} can be calculated to be {\frac{p-1}{p-2}} times as large as the probability that {p'-p'' = h \hbox{ mod } p} for any given {h} not divisible by {p}. For instance, if {p=3}, then {p'-p''} is twice as likely to equal {0 \hbox{ mod } 3} as it is equal {2 \hbox{ mod } 3}, as we have already observed before.

Naively, one would expect the quantity {f(h)} to be about twice as large when {h} is a multiple of three than when {h} is not a multiple of {3}, due to the {p=3} factor of {\frac{p-1}{p-2} = 2} in (1). However, it turns out that when restricting to the range {h = O(\log x)}, the average value of {f(h)} for {h} a multiple of {3} is only about {2 - c \frac{\log \log x}{\log x}} as large as the average value of {f(h)} for {h} not a multiple of {3}.

If we strip out the {p=3} term in (1), creating a new function

\displaystyle  f_3(h) := \prod_{p>3: p|h} \frac{p-1}{p-2} 

then the previous bias turns out to be a consequence of an asymptotic roughly of the form

\displaystyle  \sum_{h \leq H} f_3(h) = c_1 H - c_2 \log H + O(1) \ \ \ \ \ (2)

for some absolute constants {c_1,c_2 > 0} and all {H > 1}. (Actually, to avoid some artificial boundary issues one should replace the restriction {1_{h \leq H}} with a smoother weight such as {e^{-h/H}}, but we will ignore this technicality for sake of discussion.) Indeed, assuming the asymptotic (2), we have

\displaystyle  \sum_{h \leq \log x: h = 0 \hbox{ mod } 3} f_3(h) = \sum_{h \leq \frac{1}{3} \log x} f_3(3h) 

\displaystyle  = \sum_{h \leq \frac{1}{3} \log x} f_3(h) 

\displaystyle  = \frac{1}{3} c_1 \log x ( 1 - 3\frac{c_2}{c_1} \frac{\log\log x}{\log x} + O( \frac{1}{\log x} ) )

whereas

\displaystyle  \sum_{h \leq \log x} f_3(h) = c_1 \log x ( 1 - \frac{c_2}{c_1} \frac{\log\log x}{\log x} + O( \frac{1}{\log x} ) )

so we see that {f_3} has a slightly lower mean (by a factor of about {1 - 2 \frac{c_2}{c_1} \frac{\log\log x}{\log x}}) on the multiples of {3} than in general, which implies the corresponding claim about {f}. We thus see that the Lemke Oliver-Soundarajan bias can be traced to the lower order term {-c_2 \log H} in (2).

In the paper of Lemke Oliver and Soundararajan, the asymptotic (2) (smoothed out as discussed above) is obtained from standard complex methods, based on an analysis of the Dirichlet series

\displaystyle  \sum_h \frac{f_3(h)}{h^s} = \prod_{p>3} (1 + \frac{p-1}{p-2} \frac{1}{p^s}).

As it turns out, this Dirichlet series has poles at both {s=1} and {s=0} (it contains a factor of {\zeta(s) \zeta(1+s)}), contributing to the {c_1 H} and {-c_2 \log H} terms respectively. One can also establish (2) (with smoothing) using elementary number theory methods (as in this previous post); we sketch the argument as follows. We can factor {f_3} as a Dirichlet convolution

\displaystyle  f_3(h) = \sum_{d|h} g(d)

where {g(d)} vanishes unless {d} is the product of distinct primes greater than or equal to {3}, in which case

\displaystyle  g(d) = \prod_{p|d} \frac{1}{p-2}

(with the convention {g(1)=1}). Then we have

\displaystyle  \sum_{h \leq H} f_3(h) = \sum_{d \leq H} g(d) \sum_{m \leq H/d} 1.

Morally speaking, {\sum_{m \leq H/d} 1} behaves like {\frac{H}{d} - \frac{1}{2}}; we can use pseudorandomness heuristics to argue that the fluctuation around this main term give a lower order contribution (and one can argue this rigorously when using smoother weights like {e^{-h/H}}). The term {-1/2} can be interpreted as {\zeta(0)=1+1+\dots}, as per this previous post. Assuming this approximation, we obtain the approximation

\displaystyle  \sum_{h \leq H} f_3(h) \approx H \sum_{d \leq H} \frac{g(d)}{d} - \frac{1}{2} \sum_{d \leq H} g(d).

The sequence {g(d)} behaves somewhat like {1/d}. As such, one expects (and can calculate) {\sum_{d \leq H} \frac{g(d)}{d}} to have an asymptotic of the form {c_1 + O(1/H)}, while {\sum_{d \leq H} g(d)} has an asymptotic of the form {2 c_2 \log H + O(1)} for some explicit constants {c_1,c_2>0}, which gives (2).