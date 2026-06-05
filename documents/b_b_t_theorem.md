---
title: "Notes on the B+B+t theorem"
source: "terrytao.wordpress.com"
url: "https://terrytao.wordpress.com/2024/04/24/notes-on-the-b-b-t-theorem/"
date: "2024-04-24"
categories: ["combinatorics", "additive combinatorics", "ergodic theory", "expository"]
---
A recent paper of Kra, Moreira, Richter, and Robertson established the following theorem, resolving a question of Erdös. Given a discrete amenable group {G = (G,+)}, and a subset {A} of {G}, we define the Banach density of {A} to be the quantity

\displaystyle  \sup_\Phi \limsup_{N \rightarrow \infty} |A \cap \Phi_N|/|\Phi_N|,

where the supremum is over all Følner sequences {\Phi = (\Phi_N)_{N=1}^\infty} of {G}. Given a set {B} in {G}, we define the restricted sumset {B \oplus B} to be the set of all pairs {b_1+b_2} where {b_1, b_2} are distinct elements of {B}.

Theorem 1 Let {G} be a countably infinite abelian group with the index {[G:2G]} finite. Let {A} be a positive Banach density subset of {G}. Then there exists an infinite set {B \subset A} and {t \in G} such that {B \oplus B + t \subset A}.

Strictly speaking, the main result of Kra et al. only claims this theorem for the case of the integers {G={\bf Z}}, but as noted in the recent preprint of Charamaras and Mountakis, the argument in fact applies for all countable abelian {G} in which the subgroup {2G := \{ 2x: x \in G \}} has finite index. This condition is in fact necessary (as observed by forthcoming work of Ethan Acklesberg): if {2G} has infinite index, then one can find a subgroup {H_j} of {G} of index {2^j} for any {j \geq 1} that contains {2G} (or equivalently, {G/H_j} is {2}-torsion). If one lets {y_1,y_2,\dots} be an enumeration of {G}, and one can then check that the set

\displaystyle  A := G \backslash \bigcup_{j=1}^\infty (H_{j+1} + y_j) \backslash \{y_1,\dots,y_j\}

