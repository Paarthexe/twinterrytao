---
title: "Some remarks on the lonely runner conjecture"
source: "terrytao.wordpress.com"
url: "https://terrytao.wordpress.com/2017/01/10/some-remarks-on-the-lonely-runner-conjecture/"
date: "2017-01-10"
categories: ["geometry", "discrete geometry", "diophantine approximation", "expository"]
---
The lonely runner conjecture is the following open problem:

Conjecture 1 Suppose one has {n \geq 1} runners on the unit circle {{\bf R}/{\bf Z}}, all starting at the origin and moving at different speeds. Then for each runner, there is at least one time {t} for which that runner is “lonely” in the sense that it is separated by a distance at least {1/n} from all other runners.

One can normalise the speed of the lonely runner to be zero, at which point the conjecture can be reformulated (after replacing {n} by {n+1}) as follows:

Conjecture 2 Let {v_1,\dots,v_n} be non-zero real numbers for some {n \geq 1}. Then there exists a real number {t} such that the numbers {tv_1,\dots,tv_n} are all a distance at least {\frac{1}{n+1}} from the integers, thus {\|tv_1\|_{{\bf R}/{\bf Z}},\dots,\|tv_n\|_{{\bf R}/{\bf Z}} \geq \frac{1}{n+1}} where {\|x\|_{{\bf R}/{\bf Z}}} denotes the distance of {x} to the nearest integer.

This conjecture has been proven for {n \leq 7}, but remains open for larger {n}. The bound {\frac{1}{n+1}} is optimal, as can be seen by looking at the case {v_i=i} and applying the Dirichlet approximation theorem. Note that for each non-zero {v}, the set {\{ t \in {\bf R}: \|vt\|_{{\bf R}/{\bf Z}} \leq r \}} has (Banach) density {2r} for any {0 < r < 1/2}, and from this and the union bound we can easily find {t \in {\bf R}} for which

\displaystyle \|tv_1\|_{{\bf R}/{\bf Z}},\dots,\|tv_n\|_{{\bf R}/{\bf Z}} \geq \frac{1}{2n}-\varepsilon

for any {\varepsilon>0}, but it has proven to be quite challenging to remove the factor of {2} to increase {\frac{1}{2n}} to {\frac{1}{n+1}}. (As far as I know, even improving {\frac{1}{2n}} to {\frac{1+c}{2n}} for some absolute constant {c>0} and sufficiently large {n} remains open.)

The speeds {v_1,\dots,v_n} in the above conjecture are arbitrary non-zero reals, but it has been known for some time that one can reduce without loss of generality to the case when the {v_1,\dots,v_n} are rationals, or equivalently (by scaling) to the case where they are integers; see e.g. Section 4 of this paper of Bohman, Holzman, and Kleitman.

In this post I would like to remark on a slight refinement of this reduction, in which the speeds {v_1,\dots,v_n} are integers of bounded size, where the bound depends on {n}. More precisely:

Proposition 3 In order to prove the lonely runner conjecture, it suffices to do so under the additional assumption that the {v_1,\dots,v_n} are integers of size at most {n^{Cn^2}}, where {C} is an (explicitly computable) absolute constant. (More precisely: if this restricted version of the lonely runner conjecture is true for all {n \leq n_0}, then the original version of the conjecture is also true for all {n \leq n_0}.)

In principle, this proposition allows one to verify the lonely runner conjecture for a given {n} in finite time; however the number of cases to check with this proposition grows faster than exponentially in {n}, and so this is unfortunately not a feasible approach to verifying the lonely runner conjecture for more values of {n} than currently known.

One of the key tools needed to prove this proposition is the following additive combinatorics result. Recall that a generalised arithmetic progression (or {GAP}) in the reals {{\bf R}} is a set of the form

\displaystyle  P = \{ n_1 v_1 + \dots + n_d v_d: n_1,\dots,n_d \in {\bf Z}; |n_1| \leq N_1, \dots, |n_d| \leq N_d \}

