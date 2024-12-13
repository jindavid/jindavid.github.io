---
layout: post
title: Evaluating Heavy-Tailed Diffusion Models on Heavy-Tailed Datasets with Rare Event Statistics
subtitle : 6.S978 Final Project
tags: [Course Project]
author: David Jin, Kai Chang
comments : True
---

# The Effects of Non-Gaussian Noise in Diffusion Models: A Systematic Study

## Introduction

In the broadest sense, generative modeling concerns the statistical problem of estimating and sampling from an unknown probability measure given samples from the measure. However, when the target measure is high-dimensional, such a task can be extremely difficult, and traditional methods such as Gaussian Mixture Models become computationally intractable easily [BN06]. Arguably, the most empirically successful modern technique for tackling this problem is to identify a mapping from a base measure (which is easy to sample from) to the target measure and approximate the mapping with the given samples instead. Exactly how the mapping is constructed and approximated depends on the modeling choice and can be dramatically different. In particular, various methods based on Deep Neural Networks have been proposed in the past decade, including Variational Auto-Encoders, Generative Adversarial Networks, Normalizing Flows, Denoising Diffusion Probabilistic Models (DDPMs), and Score-Based Diffusion Models (SBMs) [SSDK20], just to name a few.

Notably, SBMs model the mapping from the base measure to the target measure as the reverse stochastic differential equation (SDE) of a pre-specified Ornstein-Uhlenbeck (OU) process. DDPMs can be viewed as a specific type of discretized SBMs. Due to the specific choice, the base measure, with no other options, has to be a standard Gaussian. While such a constraint seems not restrictive for many problems, in the context that the targeting measure possesses heavy-tailed (rare and extreme events) or long-tailed (imbalanced datasets) nature, it has been argued in several recent works that limiting ourselves in OU processes and standard Gaussian base measures might not be the best thing to do. In this project, we aim to provide a comprehensive review on this line of works and provide a systematic comparison in terms of their formulations and empirical performance.

The motivations for us to conduct such a study are the following. First off, some works use the same kind of heavy-tailed distributions but arrive at completely different conclusions. For instance, both [PPX24] and [JMFLK23] use $t$-distributions in their models but draw completely opposite conclusions. Second, works that share certain mathematical similarities have not been compared against each other: while [NSA24] formulates the mapping as a rough-path fractional Brownian Motion, [YPKL23, SSD24] use Lévy processes to model the mapping. Last but not least, for the works that we are considering here, at least in the official paper, the intersection of the benchmarks on which they are tested is an empty set: some of them are tested on image data, and some are tested on climate data.

In summary, we aim to conduct the following systematic comparative studies on these works [DSL22, HSV24, JMFLK23, NRW21, NSA24, PPX24, SSD24, YPKL23]:

1. Review the formulations in reasonable detail for the models proposed in these papers, comment on the similarities shared, and emphasize the differences among them.
2. Identify one or more suitable datasets and conduct extensive experiments to compare the empirical performances against one another.

## References

- **[BN06]** Christopher M. Bishop and Nasser M. Nasrabadi. _Pattern Recognition and Machine Learning_, volume 4. Springer, 2006.
- **[DSL22]** Jacob Deasy, Nikola Simidjievski, and Pietro Liò. _Heavy-tailed denoising score matching_, April 2022. arXiv:2112.09788 [cs, stat].
- **[HSV24]** Xingchang Huang, Corentin Salaun, Cristina Vasconcelos, Christian Theobalt, Cengiz Oztireli, and Gurprit Singh. _Blue noise for diffusion models_. In ACM SIGGRAPH 2024 Conference Papers, SIGGRAPH '24, pages 1–11, New York, NY, USA, July 2024. Association for Computing Machinery.
- **[JMFLK23]** Alexia Jolicoeur-Martineau, Kilian Fatras, Ke Li, and Tal Kachman. _Diffusion models with location-scale noise_, April 2023. arXiv:2304.05907.
- **[NRW21]** Eliya Nachmani, Robin San Roman, and Lior Wolf. _Denoising Diffusion Gamma Models_, October 2021. arXiv:2110.05948 [cs, eess].
- **[NSA24]** Gabriel Nobis et al. _Generative Fractional Diffusion Models_, June 2024. arXiv:2310.17638.
- **[PPX24]** Kushagra Pandey et al. _Heavy-Tailed Diffusion Models_, October 2024. arXiv:2410.14171.
- **[SSD24]** Dario Shariatian et al. _Denoising Lévy Probabilistic Models_, July 2024. arXiv:2407.18609 [cs, stat].
- **[SSDK20]** Yang Song et al. _Score-Based Generative Modeling through Stochastic Differential Equations_, November 2020.
- **[YPKL23]** Eunbi Yoon et al. _Score-based Generative Models with Lévy Processes_, November 2023.
