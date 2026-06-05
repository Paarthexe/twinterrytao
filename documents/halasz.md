---
title: "Cheap Halasz"
source: "terrytao.wordpress.com"
url: "https://terrytao.wordpress.com/2015/02/24/cheap-halasz/"
date: "2015-02-24"
categories: ["number theory", "multiplicative number theory", "expository"]
---
A basic estimate in multiplicative number theory (particularly if one is using the Granville-Soundararajan “pretentious” approach to this subject) is the following inequality of Halasz (formulated here in a quantitative form introduced by Montgomery and Tenenbaum).

Theorem 1 (Halasz inequality) Let {f: {\bf N} \rightarrow {\bf C}} be a multiplicative function bounded in magnitude by {1}, and suppose that {x \geq 3}, {T \geq 1}, and { M \geq 0} are such that

\displaystyle  \sum_{p \leq x} \frac{1 - \hbox{Re}(f(p) p^{-it})}{p} \geq M \ \ \ \ \ (1)

for all real numbers {t} with {|t| \leq T}. Then

\displaystyle  \frac{1}{x} \sum_{n \leq x} f(n) \ll (1+M) e^{-M} + \frac{1}{\sqrt{T}}.

As a qualitative corollary, we conclude (by standard compactness arguments) that if

\displaystyle  \sum_{p} \frac{1 - \hbox{Re}(f(p) p^{-it})}{p} = +\infty

for all real {t}, then

\displaystyle  \frac{1}{x} \sum_{n \leq x} f(n) = o(1) \ \ \ \ \ (2)

as {x \rightarrow \infty}. In the more recent work of this paper of Granville and Soundararajan, the sharper bound

\displaystyle  \frac{1}{x} \sum_{n \leq x} f(n) \ll (1+M) e^{-M} + \frac{1}{T} + \frac{\log\log x}{\log x}

is obtained (with a more precise description of the {(1+M) e^{-M}} term).
The usual proofs of Halasz’s theorem are somewhat lengthy (though there has been a recent simplification, in forthcoming work of Granville, Harper, and Soundarajan). Below the fold I would like to give a relatively short proof of the following “cheap” version of the inequality, which has slightly weaker quantitative bounds, but still suffices to give qualitative conclusions such as (2).

Theorem 2 (Cheap Halasz inequality) Let {f: {\bf N} \rightarrow {\bf C}} be a multiplicative function bounded in magnitude by {1}. Let {T \geq 1} and {M \geq 0}, and suppose that {x} is sufficiently large depending on {T,M}. If (1) holds for all {|t| \leq T}, then

\displaystyle  \frac{1}{x} \sum_{n \leq x} f(n) \ll (1+M)^{1/6} e^{-M/3} + \frac{1}{T}.

The non-optimal exponent {1/3} can probably be improved a bit by being more careful with the exponents, but I did not try to optimise it here. A similar bound appears in the first paper of Halasz on this topic.
The idea of the argument is to split {f} as a Dirichlet convolution {f = f_1 * f_2 * f_3} where {f_1,f_2,f_3} is the portion of {f} coming from “small”, “medium”, and “large” primes respectively (with the dividing line between the three types of primes being given by various powers of {x}). Using a Perron-type formula, one can express this convolution in terms of the product of the Dirichlet series of {f_1,f_2,f_3} respectively at various complex numbers {1+it} with {|t| \leq T}. One can use {L^2} based estimates to control the Dirichlet series of {f_2,f_3}, while using the hypothesis (1) one can get {L^\infty} estimates on the Dirichlet series of {f_1}. (This is similar to the Fourier-analytic approach to ternary additive problems, such as Vinogradov’s theorem on representing large odd numbers as the sum of three primes.) This idea was inspired by a similar device used in the work of Granville, Harper, and Soundarajan. A variant of this argument also appears in unpublished work of Adam Harper.
I thank Andrew Granville for helpful comments which led to significant simplifications of the argument.

— 1. Basic estimates —

We need the following basic tools from analytic number theory. We begin with a variant of the classical Perron formula.

Proposition 3 (Perron type formula) Let {f: {\bf N} \rightarrow {\bf C}} be an arithmetic function bounded in magnitude by {1}, and let {x, T \geq 1}. Assume that the Dirichlet series {F(s) := \sum_{n=1}^\infty \frac{f(n)}{n^s}} is absolutely convergent for {\hbox{Re}(s) \geq 1}. Then