for some {v_1,\dots,v_d \in {\bf R}} and {N_1,\dots,N_d > 0}; the quantity {d} is called the rank of the progression. If {t>0}, the progression {P} is said to be {t}-proper if the sums {n_1 v_1 + \dots + n_d v_d} with {|n_i| \leq t N_i} for {i=1,\dots,d} are all distinct. We have

Lemma 4 (Progressions lie inside proper progressions) Let {P} be a GAP of rank {d} in the reals, and let {t \geq 1}. Then {P} is contained in a {t}-proper GAP {Q} of rank at most {d}, with

\displaystyle |Q| \leq (2t)^d d^{6d^2} \prod_{i=1}^d (2N_i+1).

Proof: See Theorem 2.1 of this paper of Bilu. (Very similar results can also be found in Theorem 3.40 of my book with Van Vu, or Theorem 1.10 of this paper of mine with Van Vu.) \Box

Now let {n \geq 1}, and assume inductively that the lonely runner conjecture has been proven for all smaller values of {n}, as well as for the current value of {n} in the case that {v_1,\dots,v_n} are integers of size at most {n^{Cn^2}} for some sufficiently large {C}. We will show that the lonely runner conjecture holds in general for this choice of {n}.

let {v_1,\dots,v_n} be non-zero real numbers. Let {C_0} be a large absolute constant to be chosen later. From the above lemma applied to the GAP {\{ n_1 v_1 + \dots + n_d v_d: n_1,\dots,n_d \in \{-1,0,1\}\}}, one can find a {n^{C_0n}}-proper GAP {Q} of rank at most {n} containing {\{v_1,\dots,v_n\}} such that

\displaystyle  |Q| \leq (6n^{C_0 n})^n n^{6n^2};

in particular {|Q| \leq n^{Cn^2}} if {C} is large enough depending on {C_0}.

We write

\displaystyle  Q = \{ n_1 w_1 + \dots + n_d w_d: n_1,\dots,n_d \in {\bf Z}; |n_1| \leq N_1,\dots,|n_d| \leq N_d \}

for some {d \leq n}, {w_1,\dots,w_d}, and {N_1,\dots,N_d \geq 0}. We thus have {v_i = \phi(a_i)} for {i=1,\dots,n}, where {\phi: {\bf R}^d \rightarrow {\bf R}} is the linear map {\phi(n_1,\dots,n_d) := n_1 w_1 + \dots + n_d w_d} and {a_1,\dots,a_n \in {\bf Z}^d} are non-zero and lie in the box {\{ (n_1,\dots,n_d) \in {\bf R}^d: |n_1| \leq N_1,\dots,|n_d| \leq N_d \}}.

We now need an elementary lemma that allows us to create a “collision” between two of the {a_1,\dots,a_n} via a linear projection, without making any of the {a_i} collide with the origin:

Lemma 5 Let {a_1,\dots,a_n \in {\bf R}^d} be non-zero vectors that are not all collinear with the origin. Then, after replacing one or more of the {a_i} with their negatives {-a_i} if necessary, there exists a pair {a_i,a_j} such that {a_i-a_j \neq 0}, and such that none of the {a_1,\dots,a_n} is a scalar multiple of {a_i-a_j}.

Proof: We may assume that {d \geq 2}, since the {d \leq 1} case is vacuous. Applying a generic linear projection to {{\bf R}^2} (which does not affect collinearity, or the property that a given {a_k} is a scalar multiple of {a_i-a_j}), we may then reduce to the case {d=2}.

By a rotation and relabeling, we may assume that {a_1} lies on the negative {x}-axis; by flipping signs as necessary we may then assume that all of the {a_2,\dots,a_n} lie in the closed right half-plane. As the {a_i} are not all collinear with the origin, one of the {a_i} lies off of the {x}-axis, by relabeling, we may assume that {a_2} lies off of the {x} axis and makes a minimal angle with the {x}-axis. Then the angle of {a_2-a_1} with the {x}-axis is non-zero but smaller than any non-zero angle that any of the {a_i} make with this axis, and so none of the {a_i} are a scalar multiple of {a_2-a_1}, and the claim follows. \Box