has positive Banach density, but does not contain any set of the form {B \oplus B + t} for any {t} (indeed, from the pigeonhole principle and the {2}-torsion nature of {G/H_{j+1}} one can show that {B \oplus B + y_j} must intersect {H_{j+1} + y_j \backslash \{y_1,\dots,y_j\}} whenever {B} has cardinality larger than {j 2^{j+1}}). It is also necessary to work with restricted sums {B \oplus B} rather than full sums {B+B}: a counterexample to the latter is provided for instance by the example with {G = {\bf Z}} and {A := \bigcup_{j=1}^\infty [10^j, 1.1 \times 10^j]}. Finally, the presence of the shift {t} is also necessary, as can be seen by considering the example of {A} being the odd numbers in {G ={\bf Z}}, though in the case {G=2G} one can of course delete the shift {t} at the cost of giving up the containment {B \subset A}.
Theorem 1 resembles other theorems in density Ramsey theory, such as Szemerédi’s theorem, but with the notable difference that the pattern located in the dense set {A} is infinite rather than merely arbitrarily large but finite. As such, it does not seem that this theorem can be proven by purely finitary means. However, one can view this result as the conjunction of an infinite number of statements, each of which is a finitary density Ramsey theory statement. To see this, we need some more notation. Observe from Tychonoff’s theorem that the collection {2^G := \{ B: B \subset G \}} is a compact topological space (with the topology of pointwise convergence) (it is also metrizable since {G} is countable). Subsets {{\mathcal F}} of {2^G} can be thought of as properties of subsets of {G}; for instance, the property a subset {B} of {G} of being finite is of this form, as is the complementary property of being infinite. A property of subsets of {G} can then be said to be closed or open if it corresponds to a closed or open subset of {2^G}. Thus, a property is closed and only if if it is closed under pointwise limits, and a property is open if, whenever a set {B} has this property, then any other set {B'} that shares a sufficiently large (but finite) initial segment with {B} will also have this property. Since {2^G} is compact and Hausdorff, a property is closed if and only if it is compact.

The properties of being finite or infinite are neither closed nor open. Define a smallness property to be a closed (or compact) property of subsets of {G} that is only satisfied by finite sets; the complement to this is a largeness property, which is an open property of subsets of {G} that is satisfied by all infinite sets. (One could also choose to impose other axioms on these properties, for instance requiring a largeness property to be an upper set, but we will not do so here.) Examples of largeness properties for a subset {B} of {G} include:

{B} has at least {10} elements.
{B} is non-empty and has at least {b_1} elements, where {b_1} is the smallest element of {B}.
{B} is non-empty and has at least {b_{b_1}} elements, where {b_n} is the {n^{\mathrm{th}}} element of {B}.
{T} halts when given {B} as input, where {T} is a given Turing machine that halts whenever given an infinite set as input. (Note that this encompasses the preceding three examples as special cases, by selecting {T} appropriately.)
We will call a set obeying a largeness property {{\mathcal P}} an {{\mathcal P}}-large set.
Theorem 1 is then equivalent to the following “almost finitary” version (cf. this previous discussion of almost finitary versions of the infinite pigeonhole principle):


Theorem 2 (Almost finitary form of main theorem) Let {G} be a countably infinite abelian group with {[G:2G]} finite. Let {\Phi_n} be a Følner sequence in {G}, let {\delta>0}, and let {{\mathcal P}_t} be a largeness property for each {t \in G}. Then there exists {N} such that if {A \subset G} is such that {|A \cap \Phi_n| / |\Phi_n| \geq \delta} for all {n \leq N}, then there exists a shift {t \in G} and {A} contains a {{\mathcal P}_t}-large set {B} such that {B \oplus B + t \subset A}.

Proof of Theorem 2 assuming Theorem 1. Let {G, \Phi_n}, {\delta}, {{\mathcal P}_t} be as in Theorem 2. Suppose for contradiction that Theorem 2 failed, then for each {N} we can find {A_N} with {|A_N \cap \Phi_n| / |\Phi_n| \geq \delta} for all {n \leq N}, such that there is no {t} and {{\mathcal P}_t}-large {B} such that {B, B \oplus B + t \subset A_N}. By compactness, a subsequence of the {A_N} converges pointwise to a set {A}, which then has Banach density at least {\delta}. By Theorem 1, there is an infinite set {B} and a {t} such that {B, B \oplus B + t \subset A}. By openness, we conclude that there exists a finite {{\mathcal P}_t}-large set {B'} contained in {B}, thus {B', B' \oplus B' + t \subset A}. This implies that {B', B' \oplus B' + t \subset A_N} for infinitely many {N}, a contradiction.

Proof of Theorem 1 assuming Theorem 2. Let {G, A} be as in Theorem 1. If the claim failed, then for each {t}, the property {{\mathcal P}_t} of being a set {B} for which {B, B \oplus B + t \subset A} would be a smallness property. By Theorem 2, we see that there is a {t} and a {B} obeying the complement of this property such that {B, B \oplus B + t \subset A}, a contradiction.


Remark 3 Define a relation {R} between {2^G} and {2^G \times G} by declaring {A\ R\ (B,t)} if {B \subset A} and {B \oplus B + t \subset A}. The key observation that makes the above equivalences work is that this relation is continuous in the sense that if {U} is an open subset of {2^G \times G}, then the inverse image
\displaystyle R^{-1} U := \{ A \in 2^G: A\ R\ (B,t) \hbox{ for some } (B,t) \in U \}

is also open. Indeed, if {A\ R\ (B,t)} for some {(B,t) \in U}, then {B} contains a finite set {B'} such that {(B',t) \in U}, and then any {A'} that contains both {B'} and {B' \oplus B' + t} lies in {R^{-1} U}.

For each specific largeness property, such as the examples listed previously, Theorem 2 can be viewed as a finitary assertion (at least if the property is “computable” in some sense), but if one quantifies over all largeness properties, then the theorem becomes infinitary. In the spirit of the Paris-Harrington theorem, I would in fact expect some cases of Theorem 2 to undecidable statements of Peano arithmetic, although I do not have a rigorous proof of this assertion.

Despite the complicated finitary interpretation of this theorem, I was still interested in trying to write the proof of Theorem 1 in some sort of “pseudo-finitary” manner, in which one can see analogies with finitary arguments in additive combinatorics. The proof of Theorem 1 that I give below the fold is my attempt to achieve this, although to avoid a complete explosion of “epsilon management” I will still use at one juncture an ergodic theory reduction from the original paper of Kra et al. that relies on such infinitary tools as the ergodic decomposition, the ergodic theory, and the spectral theorem. Also some of the steps will be a little sketchy, and assume some familiarity with additive combinatorics tools (such as the arithmetic regularity lemma).



— 1. Proof of theorem —

The proof of Kra et al. proceeds by establishing the following related statement. Define a (length three) combinatorial Erdös progression to be a triple {(A,X_1,X_2)} of subsets of {G} such that there exists a sequence {n_j \rightarrow \infty} in {G} such that {A - n_j} converges pointwise to {X_1} and {X_1-n_j} converges pointwise to {X_2}. (By {n_j \rightarrow \infty}, we mean with respect to the cocompact filter; that is, that for any finite (or, equivalently, compact) subset {K} of {G}, {n_j \not \in K} for all sufficiently large {j}.)


Theorem 4 (Combinatorial Erdös progression) Let {G} be a countably infinite abelian group with {[G:2G]} finite. Let {A} be a positive Banach density subset of {G}. Then there exists a combinatorial Erdös progression {(A,X_1,X_2)} with {0 \in X_1} and {X_2} non-empty.

Let us see how Theorem 4 implies Theorem 1. Let {G, A, X_1, X_2, n_j} be as in Theorem 4. By hypothesis, {X_2} contains an element {t} of {G}, thus {0 \in X_1} and {t \in X_2}. Setting {b_1} to be a sufficiently large element of the sequence {n_1, n_2, \dots}, we conclude that {b_1 \in A} and {b_1 + t \in X_1}. Setting {b_2} to be an even larger element of this sequence, we then have {b_2, b_2+b_1+t \in A} and {b_2 +t \in X_1}. Setting {b_3} to be an even larger element, we have {b_3, b_3+b_1+t, b_3+b_2+t \in A} and {b_3 + t \in X_1}. Continuing in this fashion we obtain the desired infinite set {B}.

It remains to establish Theorem 4. The proof of Kra et al. converts this to a topological dynamics/ergodic theory problem. Define a topological measure-preserving {G}-system {(X,T,\mu)} to be a compact space {X} equipped with a Borel probability measure {\mu} as well as a measure-preserving homeomorphism {T: X \rightarrow X}. A point {a} in {X} is said to be generic for {\mu} with respect to a Følner sequence {\Phi} if one has

\displaystyle  \int_X f\ d\mu = \lim_{N \rightarrow \infty} {\bf E}_{n \in \Phi_N} f(T^n a)

for all continuous {f: X \rightarrow {\bf C}}. Define an (length three) dynamical Erdös progression to be a tuple {(a,x_1,x_2)} in {X} with the property that there exists a sequence {n_j \rightarrow \infty} such that {T^{n_j} a \rightarrow x_1} and {T^{n_j} x_1 \rightarrow x_2}.
Theorem 4 then follows from


Theorem 5 (Dynamical Erdös progression) Let {G} be a countably infinite abelian group with {[G:2G]} finite. Let {(X,T,\mu)} be a topological measure-preserving {G}-system, let {a} be a {\Phi}-generic point of {\mu} for some Følner sequence {\Phi}, and let {E} be a positive measure open subset of {X}. Then there exists a dynamical Erdös progression {(a,x_1,x_2)} with {x_1 \in E} and {x_2 \in \bigcup_{t \in G} T^t E}.

Indeed, we can take {X} to be {2^G}, {a} to be {A}, {T} to be the shift {T^n B := B-n}, {E := \{ B \in 2^G: 0 \in B \}}, and {\mu} to be a weak limit of the {\mathop{\bf E}_{n \in \Phi_N} \delta_{A-n}} for a Følner sequence {\Phi_N} with {\lim_{N \rightarrow \infty} |A \cap \Phi_N| / |\Phi_N| > 0}, at which point Theorem 4 follows from Theorem 5 after chasing definitions. (It is also possible to establish the reverse implication, but we will not need to do so here.)

A remarkable fact about this theorem is that the point {a} need not be in the support of {\mu}! (In a related vein, the elements {\Phi_j} of the Følner sequence are not required to contain the origin.)

Using a certain amount of ergodic theory and spectral theory, Kra et al. were able to reduce this theorem to a special case:


Theorem 6 (Reduction) To prove Theorem 5, it suffices to do so under the additional hypotheses that {X} is ergodic, and there is a continuous factor map to the Kronecker factor. (In particular, the eigenfunctions of {X} can be taken to be continuous.)

We refer the reader to the paper of Kra et al. for the details of this reduction. Now we specialize for simplicity to the case where {G = {\bf F}_p^\omega = \bigcup_N {\bf F}_p^N} is a countable vector space over a finite field of size equal to an odd prime {p}, so in particular {2G=G}; we also specialize to Følner sequences of the form {\Phi_j = x_j + {\bf F}_p^{N_j}} for some {x_j \in G} and {N_j \geq 1}. In this case we can prove a stronger statement:


Theorem 7 (Odd characteristic case) Let {G = {\bf F}_p^\omega} for an odd prime {p}. Let {(X,T,\mu)} be a topological measure-preserving {G}-system with a continuous factor map to the Kronecker factor, and let {E_1, E_2} be open subsets of {X} with {\mu(E_1) + \mu(E_2) > 1}. Then if {a} is a {\Phi}-generic point of {\mu} for some Følner sequence {\Phi_j = y_j + {\bf F}_p^{n_j}}, there exists an Erdös progression {(a,x_1,x_2)} with {x_1 \in E_1} and {x_2 \in E_2}.

Indeed, in the setting of Theorem 5 with the ergodicity hypothesis, the set {\bigcup_{t \in G} T^t E} has full measure, so the hypothesis {\mu(E_1)+\mu(E_2) > 1} of Theorem 7 will be verified in this case. (In the case of more general {G}, this hypothesis ends up being replaced with {\mu(E_1)/[G:2G] + \mu(E_2) > 1}; see Theorem 2.1 of this recent preprint of Kousek and Radic for a treatment of the case {G={\bf Z}} (but the proof extends without much difficulty to the general case).)

As with Theorem 1, Theorem 7 is still an infinitary statement and does not have a direct finitary analogue (though it can likely be expressed as the conjunction of infinitely many such finitary statements, as we did with Theorem 1). Nevertheless we can formulate the following finitary statement which can be viewed as a “baby” version of the above theorem:


Theorem 8 (Finitary model problem) Let {X = (X,d)} be a compact metric space, let {G = {\bf F}_p^N} be a finite vector space over a field of odd prime order. Let {T} be an action of {G} on {X} by homeomorphisms, let {a \in X}, and let {\mu} be the associated {G}-invariant measure {\mu = {\bf E}_{x \in G} \delta_{T^x a}}. Let {E_1, E_2} be subsets of {X} with {\mu(E_1) + \mu(E_2) > 1 + \delta} for some {\delta>0}. Then for any {\varepsilon>0}, there exist {x_1 \in E_1, x_2 \in E_2} such that
\displaystyle  |\{ h \in G: d(T^h a,x_1) \leq \varepsilon, d(T^h x_1,x_2) \leq \varepsilon \}| \gg_{p,\delta,\varepsilon,X} |G|.


The important thing here is that the bounds are uniform in the dimension {N} (as well as the initial point {a} and the action {T}).

Let us now give a finitary proof of Theorem 8. We can cover the compact metric space {X} by a finite collection {B_1,\dots,B_M} of open balls of radius {\varepsilon/2}. This induces a coloring function {\tilde c: X \rightarrow \{1,\dots,M\}} that assigns to each point in {X} the index {m} of the first ball {B_m} that covers that point. This then induces a coloring {c: G \rightarrow \{1,\dots,M\}} of {G} by the formula {c(h) := \tilde c(T^h a)}. We also define the pullbacks {A_i := \{ h \in G: T^h a \in E_i \}} for {i=1,2}. By hypothesis, we have {|A_1| + |A_2| > (1+\delta)|G|}, and it will now suffice by the triangle inequality to show that

\displaystyle  |\{ h \in G: c(h) = c(x_1); c(h+x_1)=c(x_2) \}| \gg_{p,\delta,M} |G|.

Now we apply the arithmetic lemma of Green with some regularity parameter {\kappa>0} to be chosen later. This allows us to partition {G} into cosets of a subgroup {H} of index {O_{p,\kappa}(1)}, such that on all but {\kappa [G:H]} of these cosets {y+H}, all the color classes {\{x \in y+H: c(x) = c_0\}} are {\kappa^{100}}-regular in the Fourier ({U^2}) sense. Now we sample {x_1} uniformly from {G}, and set {x_2 := 2x_1}; as {p} is odd, {x_2} is also uniform in {G}. If {x_1} lies in a coset {y+H}, then {x_2} will lie in {2y+H}. By removing an exceptional event of probability {O(\kappa)}, we may assume that neither of these cosetgs {y+H}, {2y+H} is a bad coset. By removing a further exceptional event of probability {O_M(\kappa)}, we may also assume that {x_1} is in a popular color class of {y+H} in the sense that
\displaystyle  |\{ x \in y+H: c(x) = c(x_1) \}| \geq \kappa |H| \ \ \ \ \ (1)

since the set of exceptional {x_1} that fail to achieve this only are hit with probability {O(M\kappa)}. Similarly we may assume that
\displaystyle  |\{ x \in 2y+H: c(x) = c(x_2) \}| \geq \kappa |H|. \ \ \ \ \ (2)

Now we consider the quantity
\displaystyle  |\{ h \in y+H: c(h) = c(x_1); c(h+x_1)=c(x_2) \}|

which we can write as
\displaystyle  |H| {\bf E}_{h \in y+H} 1_{c^{-1}(c(x_1))}(h) 1_{c^{-1}(c(x_2))}(h+x_1).

Both factors here are {O(\kappa^{100})}-uniform in their respective cosets. Thus by standard Fourier calculations, we see that after excluding another exceptional event of probabitiy {O(\kappa)}, this quantity is equal to
\displaystyle  |H| (({\bf E}_{h \in y+H} 1_{c^{-1}(c(x_1))}(h)) ({\bf E}_{h \in y+H} 1_{c^{-1}(c(x_2))}(h+x_1)) + O(\kappa^{10})).

By (1), (2), this expression is {\gg \kappa^2 |H| \gg_{p,\kappa} |G|}. By choosing {\kappa} small enough depending on {M,\delta}, we can ensure that {x_1 \in E_1} and {x_2 \in E_2}, and the claim follows.
Now we can prove the infinitary result in Theorem 7. Let us place a metric {d} on {X}. By sparsifying the Følner sequence {\Phi_j = y_j + {\bf F}_p^{N_j}}, we may assume that the {n_j} grow as fast as we wish. Once we do so, we claim that for each {J}, we can find {x_{1,J}, x_{2,J} \in X} such that for each {1 \leq j \leq J}, there exists {n_j \in \Phi_j} that lies outside of {{\bf F}_p^j} such that

\displaystyle  d(T^{n_j} a, x_{1,J}) \leq 1/j, \quad d(T^{n_j} x_{1,J}, x_{2,J}) \leq 1/j.

Passing to a subsequence to make {x_{1,J}, x_{2,J}} converge to {x_1, x_2} respectively, we obtain the desired Erdös progression.
Fix {J}, and let {M} be a large parameter (much larger than {J}) to be chosen later. By genericity, we know that the discrete measures {{\bf E}_{h \in \Phi_M} \delta_{T^h a}} converge vaguely to {\mu}, so any point in the support in {\mu} can be approximated by some point {T^h a} with {h \in \Phi_M}. Unfortunately, {a} does not necessarily lie in this support! (Note that {\Phi_M} need not contain the origin.) However, we are assuming a continuous factor map {\pi:X \rightarrow Z} to the Kronecker factor {Z}, which is a compact abelian group, and {\mu} pushes down to the Haar measure of {Z}, which has full support. In particular, thus pushforward contains {\pi(a)}. As a consequence, we can find {h_M \in \Phi_M} such that {\pi(T^{h_M} a)} converges to {\pi(a)}, even if we cannot ensure that {T^{h_M} a} converges to {a}. We are assuming that {\Phi_M} is a coset of {{\bf F}_p^{n_M}}, so now {{\bf E}_{h \in {\bf F}_p^{n_M}} \delta_{T^{h+h_M} a}} converges vaguely to {\mu}.

We make the random choice {x_{1,J} := T^{h_*+h_M} a}, {x_{2,J} := T^{2h_*+h_M} a}, where {h_*} is drawn uniformly at random from {{\bf F}_p^{n_M}}. This is not the only possible choice that can be made here, and is in fact not optimal in certain respects (in particular, it creates a fair bit of coupling between {x_{1,J}}, {x_{2,J}}), but is easy to describe and will suffice for our argument. (A more appropriate choice, closer to the arguments of Kra et al., would be to {x_{2,J}} in the above construction by {T^{2h_*+k_*+h_M} a}, where the additional shift {k_*} is a random variable in {{\bf F}_p^{n_M}} independent of {h_*} that is uniformly drawn from all shifts annihilated by the first {M} characters associated to some enumeration of the (necessarily countable) point spectrum of {T}, but this is harder to describe.)

Since we are in odd characteristic, the map {h \mapsto 2h} is a permutation on {h \in {\bf F}_p^{n_M}}, and so {x_{1,J}}, {x_{2,J}} are both distributed according to the law {{\bf E}_{h \in {\bf F}_p^{n_M}} \delta_{T^{h+h_M} a}}, though they are coupled to each other. In particular, by vague convergence (and inner regularity) we have

\displaystyle  {\bf P}( x_{1,J} \in E_1 ) \geq \mu(E_1) - o(1)

and
\displaystyle  {\bf P}( x_{2,J} \in E_2 ) \geq \mu(E_2) - o(1)

where {o(1)} denotes a quantity that goes to zero as {M \rightarrow \infty} (holding all other parameters fixed). By the hypothesis {\mu(E_1)+\mu(E_2) > 1}, we thus have
\displaystyle  {\bf P}( x_{1,J} \in E_1, x_{2,J} \in E_2 ) \geq \kappa - o(1) \ \ \ \ \ (3)

for some {\kappa>0} independent of {M}.
We will show that for each {1 \leq j \leq J}, one has

\displaystyle  |\{ h \in \Phi_j: d(T^{h} a,x_{1,J}) \leq 1/j, d(T^h x_{1,J},x_{2,J}) \leq 1/j \}| \ \ \ \ \ (4)

\displaystyle  \gg_{p,\kappa,j,X} (1-o(1)) |\Phi_j|

outside of an event of probability at most {\kappa/2^{j+1}+o(1)} (compare with Theorem 8). If this is the case, then by the union bound we can find (for {M} large enough) a choice of {x_{1,J}}, {x_{2,J}} obeying (3) as well as (4) for all {1 \leq j \leq J}. If the {N_j} grow fast enough, we can then ensure that for each {1 \leq j \leq J} one can find (again for {M} large enough) {n_j} in the set in (4) that avoids {{\bf F}_p^j}, and the claim follows.
It remains to show (4) outside of an exceptional event of acceptable probability. Let {\tilde c: X \rightarrow \{1,\dots,M_j\}} be the coloring function from the proof of Theorem 8 (with {\varepsilon := 1/j}). Then it suffices to show that

\displaystyle  |\{ h \in \Phi_j: c_0(h) = c(h_*); c(h+h_*)=c(2h_*) \}| \gg_{p,\kappa,M_j} (1-o(1)) |\Phi_j|

where {c_0(h) := \tilde c(T^h a)} and {c(h) := \tilde c(T^{h+h_M} a)}. This is a counting problem associated to the patterm {(h_*, h, h+h_*, 2h_*)}; if we concatenate the {h_*} and {2h_*} components of the pattern, this is a classic “complexity one” pattern, of the type that would be expected to be amenable to Fourier analysis (especially if one applies Cauchy-Schwarz to eliminate the {h_*} averaging and absolute value, at which point one is left with the {U^2} pattern {(h, h+h_*, h', h'+h_*)}).
In the finitary setting, we used the arithmetic regularity lemma. Here, we will need to use the Kronecker factor instead. The indicator function {1_{\tilde c^{-1}(i)}} of a level set of the coloring function {\tilde c} is a bounded measurable function of {X}, and can thus be decomposed into a function {f_i} that is measurable on the Kronecker factor, plus an error term {g_i} that is orthogonal to that factor and thus is weakly mixing in the sense that {|\langle T^h g_i, g_i \rangle|} tends to zero on average (or equivalently, that the Host-Kra seminorm {\|g_i\|_{U^2}} vanishes). Meanwhile, for any {\varepsilon > 0}, the Kronecker-measurable function {f_i} can be decomposed further as {P_{i,\varepsilon} + k_{i,\varepsilon}}, where {P_{i,\varepsilon}} is a bounded “trigonometric polynomial” (a finite sum of eigenfunctions) and {\|k_{i,\varepsilon}\|_{L^2} < \varepsilon}. The polynomial {P_{i,\varepsilon}} is continuous by hypothesis. The other two terms in the decomposition are merely meaurable, but can be approximated to arbitrary accuracy by continuous functions. The upshot is that we can arrive at a decomposition

\displaystyle  1_{\tilde c^{-1}(i)} = P_{i,\varepsilon} + k_{i,\varepsilon,\varepsilon'} + g_{i,\varepsilon'}

(analogous to the arithmetic regularity lemma) for any {\varepsilon,\varepsilon'>0}, where {k_{i,\varepsilon,\varepsilon'}} is a bounded continuous function of {L^2} norm at most {\varepsilon}, and {g_{i,\varepsilon'}} is a bounded continuous function of {U^2} norm at most {\varepsilon'} (in practice we will take {\varepsilon'} much smaller than {\varepsilon}). Pulling back to {c}, we then have
\displaystyle  1_{c(h)=i} = P_{i,\varepsilon}(T^{h+h_M} a) + k_{i,\varepsilon,\varepsilon'}(T^{h+h_M}a) + g_{i,\varepsilon'}(T^{h+h_M}a). \ \ \ \ \ (5)

Let {\varepsilon,\varepsilon'>0} be chosen later. The trigonometric polynomial {h \mapsto P_{i,\varepsilon}(T^{h} a)} is just a sum of {O_{\varepsilon,M_j}(1)} characters on {G}, so one can find a subgroup {H} of {G} of index {O_{p,\varepsilon,M_j}(1)} such that these polynomial are constant on each coset of {H} for all {i}. Then {h_*} lies in some coset {a_*+H} and {2h_*} lies in the coset {2a_*+H}. We then restrict {h} to also lie in {a_*+H}, and we will show that
\displaystyle  |\{ h \in \Phi_j \cap (a_*+H): c_0(h) = c(h_*); c(h+h_*)=c(2h_*) \}| \ \ \ \ \ (6)

\displaystyle  \gg_{\kappa,p,M_j} (1-o(1)) |\Phi_j \cap (a_*+H)| 

outside of an exceptional event of proability {\kappa/2+o(1)}, which will establish our claim because {\varepsilon} will ultimately be chosen to dependon {p,\kappa,M_j}.
The left-hand side can be written as

\displaystyle  \sum_{i,i'} \sum_{h \in \Phi_j \cap (a_*+H)} 1_{c_0(h)=i} 1_{c(h_*)=i, c(2h_*)=i'} 1_{c(h+h_*)=i'}.

The coupling of the constraints {c(h_*)=i} and {c(2h_*)=i'} is annoying (as {(h_*,2h_*)} is an “infinite complexity” pattern that cannot be controlled by any uniformity norm), but (perhaps surprisingly) will not end up causing an essential difficulty to the argument, as we shall see when we start eliminating the terms in this sum one at a time starting from the right.
We decompose the {1_{c(h+h_*)=i'}} term using (5):

\displaystyle  1_{c(h+h_*)=i'} = P_{i',\varepsilon}(T^{h+h_*+h_M} a) + k_{i,\varepsilon,\varepsilon'}(T^{h+h_*+h_M}a) + g_{i,\varepsilon'}(T^{h+h_*+h_M}a). 

By Markov’s inequality, and removing an exceptional event of probabiilty at most {\kappa/100}, we may assume that the {g_{i',\varepsilon}} have normalized {L^2} norm {O_{\kappa,M_j}(\varepsilon)} on both of these cosets {a_*+H, 2a_*+H}. As such, the contribution of {k_{i',\varepsilon,\varepsilon'}(T^{h+h_*+h_M}a)} to (6) become negligible if {\varepsilon} is small enough (depending on {\kappa,p,M_j}). From the near weak mixing of the {g_{i,\varepsilon'}}, we know that
\displaystyle {\bf E}_{h \in \Phi_j \cap (a_*+H)} |\langle T^h g_{i,\varepsilon'}, g_{i,\varepsilon'} \rangle| \ll_{p,\varepsilon,M_j} \varepsilon'

for all {i}, if we choose {\Phi_j} large enough. By genericity of {a}, this implies that
\displaystyle {\bf E}_{h \in \Phi_j \cap (a_*+H)} |{\bf E}_{l \in {\bf F}_p^{n_M}} g_{i,\varepsilon'}(T^{h+l+h_M} a) g_{i,\varepsilon'}(T^{l+h_M} a)| \ll_{p,\varepsilon,M_j} \varepsilon' + o(1).

From this and standard Cauchy-Schwarz (or van der Corput) arguments we can then show that the contribution of the {g_{i',\varepsilon'}(T^{h+h_*+h_M}a)} to (6) is negligible outside of an exceptional event of probability at most {\kappa/100+o(1)}, if {\varepsilon'} is small enough depending on {\kappa,p,M_j,\varepsilon}. Finally, the quantity {P_{i',\varepsilon}(T^{h+h_*+h_M} a)} is independent of {h}, and in fact is equal up to negligible error to the density of {c^{-1}(i')} in the coset {{\bf F}_p^{M_j}(2a_*+H)}. This density will be {\gg_{p,\kappa,M_j}} except for those {i'} which would have made a negligible impact on (6) in any event due to the rareness of the event {c(2h_*)=i'} in such cases. As such, to prove (6) it suffices to show that
\displaystyle  \sum_{i,i'} \sum_{h \in \Phi_j \cap (a_*+H)} 1_{c_0(h)=i} 1_{c(h_*)=i, c(2h_*)=i'} \gg_{\kappa,p,M_j} (1-o(1)) |\Phi_j \cap (a_*+H)| 

outside of an event of probability {\kappa/100+o(1)}. Now one can sum in {i'} to simplify the above estiamte to
\displaystyle  \sum_{i} 1_{c(h_*)=i} (\sum_{h \in \Phi_j \cap (a_*+H)} 1_{c_0(h)=i}) / |\Phi_j \cap (a_*+H)| \gg_{\kappa,p,M_j} 1-o(1).

If {i} is such that {(\sum_{h \in \Phi_j \cap (a_*+H)} 1_{c_0(h)=i})/|\Phi_j \cap (a_*+H)|} is small compared with {p,\kappa,M_j}, then by genericity (and assuming {\Phi_j} large enough), the probability that {c(h_*)=i} will similarly be small (up to {o(1)} errors), and thus have a negligible influence on the above sum. As such, the above estimate simplifies to
\displaystyle  \sum_{i} 1_{c(h_*)=i} \gg_{\kappa,p,M_j} 1-o(1).

But the left-hand side sums to one, and the claim follows.