\displaystyle  \frac{1}{x} \sum_{n \leq x} f(n) \ll \int_{-T}^T |F(1+it)| \frac{dt}{1+|t|} + \frac{1}{T} + \frac{T}{x}.

Proof: By telescoping series (and treating the contribution of {n \ll T} trivially), it suffices to show that

\displaystyle  \sum_{x/e \leq n \leq x} f(n) \ll x \int_{-T}^T |F(1+it)| \frac{dt}{1+|t|} + \frac{x}{T}

whenever {x \geq T}.
The left-hand side can be written as

\displaystyle  x \sum_n \frac{f(n)}{n} g( \log x - \log n ) \ \ \ \ \ (3)

where {g(u) := e^{-u} 1_{[0,1]}(u)}. We now introduce the mollified version

\displaystyle  \tilde g(u) := \int_{\bf R} g(u + \frac{v}{T}) \Psi(v)\ dv

of {g}, where

\displaystyle  \Psi(v) := \frac{1}{2\pi} \int_{\bf R} \psi(t) e^{itv}\ dt 

and {\psi: {\bf R} \rightarrow {\bf R}} is a fixed smooth function supported on {[-1,1]} that equals {1} at the origin. Basic Fourier analysis then tells us that {\Psi} is a Schwartz function with total mass one. This gives the crude bound

\displaystyle  \tilde g(u) \ll 1 

for any {u}. For {u \leq -\frac{1}{T}} or {u \geq 1 + \frac{1}{T}}, we use the bound {\Psi(v) \ll \frac{1}{(1+|v|)^{10}}} (say) to arrive at the bound

\displaystyle  \tilde g(u) \ll (T \hbox{dist}(u, \{0,1\}))^{-9};

for {\frac{1}{T} \leq u \leq 1 - \frac{1}{T}} we again use {\Psi(v) \ll \frac{1}{(1+|v|)^{10}}} and write

\displaystyle  \tilde g(u) - g(u) = \int_{\bf R} (g(u + \frac{v}{T}) - g(u)) \Psi(v)\ dv

and use the Lipschitz bound {g(u+\frac{v}{T}) - g(u) \ll \frac{v}{T}} for {u + \frac{v}{T} \in [0,1]} to obtain

\displaystyle  \tilde g(u) - g(u) \ll (T \hbox{dist}(u, \{0,1\}))^{-9}

for such {u}. Putting all these bounds together, we see that

\displaystyle  \tilde g(u) = g(u) + O( \frac{1}{(1 + T |u|)^9} ) + O( \frac{1}{(1 + T |u-1|)^9} )

for all {u}. In particular, we can write (3) as

\displaystyle  x \sum_n \frac{f(n)}{n} \tilde g(\log x - \log n) 

\displaystyle + O( \sum_n \frac{x}{n} \frac{1}{(1 + T |\log x - \log n|)^9} + \frac{1}{(1 + T |\log x/e - \log n|)^9} ).

The expression {\frac{x}{n} \frac{1}{(1 + T |\log x - \log n|)^9} + \frac{1}{(1 + T |\log x/e - \log n|)^9}} is bounded by {O( \frac{x}{n} \frac{1}{T \log^9 x} )} when {n \leq x/10}, is bounded by {O( \frac{x}{n} \frac{1}{T \log^9 n} )} when {n \geq 10x}, is bounded by {O(1)} when {n = (1+O(1/T)) x} or {n = (1+O(1/T)) x/e}, and is bounded by {(\frac{T}{x} |n-x|)^{-9} + (\frac{T}{x} |n-x/e|)^{-9}} otherwise. From these bounds, a routine calculation (using the hypothesis {x \geq T}) shows that

\displaystyle  \sum_n \frac{x}{n} \frac{1}{(1 + T |\log x - \log n|)^9} + \frac{1}{(1 + T |\log x/e - \log n|)^9} \ll \frac{x}{T}

and so it remains to show that

\displaystyle  \sum_n \frac{f(n)}{n} \tilde g(\log x - \log n) \ll \int_{-T}^T |F(1+it)| \frac{dt}{1+|t|}.

Writing

\displaystyle  \tilde g(u) = T \int_{\bf R} g(v) \Psi( T(v-u) )\ dv 

\displaystyle  = \frac{T}{2\pi} \int_{\bf R} \psi(t) G(Tt) e^{-iTtu} dt 

\displaystyle  = \frac{1}{2\pi} \int_{\bf R} \psi(t/T) G(t) e^{-itu}\ dt

where

\displaystyle  G(t) := \int_{\bf R} g(v) e^{itv}\ dv 

we see from the triangle inequality and the support of {\psi(t/T)} that