We now return to the proof of the proposition. If the {a_1,\dots,a_n} are all collinear with the origin, then {\phi(a_1),\dots,\phi(a_n)} lie in a one-dimensional arithmetic progression {\{ mv: |m| \leq |Q| \}}, and then by rescaling we may take the {v_1,\dots,v_n} to be integers of magnitude at most {|Q| \leq n^{Cn}}, at which point we are done by hypothesis. Thus, we may assume that the {a_1,\dots,a_n} are not all collinear with the origin, and so by the above lemma and relabeling we may assume that {a_n-a_1} is non-zero, and that none of the {a_i} are scalar multiples of {a_n-a_1}.

We write

\displaystyle  a_n-a_1 = (c_1,\dots,c_d) \ \ \ \ \ (1)

with {|c_i| \leq 2 N_i} for {i=1,\dots,d}; by relabeling we may assume without loss of generality that {c_d} is non-zero, and furthermore that

\displaystyle  \frac{|c_i|}{N_i} \leq \frac{|c_d|}{N_d}

for {i=1,\dots,d}. We can also factor

\displaystyle  (c_1,\dots,c_d) = q (c'_1,\dots,c'_d) \ \ \ \ \ (2)

where {q} is a natural number and {c'_1,\dots,c'_d} have no common factor.

We now define a variant {\tilde \phi: {\bf R}^d \rightarrow {\bf R}} of {\phi: {\bf R}^d \rightarrow {\bf R}} by the map

\displaystyle  \tilde \phi(n_1,\dots,n_d) := n_1 \tilde w_1 + \dots + n_{d-1} \tilde w_{d-1} - \frac{n_d}{c_d} (c_1 \tilde w_1 + \dots + c_{d-1} \tilde w_{d-1}),

where the {\tilde w_1,\dots,\tilde w_{d-1}} are real numbers that are linearly independent over {{\bf Q}}, whose precise value will not be of importance in our argument. This is a linear map with the property that {\tilde \phi(a_n-a_1)=0}, so that {\tilde \phi(a_1),\dots,\tilde \phi(a_n)} consists of at most {n-1} distinct real numbers, which are non-zero since none of the {a_i} are scalar multiples of {a_n-a_1}, and the {\tilde w_i} are linearly independent over {{\bf Q}}. As we are assuming inductively that the lonely runner conjecture holds for {n-1}, we conclude (after deleting duplicates) that there exists at least one real number {\tilde t} such that

\displaystyle  \| \tilde t \tilde \phi(a_1) \|_{{\bf R}/{\bf Z}}, \dots, \| \tilde t \tilde \phi(a_n) \|_{{\bf R}/{\bf Z}} \geq \frac{1}{n}.

We would like to “approximate” {\phi} by {\tilde \phi} to then conclude that there is at least one real number {t} such that

\displaystyle  \| t \phi(a_1) \|_{{\bf R}/{\bf Z}}, \dots, \| t \phi(a_n) \|_{{\bf R}/{\bf Z}} \geq \frac{1}{n+1}.

It turns out that we can do this by a Fourier-analytic argument taking advantage of the {n^{C_0 n}}-proper nature of {Q}. Firstly, we see from the Dirichlet approximation theorem that one has

\displaystyle  \| \tilde t \tilde \phi(a_1) \|_{{\bf R}/{\bf Z}}, \dots, \| \tilde t \tilde \phi(a_n) \|_{{\bf R}/{\bf Z}} \leq \frac{1}{10 n^2}

for a set {\tilde t} of reals of (Banach) density {\gg n^{-O(n)}}. Thus, by the triangle inequality, we have

\displaystyle  \| \tilde t \tilde \phi(a_1) \|_{{\bf R}/{\bf Z}}, \dots, \| \tilde t \tilde \phi(a_n) \|_{{\bf R}/{\bf Z}} \geq \frac{1}{n} - \frac{1}{10n^2}

for a set {\tilde t} of reals of density {\gg n^{-O(n)}}.

Applying a smooth Fourier multiplier of Littlewood-Paley type, one can find a trigonometric polynomial

