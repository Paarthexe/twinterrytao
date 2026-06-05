---
title: "Open question: the Mahler conjecture"
source: "terrytao.wordpress.com"
url: "https://terrytao.wordpress.com/2007/03/08/open-question-the-mahler-conjecture/"
date: "2007-03-08"
categories: ["geometry", "convex geometry", "open questions", "expository"]
---
It seems that I have unwittingly started an “open problem of the week” column here; certainly it seems easier for me to pose unsolved problems than to write papers :-) .

This question in convex geometry has been around for a while; I am fond of it because it attempts to capture the intuitively obvious fact that cubes and octahedra are the “pointiest” possible symmetric convex bodies one can create. Sadly, we still have very few tools to make this intuition rigorous (especially when compared against the assertion that the Euclidean ball is the “roundest” possible convex body, for which we have many rigorous and useful formulations).

To state the conjecture I need a little notation. Suppose we have a symmetric convex body B \subset {\Bbb R}^d in a Euclidean space, thus B is open, convex, bounded, and symmetric around the origin. We can define the polar body B^\circ \subset {\Bbb R}^d by

B^\circ := \{ \xi \in {\Bbb R}^d: x \cdot \xi < 1 \hbox{ for all } x \in B \}.

This is another symmetric convex body. One can interpret B as the unit ball of a Banach space norm on {\Bbb R}^d, in which case B^\circ is simply the unit ball of the dual norm. The Mahler volume M(B) of the body is defined as the product of the volumes of B and its polar body:

M(B) := \hbox{vol}(B) \hbox{vol}(B^\circ).

One feature of this Mahler volume is that it is an affine invariant: if T: {\Bbb R}^d \to {\Bbb R}^d is any invertible linear transformation, then TB has the same Mahler volume as B. It is also clear that a body has the same Mahler volume as its polar body. Finally the Mahler volume reacts well to Cartesian products: if B_1 \subset {\Bbb R}^{d_1}, B_2 \subset {\Bbb R}^{d_2} are convex bodies, one can check that

M(B_1 \times B_2) = M(B_1) M(B_2) / \binom{d_1+d_2}{d_1}.

For the unit Euclidean ball B^d one can easily compute the Mahler volume as

M(B^d) = \frac{\Gamma(3/2)^{2d} 4^d}{\Gamma(\frac{d}{2} + 1)^2} = (2\pi e + o(1))^d d^{-d}

while for the unit cube Q^d or the unit octahedron O_d = (Q^d)^\circ the Mahler volume is

M(Q^d) = M(O_d) = \frac{4^d}{\Gamma(d+1)} = (4e + o(1))^d d^{-d} = (\frac{4}{2\pi} + o(1))^d M(B^d).

One can also think of Q^d, B^d, O_d as the unit balls of the l^\infty, l^2, l^1 norms respectively.

The Mahler conjecture asserts that these are the two extreme possibilities for the Mahler volume, thus for all convex bodies B \subset {\Bbb R}^d we should have

M(Q^d) = M(O_d) \leq M(B) \leq M(B^d).

Intuitively, this means that the Mahler volume is capturing the “roundness” of a convex body, with balls (and affine images of balls, i.e. ellipsoids) being the roundest, and cubes and octahedra (and affine images thereof) being the pointiest.

The upper bound was established by Santaló (with the three-dimensional case settled much earlier by Blaschke), using the powerful tool of Steiner symmetrisation, which basically is a mechanism for making a convex body rounder and rounder, converging towards a ball. One can quickly verifies that each application of Steiner symmetrisation does not decrease the Mahler volume, and the result easily follows. As a corollary one can show that the ellipsoids are the only bodies which actually attain the maximal Mahler volume. (Several other proofs of this result, now known as the Blaschke-Santaló inequality, exist in the literature. It plays an important role in affine geometry, being a model example of an affine isoperimetric inequality.) Somewhat amusingly, one can use Plancherel’s theorem to quickly obtain a crude version of this inequality, losing a factor of O(d)^d; more generally, though, I doubt that these sorts of “sharp constant” problems (for which one cannot afford to lose unspecified absolute constants) are amenable to a Fourier-analytic approach.

The lower inequality remains open. In my opinion, the main reason why this conjecture is so difficult is that unlike the upper bound, in which there is essentially only one extremiser up to affine transformations (namely the ball), there are many distinct extremisers for the lower bound – not only the cube and the octahedron, but also products of cubes and octahedra, polar bodies of products of cubes and octahedra, products of polar bodies of… well, you get the idea. It is really difficult to conceive of any sort of flow or optimisation procedure which would converge to exactly these bodies and no others; a radically different type of argument might be needed.

If one is willing to lose some factors in the inequality, then some partial results are known. Firstly, from John’s theorem one trivially gets a bound of the form M(B) \geq d^{-d/2} M(B^d). A significantly deeper argument of Bourgain and Milman, using the theory of cotype (which roughly speaking controls the size of long random sums in a normed vector space), gives a bound of the form M(B) \geq C^{-d} M(B^d) for some absolute constant C; this bound is now known as the reverse Santaló inequality. A slightly weaker “low-tech” bound of M(B) \geq (\log_2 d)^{-d} M(B^d) was given by Kuperberg, using only elementary methods. The best result currently known is again by Kuperberg, who showed that

M(B) \geq (\pi/4)^{d-1} M(Q^d)

using some Gauss-type linking integrals associated to a Minkowski metric in {\Bbb R}^{d+d}.

In another direction, the Mahler conjecture has also been verified for some special classes of convex bodies, such as zonoids (limits of finite Minkowski sums of line segments) and 1-unconditional convex bodies (those which are symmetric around all coordinate hyperplanes).

There seem to be some other directions to pursue. For instance, it might be possible to show that (say) the unit cube is a local minimiser of Mahler volume, or at least that the Mahler volume is stationary with respect to small perturbations of the cube (whatever that means). Another possibility is to locate some reasonable measure of “pointiness” for convex bodies, which is extremised precisely at cubes, octahedra, and products or polar products thereof. Then the task would be reduced to controlling the Mahler volume by this measure of pointiness.

Some time ago I wrote some notes on the more elementary aspects of the above theory; it was intended for my book with Van Vu but eventually got deleted as the book was already too big and getting unfocused.