\displaystyle  \sum_n \frac{f(n)}{n} \tilde g(\log x - \log n) \ll \int_{|t| \leq T} |G(t)| |\sum_n \frac{f(n)}{n} e^{-it(\log x- \log n)}|\ dt 

\displaystyle  \ll \int_{|t| \leq T} |G(t)| |F(1+it)|\ dt.

But from integration by parts we see that {G(t) \ll \frac{1}{1+|t|}}, and the claim follows. \Box
Next, we recall a standard {L^2} mean value estimate for Dirichlet series:

Proposition 4 ({L^2} mean value estimate) Let {f: {\bf N} \rightarrow {\bf C}} be an arithmetic function, and let {T \geq 1}. Assume that the Dirichlet series {F(s) := \sum_{n=1}^\infty \frac{f(n)}{n^s}} is absolutely convergent for {\hbox{Re}(s) \geq 1}. Then

\displaystyle  \int_{|t| \leq T} |F(1+it)|^2\ dt \ll T \sum_{n_1,n_2: \log n_2 = \log n_1 + O(1/T)} \frac{|f(n_1)| |f(n_2)|}{n_1 n_2}.

Proof: This follows from Lemma 7.1 of Iwaniec-Kowalski; for the convenience of the reader we reproduce the short proof here. Introducing the normalised sinc function {\hbox{sinc}(x) := \frac{\sin(\pi x)}{\pi x}}, we have

\displaystyle  \int_{|t| \leq T} |F(1+it)|^2\ dt \ll \int_{\bf R} |F(1+it)|^2 \hbox{sinc}^2( t / 2T )\ dt 

\displaystyle  = \sum_{n_1,n_2} f(n_1) \overline{f(n_2)} \int_{\bf R} \frac{1}{n_1^{1+it} n_2^{1-it}} \hbox{sinc}^2(t/2T)\ dt 

\displaystyle  \ll \sum_{n_1,n_2} \frac{|f(n_1)| |f(n_2)|}{n_1 n_2} |\int_{\bf R} \hbox{sinc}^2(t/2T) e^{it (\log n_1 - \log n_2)}\ dt|.

But a standard Fourier-analytic computation shows that {\int_{\bf R} \hbox{sinc}^2(t/2T) e^{it (\log n_1 - \log n_2)}\ dt} vanishes unless {\log n_2 = \log n_1 + O(1/T)}, in which case the integral is {O(T)}, and the claim follows. \Box
Now we recall a basic sieve estimate:

Proposition 5 (Sieve bound) Let {x \geq 1}, let {I} be an interval of length {x}, and let {{\mathcal P}} be a set of primes up to {x}. If we remove one residue class mod {p} from {I} for every {p \in {\mathcal P}}, the number of remaining natural numbers in {I} is at most {\ll |I| \prod_{p \in {\mathcal P}} (1 - \frac{1}{p})}.

Proof: This follows for instance from the fundamental lemma of sieve theory (see e.g. Corollary 19 of this blog post). (One can also use the Selberg sieve or the large sieve.) \Box
Finally, we record a standard estimate on the number of smooth numbers:

Proposition 6 Let {u \geq 1} and {\varepsilon>0}, and suppose that {x} is sufficiently large depending on {u,\varepsilon}. Then the number of natural numbers in {[1,x]} which have no prime factor larger than {x^{1/u}} is at most {O( u^{-(1-\varepsilon)u} x )}.

Proof: See Corollary 1.3 of this paper of Hildebrand and Tenenbaum. (The result also follows from the more classical work of Dickman.) We sketch a short proof here due to Kevin Ford. Let {{\mathcal S}} denote the set of numbers that are “smooth” in the sense that they have no prime factor larger than {x^{1/u}}. It then suffices to prove the bound

\displaystyle  \sum_{n \in {\mathcal S}: n \leq x} \log n \ll \exp( - u \log u + O(u) ) x \log x, \ \ \ \ \ (4)

since the contribution of those {n} less than (say) {\sqrt{x}} is negligible, and for the other values of {n}, {\log n} is comparable to {\log x}. Writing {\log n = \sum_{dm=n} \Lambda(d)}, we can rearrange the left-hand side as

\displaystyle  \sum_{m \in {\mathcal S}: m \leq x} \sum_{d \in {\mathcal S}: d \leq x/m} \Lambda(d).

