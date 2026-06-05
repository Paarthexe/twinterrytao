---
title: "Open question: effective Skolem-Mahler-Lech theorem"
source: "terrytao.wordpress.com"
url: "https://terrytao.wordpress.com/2007/05/25/open-question-effective-skolem-mahler-lech-theorem/"
date: "2007-05-25"
categories: ["number theory", "algebraic number theory", "open questions", "expository"]
---
The Skolem-Mahler-Lech theorem in algebraic number theory is a significant generalisation of the obvious statement that a polynomial either has finitely many zeroes (in particular, the set of zeroes is bounded), or it vanishes identically. It appeals to me (despite not really being within my areas of expertise) because it is one of the simplest (non-artificial) results I know of which (currently) comes with an ineffective bound – a bound which is provably finite, but which cannot be computed! It appears that to obtain an effective result, one may need a rather different proof. (I thank Kousha Etessami and Tom Lenagan for drawing this problem to my attention.)

Ineffective bounds seem to arise particularly often in number theory. I am aware of at least three ways in which they come in:

By using methods from soft (infinitary) analysis.
By using the fact that any finite set in a metric space is bounded (i.e. is contained in a ball of finite radius centred at a designated origin).
By using the fact that any set of finite diameter in a metric space is bounded.
Regarding #1, there are often ways to make these arguments quantitative and effective, as discussed in my previous post. But #2 and #3 seem to be irreducibly ineffective: if you know that a set A has finite cardinality or finite diameter, you know it has finite distance to the origin, but an upper bound on the cardinality or diameter does not translate to an effective bound on the radius of the ball centred at the origin needed to contain the set. [In the spirit of the preceding post, one can conclude an effective “meta-bound” on such a set, establishing a large annulus \{ x: N \leq |x| \leq N+F(N)\} in which the set has no presence, but this is not particularly satisfactory.] The problem with the Skolem-Mahler-Lech theorem is that all the known proofs use #2 at some point.


So, what is the Skolem-Mahler-Lech theorem? There are many ways to phrase it, but let us use the formulation using linear recurrence sequences, and in particular restrict attention to integer linear recurrence sequences for simplicity (which was the scope of the original result of Skolem; Mahler and Lech handled algebraic numbers and elements of fields of characteristic zero respectively. The situation in positive characteristic is more subtle, as this recent paper of Derksen shows). By definition, an integer linear recurrence sequence is a sequence x_0, x_1, x_2, \ldots of integers which obeys a linear recurrence relation

x_n = a_1 x_{n-1} + a_2 x_{n-2} + \ldots + a_d x_{n-d}

for some integer d \geq 1 (the degree of the linear recurrence sequence), some integer coefficients a_1,\ldots, a_d with a_d non-zero, and all n \geq d. This data, together with the first d values x_0,\ldots,x_{d-1} of the sequence, clearly determine the entire sequence. The most famous example of a linear recurrence sequence is of course the Fibonacci sequence 0,1,1,2,3,5,\ldots given by

x_n = x_{n-1} + x_{n-2}; x_0 = 0, x_1 = 1.

It is also a nice exercise to show that any polynomial sequence (e.g. the squares 0, 1, 4, 9, \ldots is a linear recurrence sequence), or more generally that the component-wise sum or product of two linear recurrence sequences is another linear recurrence sequence. (Hint: this is related to the fact that the sum or product of algebraic integers is again an algebraic integer.)

The Skolem-Mahler-Lech theorem concerns the set of zeroes Z := \{ n \in {\Bbb N}: x_n = 0 \} of a given integer linear recurrence sequence. In the case of the Fibonacci sequence, the set of zeroes is pretty boring, just {0}. To give a somewhat trivial example, the linear recurrence sequence

x_n = x_{n-2}; x_0 = 0, x_1 = 1

has a zero set which is the even numbers \{0,2,4,\ldots\}. Similarly, the linear recurrence sequence

x_n = x_{n-4} + x_{n-2}; x_0 = x_1 = x_3 = 0, x_2 = 1

has a zero set \{ 0, 1, 3, 5, \ldots \}, i.e. the odd numbers together with 0. One can ask whether more interesting zero sets are possible; for instance, can one design a linear recurrence system which only vanishes at the square numbers \{0,1,4,9,\ldots\}? The Skolem-Mahler-Lech theorem says no:

Skolem-Mahler-Lech theorem. The zero set of a linear recurrence set is eventually periodic, i.e. it agrees with a periodic set for sufficiently large n. In fact, a slightly stronger statement is true: the zero set is the union of a finite set and a finite number of residue classes \{ n \in {\Bbb N}: n = r \mod m \}.

Interestingly, all known proofs of this theorem require that one introduce the p-adic integers {\Bbb Z}_p (or a thinly disguised version thereof). Let me quickly sketch a proof as follows (loosely based on the proof of Hansel). Firstly it is not hard to reduce to the case where the final coefficient a_d is non-zero. Then, by elementary linear algebra, one can get a closed form for the linear recurrence sequence as

x_n = \langle A^n v, w \rangle

