---
categories:
- research_paper
date: ''
source: "Cand\xE8s, E., Romberg, J., and Tao, T. (2006). 'Robust uncertainty principles:\
  \ exact signal reconstruction from highly incomplete frequency information.' IEEE\
  \ Transactions on Information Theory, 52(2), 489\u2013509."
title: Robust uncertainty principles and compressed sensing
url: ''
---
This paper, published in IEEE Transactions on Information Theory in February 2006,
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
foundations for the field of compressed sensing.