By the prime number theorem, the contribution to {\sum_{d \in {\mathcal S}: d \leq x/m} \Lambda(d)} of those {d \leq x^{1/u}} is {O( \min( x^{1/u}, x/m )}, and the contribution of those {d} with {d > x^{1/u}} consists only of prime powers, which contribute {O( (x/m)^{1/2} )}. Combining these estimates, we can get a bound of the form

\displaystyle  \sum_{d \in {\mathcal S}: d \leq x/m} \Lambda(d) \ll (x/m)^{1-\rho} (x^{1/u})^\rho

where {0 < \rho < 1/2} is a quantity to be chosen later. Thus we can bound the left-hand side of (4) by

\displaystyle  O( x^{\rho/u} x^{1-\rho} \sum_{m \in {\mathcal S}} \frac{1}{m^{1-\rho}} )

which by Euler products can be bounded by

\displaystyle  O( x^{\rho/u} x^{1-\rho} \exp( \sum_{p \leq x^{1/u}} \frac{1}{p^{1-\rho}} ) ).

By the mean value theorem applied to the function {t \mapsto \exp( \rho t \log x^{1/u})}, we can bound {p^\rho = \exp( \rho \log p )} by {1 + \frac{\log p}{\log x^{1/u}} \exp( \rho \log x^{1/u} )} for {p \leq x^{1/u}}. By Mertens’ theorem, we thus get a bound of

\displaystyle  O( x^{\rho/u} x^{1-\rho} \exp( \log\log x^{1/u} + O( \exp( \rho \log x^{1/u} ) ) ).

If we make the choice {\rho := \frac{\log u}{\log x^{1/u}}}, we obtain the required bound (4). \Box

— 2. Proof of theorem —

By increasing {M} as necessary we may assume that {M \geq 10} (say). Let {0 < \varepsilon_2 < \varepsilon_1 \leq 1/2} be small parameters (depending on {M}) to be optimised later; we assume {x} to be sufficiently large depending on {\varepsilon_1,\varepsilon_2,T}. Call a prime {p} small if {p \leq x^{\varepsilon_2}}, medium if {x^{\varepsilon_2} < p \leq x^{\varepsilon_1}}, and large if {x^{\varepsilon_1} < p \leq x}. Observe that for any {n \leq x} we can factorise {f} as a Dirichlet convolution

\displaystyle  f(n) = f_1 * f_2 * f_3(n) 

where

{f_1} is the restriction of {f} to those natural numbers {n} whose prime factors are all small;
{f_2} is the restriction of {f} to those natural numbers {n} whose prime factors are all medium;
{f_3} is the restriction of {f} to those natural numbers {n} whose prime factors are all large.
We thus have

\displaystyle  \frac{1}{x} \sum_{n \leq x} f(n) = \frac{1}{x} \sum_{n \leq x} f_1*f_2*f_3(n). \ \ \ \ \ (5)

It is convenient to remove the Dirac function {\delta(n) := 1_{n=1}} from {f_2,f_3}, so we write

\displaystyle  f_2 = \delta + f'_2; \quad f_3 = \delta + f'_3 

and split

\displaystyle  f_1*f_2*f_3 = f_1*f_2 + f_1*f'_3 + f_1*f'_2*f'_3.

Note that {f_1*f_2} is the restriction of {f} to those numbers {n \leq x} whose prime factors are all small or medium. By Proposition 6, the number of such {n} can certainly be bounded by {O(e^{-1/\varepsilon_1} x)} if {x} is sufficiently large. Thus the contribution of this term to (5) is {O( e^{-1/\varepsilon_1} )}.
Similarly, {f_1 * f'_3} is the restriction of {f} to those numbers {n \leq x} which contain at least one large prime factor, but no medium prime factors. By Proposition 5 the number of such {n} is bounded by {O( \frac{\varepsilon_2}{\varepsilon_1} x )} if {x} is sufficiently large. Thus the contribution of this term to (5) is {O( \frac{\varepsilon_2}{\varepsilon_1} )}, and hence

\displaystyle  \frac{1}{x} \sum_{n \leq x} f(n) \ll |\frac{1}{x} \sum_{n \leq x} f_1*f'_2*f'_3(n)| + e^{-1/\varepsilon_1} + \frac{\varepsilon_2}{\varepsilon_1}.

Note that {f_1*f'_2*f'_3} is only supported on numbers whose prime factors do not exceed {x}, so the Dirichlet series of {f_1*f'_2*f'_3} is absolutely convergent for {\hbox{Re}(s) \geq 1} and is equal to {F_1(s) F'_2(s) F'_3(s)}, where {F_1,F'_2,F'_3} are the Dirichlet series of {f_1,f'_2,f'_3} respectively. Since {f_1*f'_2*f'_3} is bounded in magnitude by {1} (being a restriction of {f}), we may apply Proposition 3 and conclude (for {x} large enough, and discarding the {\frac{1}{1+|t|}} denominator) that

\displaystyle  \frac{1}{x} \sum_{n \leq x} f(n) \ll \int_{|t| \leq T} |F_1(1+it)| |F'_2(1+it)| |F'_3(1+it)|\ dt 

\displaystyle + \frac{1}{T} + e^{-1/\varepsilon_1} + \frac{\varepsilon_2}{\varepsilon_1}.

We now record some {L^2} estimates:

Lemma 7 For sufficiently large {x}, we have

\displaystyle  \int_{|t| \leq T} |F'_2(1+it)|^2\ dt \ll \frac{\varepsilon_1}{\varepsilon_2^2 \log x}

and

\displaystyle  \int_{|t| \leq T} |F'_3(1+it)|^2\ dt \ll \frac{1}{\varepsilon_1^2 \log x}.

Proof: We just prove the former inequality, as the latter is similar. By Proposition 4, we have

\displaystyle  \int_{|t| \leq T} |F'_2(1+it)|^2\ dt \ll T \sum_{n_1,n_2: \log n_1 = \log n_2 + O(1/T)} \frac{|f'_2(n_1)| |f'_2(n_2)|}{n_1 n_2}.

The term {f'_2(n_1)} vanishes unless {n_1 \geq x^{\varepsilon_2}}, and we have {n_2 = (1+O(1/T)) n_1}, so we can bound the right-hand side by

\displaystyle  \ll T \sum_{n_1 \geq x^{\varepsilon_2}} \frac{|f'_2(n_1)|}{n_1^2}\sum_{n_2 = (1+O(1/T)) n_1} \frac{|f'_2(n_2)|}{n}.

The inner summand is bounded by {1} and supported on those {n_2} that are not divisible by any small primes. From Proposition 5 and Mertens’ theorem we conclude that

\displaystyle  \sum_{n_2 = (1+O(1/T)) n_1} |f'_2(n_2)| \ll \frac{1}{T \varepsilon_2 \log x} n_1 

and thus

\displaystyle  \int_{|t| \leq T} |F'_2(1+it)|^2\ dt \ll \frac{1}{\varepsilon_2 \log x} \sum_{n_1} \frac{|f'_2(n_1)|}{n_1}

\displaystyle  \ll \frac{1}{\varepsilon_2 \log x} \prod_{x^{\varepsilon_2} < p \leq x^{\varepsilon_1}} (1-\frac{1}{p})^{-1} 

\displaystyle  \ll \frac{\varepsilon_1}{\varepsilon^2_2 \log x} 

as desired. \Box
We also have an {L^\infty} estimate:

Lemma 8 For sufficiently large {x}, we have

\displaystyle  |F_1(1+it)| \ll \frac{1}{\varepsilon_2} e^{-M} \log x

for all {|t| \leq T}.

Proof: From Euler products, Mertens’ theorem, and (1) we have

\displaystyle  F_1(1+it) = \prod_{p \leq x^{\varepsilon_2}} \sum_{j=0}^\infty \frac{f(p^j)}{p^{j(1+it)}} 

\displaystyle  \ll \prod_{p \leq x^{\varepsilon_2}} |1 + \frac{f(p) p^{-it}}{p}| 

\displaystyle  \ll \exp( \sum_{p \leq x^{\varepsilon_2}} \hbox{Re} \frac{f(p) p^{-it}}{p} ) 

\displaystyle  \ll \varepsilon_2 \log x \exp( - \sum_{p \leq x^{\varepsilon_2}} \frac{1 - \hbox{Re} f(p) p^{-it}}{p} ) 

\displaystyle  \ll \varepsilon_2 \log x \exp( -M + 2\log \frac{1}{\varepsilon_2} ) 

\displaystyle  \ll \frac{1}{\varepsilon_2} e^{-M} \log x

as desired. \Box
Applying Hölder’s inequality, we conclude that

\displaystyle  \frac{1}{x} \sum_{n \leq x} f(n) \ll \frac{1}{\varepsilon_1^{1/2} \varepsilon^2_2} e^{-M} + e^{-1/\varepsilon_1} + \frac{\varepsilon_2}{\varepsilon_1}.

Setting {\varepsilon_1 := 1/M} and {\varepsilon_2 := M^{1/6} e^{-M/3}} we obtain the claim.