where A is an invertible d \times d matrix with integer coefficients, and v, w are d-dimensional vectors with integer coefficients (one can write A, v, w explicitly in terms of a_1,\ldots,a_d and x_0,\ldots,x_{d-1}, but it is not necessary to do so for this argument). Since A is invertible, we can find a large prime p such that A is also invertible modulo p; for technical reasons we also need p to be larger than 2 so (any prime not dividing 2 det(A) will do). Let us now fix this p. The invertible matrices A^n \mod p over the finite field {\Bbb F}_p take on only finitely many values, thus by the pigeonhole principle there must exist a finite m \geq 1 such that A^m = I \mod p, where I is the identity matrix.

This m is going to be the eventual period of the zero set; more precisely, for every r = 0,\ldots,m-1, I claim that the modified zero set \{ n \in {\Bbb N}: x_{mn+r} = 0 \} is either finite, or equal to all of {\Bbb N} (this will clearly imply the Skolem-Mahler-Lech theorem). To see this claim, suppose that this modified zero set is infinite for some r, thus

\langle A^{mn} A^r v, w \rangle = 0

for infinitely any n. By construction of m, we can write A^m = I + p B for some integer-valued matrix B, thus

P(n) = 0 for infinitely many integers n, where

P(n) := \langle (1+pB)^{n} A^r v, w \rangle.

This identity makes sense in the (rational) integers {\Bbb Z}, and hence also in the larger ring of p-adic integers {\Bbb Z}_p. On the other hand, observe from binomial expansion that P(n) can be expressed as a formal power series in p with coefficients polynomial in n:

P(n) = \sum_{j=0}^\infty p^j P_j(n).

Here the P_j are polynomials with coefficients in the p-adic integers.  Indeed, the binomial expansion of (I+pB)^n contains terms involving a polynomial in n times \frac{p^k}{k!} for natural number k.  The number of times p divides k is \lfloor k/p \rfloor + \lfloor k/p^2 \rfloor + \dots \leq k/p + k/p^2 + \dots = k/(p-1) which grows slower than k since p was assumed to be larger than 2; hence each of the P_j can be built using only finitely many of the terms in the binomial expansion.

Because of this, the function P: {\Bbb Z} \to {\Bbb Z} extends continuously to a function P: {\Bbb Z}_p \to {\Bbb Z}_p, such that n \mapsto P(n) \mod p^j is a polynomial in n for each j. In other words, P is a uniform limit of polynomials in the p-adic topology. [Note that the Stone-Weierstrass theorem is not applicable here, because we are using p-adic valued functions rather than real or complex-valued ones.] What we need to show is that if P has infinitely many zeroes, then it vanishes everywhere (which is of course what we expect polynomial-like objects to do).

Now if P(n_0) = 0 for some n_0 (either an integer or a p-adic integer, it doesn’t matter), one can then formally divide P(n) = P(n)-P(n_0) by n-n_0 (as in the factor theorem from high school algebra) to conclude that P(n) = (n-n_0) Q(n) for some continuous function Q which, like P, is a polynomial modulo p^j for each j, and whose “constant coefficient” Q_0(n) either vanishes, or has degree strictly less than the corresponding coefficient P_0(n) of P. Iterating this fact, we eventually see that if P has infinitely many zeroes, then it contains a factor with vanishing constant coefficient, or in other words it is divisible by p. We iterate this fact again and conclude that if P has infinitely many zeroes then it must be divisible by arbitrarily many powers of p, and thus must vanish everywhere. This concludes the proof.

Now, the above proof clearly gives a quite effective and computable bound on the eventual period m of the zero set. By working somewhat harder, Evertse, Schlickewei, and Schmidt obtained an effective bound on how many exceptional zeroes there are – zeroes of one of these almost polynomials P which do not cause P to vanish entirely. But there appears to be no effective bound known as to how large these zeroes are! In particular, one does not even know how to decide whether this set is non-empty, thus we have

Open problem. Given an integer linear recurrence sequence (i.e. given the data d, a_1,\ldots,a_d, x_0,\ldots,x_{d-1} as integers), is the truth of the statement “x_n \neq 0 for all n” decidable in finite time?

(Note that I am only asking here for decidability, and not even asking for effective bounds.) It is faintly outrageous that this problem is still open; it is saying that we do not know how to decide the halting problem even for “linear” automata!

The basic problem seems to boil down to one of determining whether an “almost polynomial” P: {\Bbb Z}_p \to {\Bbb Z}_p (i.e. a uniform limit of polynomials) has an integer zero or not. It is not too hard to find the p-adic zeroes of P to any specified accuracy (by using the p-adic version of Newton’s method, i.e. Hensel’s lemma), but it seems that one needs to know the zeroes to infinite accuracy in order to decide whether they are integers or not. It may be that some techniques from Diophantine approximation (e.g. some sort of p-adic analogue of the Thue-Siegel-Roth theorem) are relevant. Alternatively, one might want to find a completely different proof of the Skolem-Mahler-Lech theorem, which does not use p-adics at all.