\displaystyle  \eta(x) = \sum_{m: |m| \leq n^{C_0 n/10}} b_m e^{2\pi i mx} 

which takes values in {[0,1]}, is {\gg 1} for {\|x\|_{{\bf R}/{\bf Z}} \geq \frac{1}{n} - \frac{1}{10n^2}}, and is no larger than {O( n^{-100 C_0n} )} for {\|x\|_{{\bf R}/{\bf Z}} \leq \frac{1}{n+1}}. We then have

\displaystyle  \mathop{\bf E}_t \prod_{j=1}^n \eta( t \tilde \phi(a_j) ) \gg n^{-O(n)} 

where {\mathop{\bf E}_t f(t)} denotes the mean value of a quasiperiodic function {f} on the reals {{\bf R}}. We expand the left-hand side out as

\displaystyle  \sum_{m_1,\dots,m_n: m_1 \tilde \phi(a_1) + \dots + m_n \tilde \phi(a_n) = 0} b_{m_1} \dots b_{m_n}.

From the genericity of {\tilde w_1,\dots,\tilde w_n}, we see that the constraint

\displaystyle  m_1 \tilde \phi(a_1) + \dots + m_n \tilde \phi(a_n) = 0 

occurs if and only if {m_1 a_1 + \dots + m_n a_n} is a scalar multiple of {a_n-a_1}, or equivalently (by (1), (2)) an integer multiple of {(c'_1,\dots,c'_d)}. Thus

\displaystyle  \sum_{m_1,\dots,m_n: m_1 a_1 + \dots + m_n a_n \in {\bf Z} (c'_1,\dots,c'_d)} b_{m_1} \dots b_{m_n} \gg n^{-O(n)}. \ \ \ \ \ (3)

Next, we consider the average

\displaystyle  \mathop{\bf E}_t \varphi( t \xi ) \prod_{j=1}^n \eta( t v_j ) \ \ \ \ \ (4)

where

\displaystyle  \xi := c'_1 w_1 + \dots + c'_d w_d. \ \ \ \ \ (5)

and {\varphi} is the Dirichlet series

\displaystyle  \varphi(x) := \sum_{m: |m| \leq n^{C_0 n/2}} e^{2\pi i mx}.

By Fourier expansion and writing {v_j = \phi(a_j)}, we may write (4) as

\displaystyle  \sum_{m,m_1,\dots,m_n: |m| \leq n^{C_0n/2}; m_1 \phi(a_1) + \dots + m_n \phi(a_n) = m \xi} b_{m_1} \dots b_{m_n}. 

The support of the {b_{m_i}} implies that {|m_i| \leq n^{C_0n/10}}. Because of the {n^{C_0 n}}-properness of {Q}, we see (for {n} large enough) that the equation

\displaystyle  m_1 \phi(a_1) + \dots + m_n \phi(a_n) = m \xi \ \ \ \ \ (6)

implies that

\displaystyle  m_1 a_1 + \dots + m_n a_n \in {\bf Z} (c'_1,\dots,c'_d) \ \ \ \ \ (7)

and conversely that (7) implies that (6) holds for some {m} with {|m| \leq n^{C_0 n/2}}. From (3) we thus have

\displaystyle  \mathop{\bf E}_t \varphi( t \xi ) \prod_{j=1}^n \eta( t v_j ) \gg n^{-O(1)}. 

In particular, there exists a {t} such that

\displaystyle  \varphi( t \xi ) \prod_{j=1}^n \eta( t v_j ) \gg n^{-O(1)}. 

Since {\varphi} is bounded in magnitude by {n^{C_0n/2}}, and {\eta} is bounded by {1}, we thus have

\displaystyle  \eta(t v_j) \gg n^{-C_0 n/2 - O(1)} 

for each {1 \leq j \leq n}, which by the size properties of {\eta} implies that {\|tv_j\|_{{\bf R}/{\bf Z}} \geq \frac{1}{n+1}} for all {1 \leq j \leq n}, giving the lonely runner conjecture for {n}.