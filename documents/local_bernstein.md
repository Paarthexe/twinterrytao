---
title: "Local Bernstein theory, and lower bounds for Lebesgue constants"
source: "terrytao.wordpress.com"
url: "https://terrytao.wordpress.com/2026/03/24/local-bernstein-theory-and-lower-bounds-for-lebesgue-constants/"
date: "2026-03-24"
categories: ["analysis", "approximation theory", "polynomials", "expository"]
---
I’ve just uploaded to the arXiv my paper “Local Bernstein theory, and lower bounds for Lebesgue constants“. This paper was initially motivated by a problem of Erdős} on Lagrange interpolation, but in the course of solving that problem, I ended up modifying some very classical arguments of Bernstein and his contemporaries (Boas, Duffin, Schaeffer, Riesz, etc.) to obtain “local” versions of these classical “Bernstein-type inequalities” that may be of independent interest.

Bernstein proved many estimates concerning the derivatives of polynomials, trigonometric polynomials, and entire functions of exponential type, but perhaps his most famous inequality in this direction is:


Lemma 1 (Bernstein’s inequality for trigonometric polynomials) Let {P: {\bf R} \rightarrow {\bf C}} be a trigonometric polynomial of degree at most {n}, with {|P(x)| \leq A} for all {x}. Then {|P'(x)| \leq n A} for all {x}.

Similar inequalities concerning {L^p} norms of derivatives of Littlewood-Paley components of functions are now ubiquitious in the modern theory of nonlinear dispersive PDE (where they are also called Bernstein estimates), but this will not be the focus of this current post.

A trigonometric polynomial {P} of degree {n} is of exponential type {n} in the sense that {P(z) = O(\exp(n|z|))} for complex {z}. Bernstein in fact proved a more general result:


Lemma 2 (Bernstein’s inequality for functions of exponential type) Let {f: {\bf C} \rightarrow {\bf C}} be an entire function of exponential type at most {\lambda}, with {|f(x)| \leq A} for all {x \in {\bf R}}. Then {|f'(x)| \leq \lambda A} for all {x \in {\bf R}}.

There are several proofs of this lemma – see for instance this survey of Queffélec and Zarouf. In the case that {f} is real-valued on {{\bf R}}, there is a nice proof by Duffin and Schaeffer, which we sketch as follows. Suppose we normalize {A=\lambda=1}, and adjust {f} by a suitable damping factor so that {f(z)} actually decays slower than {\exp(|z|)} as {z \rightarrow \infty}. Then, for any {0 < \alpha < 1} and {x_0 \in {\bf R}}, one can use Rouche’s theorem to show that the function {\cos(x-x_0) - \alpha f(x)} has the same number of zeroes as {\cos(x-x_0)} in a suitable large rectangle; but on the other hand one can use the intermediate value theorem to show that {\cos(x-x_0) - \alpha f(x)} has at least as many zeroes than {\cos(x-x_0)} in the same rectangle. Among other things, this prevents double zeroes from occuring, which turns out to give the desired claim {|f'(x)| \leq 1} after some routine calculations (in fact one obtains the stronger bound {|f(x)|^2 + |f'(x)|^2 \leq 1} for all real {x}).

The first main result of the paper is to obtain localized versions of Lemma 2 (as well as some related estimates). Roughly speaking, these estimates assert that if {f} is holomorphic on a wide thin rectangle passing through the real axis, is bounded by {A} on the intersection of the real axis with this rectangle, and is “locally of exponential type” in the sense that it is bounded by {O(\exp( \lambda |\mathrm{Im} z|))} on the upper and lower edges of this rectangle (and obeys some very mild growth conditions on the remaining sides of this rectangle), then {|f'(x)|} can be bounded by {\lambda A} plus small errors on the real line, with some additional estimates away from the real line also available. The proof proceeds by a modification of the Duffin–Schaeffer argument, together with the two-constant theorem of Nevanlinna (and some standard estimates of harmonic measures on rectangles) to deal with the effect of the localization. (As a side note, this latter argument was provided to me by ChatGPT, as I was not previously aware of the Nevanlinna two-constant theorem.)

Once one localizes this “Bernstein theory”, it becomes suitable for the analysis of (real-rooted, monic) polynomials {P} of a high degree {n}, which are not bounded globally on {{\bf R}} (and grow polynomially rather than exponentially at infinity), but which can exhibit “local exponential type” behavior on various intervals, particularly in regions where the logarithmic potential

\displaystyle  U_\mu(z) := \frac{1}{n} \log \frac{1}{|P(z)|} = \int \log \frac{1}{|z-x|}\ d\mu(x)

behaves like a smooth function (here {\mu = \frac{1}{n} \sum_{j=1}^k \delta_{x_j}} is the empirical measure of the roots {x_1,\dots,x_n} of {P}). A key example is the (monic) Chebyshev polynomials {2^{1-n} T_n(x)}, which locally behave like sinusoids on the interval {[-1,1]} (and are locally of exponential type above and below this interval):


This becomes relevant in the theory of Lagrange interpolation. Recall that if {x_1 < \dots < x_n} are real numbers and {Q} is a polynomial of degree less than {n} then one has the interpolation formula

\displaystyle  Q(z) = \sum_{j=1}^k Q(x_k) \ell_j(z)

where the Lagrange basis functions {\ell_j(z)} are defined by the formula
\displaystyle  \ell_k(z) := \prod_{i \neq k} \frac{z - x_i}{x_k - x_i}.

In terms of the monic polynomial {P(z) := \prod_{j=1}^n (z-x_j)}, we can write
\displaystyle  \ell_k(z) = \frac{P(z)}{(z-x_k) P'(x_k)}.

The stability and convergence properties of Lagrange interpolation are closely related to the Lebesgue function
\displaystyle  \Lambda(z) := \sum_{k=1}^n |\ell_k(z)|,

and for a given interval {I}, the quantity {\sup_{x \in I} \Lambda(x)} is known as the Lebesgue constant for that interval.
If one chooses the interpolation points {x_1,\dots,x_n} poorly, then the Lebesgue constant can be extremely large. However, if one selects these points to be the roots of the aforementioned monic Chebyshev polynomials, then it is known that {\sup_{x \in I} \Lambda(x) = \frac{2}{\pi} \log n - O(1)} for all fixed intervals {I} in {[-1,1]}. In the case {I = [-1,1]}, it was shown by Erdős} that this is the best possible value of the Lebesgue constant up to {O(1)} errors for interpolation on {[-1,1]}, thus

\displaystyle  \sup_{x \in [-1,1]} \Lambda(x) \geq \frac{2}{\pi} \log n - O(1)

whenever {-1 \leq x_1 < \dots < x_n \leq 1} (a more precise bound was later shown by Vertesi). Erdős and Turán then asked if the same lower bound
\displaystyle  \sup_{x \in I} \Lambda(x) \geq \frac{2}{\pi} \log n - O(1) \ \ \ \ \ (1)

held for more general intervals {I}. This is shown in our paper; a variant integral bound
\displaystyle  \int_I \Lambda(x)\ dx \geq \frac{4}{\pi^2} |I| \log n - o(\log n) \ \ \ \ \ (2)

is also established, answering a separate question of Erdős. These lower bounds had previously obtained up to constants by Erdős and Szabados}; the main issue was to obtain the sharp constant in the main term.
In terms of the monic polynomial {P}, these two estimates can be written as

\displaystyle  \sup_{x \in I} \sum_{k=1}^n \frac{|P(x)|}{|x-x_k||P'(x_k)|} \geq \frac{2}{\pi} \log n - O(1)

and
\displaystyle  \int_I \sum_{k=1}^n \frac{|P(x)|}{|x-x_k||P'(x_k)|}\ dx \geq \frac{4}{\pi^2} |I| \log n - o(\log n).

Using the intuition that {P} should behave locally like a trigonometric polynomial, and performing some renormalizations, one can extract the following toy problem to work with first:

Problem 3 Let {P: {\bf R} \rightarrow {\bf R}} be a trigonometric polynomial of degree {n} with {2n} roots {x_1 < \dots < x_{2n}} in {[0, 2\pi)}.
(i) Show that
\displaystyle  \sup_{x \in [0,2\pi)} \sum_{k=1}^{2n} \frac{|P(x)|}{|P'(x_k)|} \geq 2. \ \ \ \ \ (3)

(ii) Show that
\displaystyle  \int_0^{2\pi} \sum_{k=1}^{2n} \frac{|P(x)|}{|P'(x_k)|}\ dx \geq 8. \ \ \ \ \ (4)


It is easy to check that the lower bounds of {2} and {8} are sharp by considering the case when {P} is a sinusoid {P(x) = A \sin(n(x-x_0))}.

The bound (3) is immediate from Bernstein’s inequality (Lemma 1). By applying a local version of this inequality, I was able to get a weak version of the claim (1) in which {O(1)} was replaced with {o(\log n)}; see this early version of the paper, which was developed through conversations with Nat Sothanaphan and Aron Bhalla. By combining this argument with ideas from the older work of Erdős}, I was able to establish (1).

The bound (2) took me longer to establish, and involved a non-trivial amount of playing around with AI tools, the story of which I would like to share here. I had discovered the toy problem (4), but initially was not able to establish this inequality; AlphaEvolve seemed to confirm it numerically (with sinusoids appearing to be the extremizer), but did not offer direct clues on how to prove this rigorously. At some point I realized that the left-hand side factorized into the expressions {\int_0^{2\pi} |P(x)|\ dx} and {\sum_{k=1}^{2n} \frac{1}{|P'(x_k)|}}, and tried to bound these expressions separately. Perturbing around a sinusoid {A \sin(n(x-x_0))}, I was able to show that the {L^1} norm {\int_0^{2\pi} |P(x)|\ dx} was a local minimum as long as one only perturbed by lower order Fourier modes, keeping the frequency {n} coefficients unchanged. Guessing that this local minimum was actually a global minimum, this led me to conjecture the general lower bound

\displaystyle  \int_0^{2\pi} |P(x)|\ dx \geq 4 |a_n+ib_n|

whenever {P} was a degree {n} trigonometric polynomial with highest frequency components {a_n \cos(nx) + b_n \sin(nx)}. AlphaEvolve numerically confirmed this inequality to be likely to be true also. I still did not see how to prove this inequality, but I decided to try my luck giving it to ChatGPT Pro, which recognized it as an {L^1} approximation problem and gave me a duality-based proof (based ultimately on the Fourier expansion of the square wave). With some further discussion, I was able to adapt this proof to functions of global exponential type (replacing the Fourier manipulations with contour shifting arguments, in the spirit of the Paley-Wiener theorem), which roughly speaking gave me half of what I needed to establish (2). However, I still needed the matching lower bound
\displaystyle  \sum_{k=1}^{2n} \frac{1}{|P'(x_k)|} \geq \frac{2}{|a_n+ib_n|}

on the other factor in the toy problem. Again, AlphaEvolve could numerically confirm that this inequality was likely to be true, but now the quantity I was trying to control did not look convex or linear in {P}, and so the previous duality method did not seem to apply. At this point I switched to pen and paper; eventually I realized that the expression almost looked like a sum of residues, and eventually after playing around with contour integrals of {\frac{e^{inz}}{P(z)}} using the residue theorem I was able to establish (4), and then with a bit more (human) effort I could move from the toy problem back to the original problem to obtain (2). Quite possibly AI tools would also have been able to assist with these steps, but they were not necessary here; their main value for me was in quickly confirming that the approach I had in mind was numerically plausible, and in recognizing the right technique to solve one part of the toy problem I had isolated. (I also used AI tools for several other secondary tasks, such as literature review, proofreading, and generating pictures, but these applications of AI have matured to the point where using them for this purpose is almost mundane.)