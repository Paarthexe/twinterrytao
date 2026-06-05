---
title: "The Szemerédi-Trotter theorem via the polynomial ham sandwich theorem"
source: "terrytao.wordpress.com"
url: "https://terrytao.wordpress.com/2011/02/18/the-szemeredi-trotter-theorem-via-the-polynomial-ham-sandwich-theorem/"
date: "2011-02-18"
categories: ["geometry", "discrete geometry", "incidence geometry", "expository"]
---
The ham sandwich theorem asserts that, given {d} bounded open sets {U_1,\ldots,U_d} in {{\bf R}^d}, there exists a hyperplane {\{ x \in {\bf R}^d: x \cdot v = c \}} that bisects each of these sets {U_i}, in the sense that each of the two half-spaces {\{ x \in {\bf R}^d: x \cdot v < c \}, \{ x \in {\bf R}^d: x \cdot v > c \}} on either side of the hyperplane captures exactly half of the volume of {U_i}. The shortest proof of this result proceeds by invoking the Borsuk-Ulam theorem.

A useful generalisation of the ham sandwich theorem is the polynomial ham sandwich theorem, which asserts that given {m} bounded open sets {U_1,\ldots,U_m} in {{\bf R}^d}, there exists a hypersurface {\{ x \in {\bf R}^d: Q(x)=0\}} of degree {O_d( m^{1/d} )} (thus {P: {\bf R}^d \rightarrow {\bf R}} is a polynomial of degree {O(m^{1/n})} such that the two semi-algebraic sets {\{ Q > 0 \}} and {\{ Q < 0\}} capture half the volume of each of the {U_i}. (More precisely, the degree will be at most {D}, where {D} is the first positive integer for which {\binom{D+d}{d}} exceeds {m}.) This theorem can be deduced from the Borsuk-Ulam theorem in the same manner that the ordinary ham sandwich theorem is (and can also be deduced directly from the ordinary ham sandwich theorem via the Veronese embedding).

The polynomial ham sandwich theorem is a theorem about continuous bodies (bounded open sets), but a simple limiting argument leads one to the following discrete analogue: given {m} finite sets {S_1,\ldots,S_m} in {{\bf R}^d}, there exists a hypersurface {\{ x \in {\bf R}^d: Q(x)=0\}} of degree {O_d( m^{1/d} )}, such that each of the two semi-algebraic sets {\{ Q > 0 \}} and {\{ Q < 0\}} contain at most half of the points on {S_i} (note that some of the points of {S_i} can certainly lie on the boundary {\{Q=0\}}). This can be iterated to give a useful cell decomposition:

Proposition 1 (Cell decomposition) Let {P} be a finite set of points in {{\bf R}^d}, and let {D} be a positive integer. Then there exists a polynomial {Q} of degree at most {D}, and a decomposition

\displaystyle  {\bf R}^d = \{ Q = 0\} \cup C_1 \cup \ldots \cup C_m

into the hypersurface {\{Q=0\}} and a collection {C_1,\ldots,C_m} of cells bounded by {\{P=0\}}, such that {m = O_d(D^d)}, and such that each cell {C_i} contains at most {O_d( |P|/D^d )} points.

A proof is sketched in this previous blog post. The cells in the argument are not necessarily connected (being instead formed by intersecting together a number of semi-algebraic sets such as {\{ Q > 0\}} and {\{Q<0\}}), but it is a classical result (established independently by Oleinik-Petrovskii, Milnor, and Thom) that any degree {D} hypersurface {\{Q=0\}} divides {{\bf R}^d} into {O_d(D^d)} connected components, so one can easily assume that the cells are connected if desired. (Incidentally, one does not need the full machinery of the results in the above cited papers – which control not just the number of components, but all the Betti numbers of the complement of {\{Q=0\}} – to get the bound on connected components; one can instead observe that every bounded connected component has a critical point where {\nabla Q = 0}, and one can control the number of these points by Bezout’s theorem, after perturbing {Q} slightly to enforce genericity, and then count the unbounded components by an induction on dimension.)

Remark 1 By setting {D} as large as {O_d(|P|^{1/m})}, we obtain as a limiting case of the cell decomposition the fact that any finite set {P} of points in {{\bf R}^d} can be captured by a hypersurface of degree {O_d(|P|^{1/m})}. This fact is in fact true over arbitrary fields (not just over {{\bf R}}), and can be proven by a simple linear algebra argument (see e.g. this previous blog post). However, the cell decomposition is more flexible than this algebraic fact due to the ability to arbitrarily select the degree parameter {D}.

The cell decomposition can be viewed as a structural theorem for arbitrary large configurations of points in space, much as the Szemerédi regularity lemma can be viewed as a structural theorem for arbitrary large dense graphs. Indeed, just as many problems in the theory of large dense graphs can be profitably attacked by first applying the regularity lemma and then inspecting the outcome, it now seems that many problems in combinatorial incidence geometry can be attacked by applying the cell decomposition (or a similar such decomposition), with a parameter {D} to be optimised later, to a relevant set of points, and seeing how the cells interact with each other and with the other objects in the configuration (lines, planes, circles, etc.). This strategy was spectacularly illustrated recently with Guth and Katz‘s use of the cell decomposition to resolve the Erdös distinct distance problem (up to logarithmic factors), as discussed in this blog post.

In this post, I wanted to record a simpler (but still illustrative) version of this method (that I learned from Nets Katz), namely to provide yet another proof of the Szemerédi-Trotter theorem in incidence geometry:

Theorem 2 (Szemerédi-Trotter theorem) Given a finite set of points {P} and a finite set of lines {L} in {{\bf R}^2}, the set of incidences {I(P,L):= \{ (p,\ell) \in P \times L: p \in \ell \}} has cardinality

\displaystyle  |I(P,L)| \ll |P|^{2/3} |L|^{2/3} + |P| + |L|.

This theorem has many short existing proofs, including one via crossing number inequalities (as discussed in this previous post) or via a slightly different type of cell decomposition (as discussed here). The proof given below is not that different, in particular, from the latter proof, but I believe it still serves as a good introduction to the polynomial method in combinatorial incidence geometry.


Let us begin with a trivial bound:

Lemma 3 (Trivial bound) For any finite set of points {P} and finite set of lines {L}, we have {|I(P,L)| \ll |P| |L|^{1/2} + |L|}.

The slickest way to prove this lemma is by the Cauchy-Schwarz inequality. If we let {\mu(\ell)} be the number of points {P} incident to a given line {\ell}, then we have

\displaystyle  |I(P,L)| = \sum_{\ell \in L} \mu(\ell)

and hence by Cauchy-Schwarz

\displaystyle  \sum_{\ell \in L} \mu(\ell)^2 \geq |I(P,L)|^2 / |L|.

On the other hand, the left-hand side counts the number of triples {(p,p',\ell) \in P \times P \times L} with {p,p' \in \ell}. Since two distinct points {p,p'} determine at most one line, one thus sees that the left-hand side is at most {|P|^2 + |I(P,L)|}, and the claim follows.

Now we return to the Szemerédi-Trotter theorem, and apply the cell decomposition with some parameter {D}. This gives a decomposition

\displaystyle  {\bf R}^2 = \{Q=0\} \cup C_1 \cup \ldots \cup C_m

into a curve {\{Q=0\}} of degree {O(D)}, and at most {O(D^2)} cells {C_1,\ldots,C_m}, each of which contains {O(|P|/D^2)} points. We can then decompose

\displaystyle  |I(P,L)| = |I(P \cap \{Q=0\},L)| + \sum_{i=1}^m |I(P \cap C_i,L)|.

By removing repeated factors, we may take {Q} to be square-free.

Let us first deal with the incidences coming from the cells {C_i}. Let {L_i} be the lines in {L} that pass through the {i^{th}} cell {C_i}. Clearly

\displaystyle  |I(P \cap C_i,L)| =|I(P \cap C_i,L_i)|

and thus by the trivial bound

\displaystyle  |I(P \cap C_i,L)| \ll |P \cap C_i| |L_i|^{1/2} + |L_i| \ll \frac{|P|}{D^2} |L_i|^{1/2} + |L_i|.

Now we make a key observation (coming from Bezout’s theorem: each line in {\ell} can meet at most {O(D)} cells {C_i}, because the cells {C_i} are bounded by a degree {D} curve {\{Q=0\}}). Thus

\displaystyle  \sum_{i=1}^m |L_i| \ll D |L|

and hence by Cauchy-Schwarz, we have

\displaystyle  \sum_{i=1}^m |L_i|^{1/2} \ll D^{3/2} |L|^{1/2}.

Putting all this together, we see that

\displaystyle  \sum_{i=1}^m |I(P \cap C_i,L)| \ll D^{-1/2} |P| |L|^{1/2} + D |L|.

Now we turn to the incidences coming from the curve {\{Q=0\}}. Applying Bezout’s theorem again, we see that each line in {L} either lies in {\{Q=0\}}, or meets {\{Q=0\}} in {O(D)} points. The latter case contributes at most {O(D |L|)} incidences, so now we restrict attention to lines that are completely contained in {\{Q=0\}}. The points in the curve {\{Q=0\}} are of two types: smooth points (for which there is a unique tangent line to the curve {\{Q=0\}}) and singular points (where {Q} and {\nabla Q} both vanish). A smooth point can be incident to at most one line in {\{Q=0\}}, and so this case contributes at most {|P|} incidences. So we may restrict attention to the singular points. But by one last application of Bezout’s theorem, each line in {L} can intersect the zero-dimensional set {\{Q=\nabla Q = 0 \}} in at most {O(D)} points (note that each partial derivative of {Q} also has degree {O(D)}), giving another contribution of {O(D |L|)} incidences. Putting everything together, we obtain

\displaystyle  |I(P,L)| \ll D^{-1/2} |P| |L|^{1/2} + D |L| + |P|

for any {D \geq 1}. An optimisation in {D} then gives the claim.

Remark 2 If one used the extreme case of the cell decomposition noted in Remark 1, one only obtains the trivial bound

\displaystyle  |I(P,L)| \ll |P|^{1/2} |L| + |P|.

On the other hand, this bound holds over arbitrary fields {k} (not just over {{\bf R}}), and can be sharp in such cases (consider for instance the case when {k} is a finite field, {P} consists of all the points in {k^2}, and {L} consists of all the lines in {k^2}.)