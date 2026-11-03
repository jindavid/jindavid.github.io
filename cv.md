---
layout: cv
title: CV
description: David Jin's education, research, experience, software, publications, talks, and teaching.
---
# Curriculum vitae

<p class="cv-download"><a href="{{ '/assets/pdf/David-Jin-CV.pdf' | relative_url }}" download="David-Jin-CV.pdf">Download CV (PDF)</a></p>

**David Jin**  
[jindavid.me](https://jindavid.me) · [GitHub](https://github.com/jindavid)

51 Vassar St, Building 45, Room 421G, Cambridge, MA 02139

## Education

### Massachusetts Institute of Technology
Cambridge, MA · May 2027 (expected)

M.S./Ph.D. in Computational Science and Engineering · GPA: 5.0/5.0  
Advisors: Sungho Shin and Yoon Kim  
**Amazon AI Fellow, 2025–2027**

### California Institute of Technology
Pasadena, CA · June 2022

B.S. in Information and Data Science · GPA: 4.2/4.3

### Grinnell College
Grinnell, IA · May 2021

B.A. in Physics · GPA: 4.0/4.0  
**Barry Goldwater Scholar, 2021–2022**

## Research interests

GPU computing, numerical optimization, and efficient machine learning.

## Professional experience

### Jump Trading
Quantitative Researcher Intern · New York, NY · May–August 2026

Designed and implemented GPU-accelerated algorithms for large-scale portfolio optimization.

### Argonne National Laboratory
Research Intern · Lemont, IL · June–September 2025

Developed a distributed optimization framework across multiple supercomputers with heterogeneous architectures, including Aurora and Frontier.

### Symbotic
Machine Learning Intern · Wilmington, MA · June–August 2024

Built a training pipeline for pose and shape estimation for large-scale multi-robot systems (more than 1,000 robots) in automated warehouses.

## Open-source software

### [BlockDSS.jl](https://github.com/MadNLP/BlockDSS.jl)
Creator, contributor, and maintainer · 2024–present

- Developed GPU-accelerated direct solvers for structured linear systems, including block-tridiagonal systems.
- Benchmarked against MA57, CHOLMOD, and cuDSS, demonstrating 20–50× speedups over CPU methods on large-scale problems.
- Integrated with Julia's scientific computing and optimization ecosystem, including MadNLP.

### [OpenMatch](https://github.com/thunlp/OpenMatch)
Contributor · 2021–2022

- Contributed implementations of neural information retrieval models and support for building customized retrieval systems.
- Reproduced results on widely used information retrieval benchmarks.

## Publications

### Manuscripts

{% bibliography --query @*[status=preprint] %}
{% bibliography --query @*[status=submitted] %}

### Conference and journal publications

{% bibliography --query @*[status=published] %}

## Talks

- **GPU-Accelerated Solution of Block-Tridiagonal Systems for Large-Scale Optimization.** IFAC World Congress, August 2026, Busan, South Korea.
- **GPU-Accelerated Solution of Block-Tridiagonal Systems for Large-Scale Optimization.** SIAM Parallel Processing, March 2026, Berlin, Germany.
- **GPU-Accelerated Solution of Block-Tridiagonal Systems for Large-Scale Optimization.** AIChE Annual Meeting, November 2025, Boston, USA. **Plenary talk.**
- **Multi-Model 3D Registration: Finding Multiple Moving Objects in Cluttered Point Clouds.** ICRA, May 2024, Yokohama, Japan.
- **Emulating Ray Tracing Using Machine Learning.** Joint Mathematics Meeting, January 2021, online (Washington, DC).
- **Laminar Chaos in an Electronic Mackey-Glass Variable Time Delay System.** APS March Meeting, March 2020, Denver, CO. Canceled.
- **The Effects of Gaps on the Correlation Dimension of Nonlinear Systems.** Midstates Consortium for Math and Science, November 2018, Washington University in St. Louis, St. Louis, MO.

## Teaching

### Massachusetts Institute of Technology
Teaching Assistant

- Numerical Computation for Mechanical Engineers · Fall 2022

### California Institute of Technology
Teaching Assistant

- Statistical Inference · Spring 2022
- Machine Learning and Data Mining · Winter 2022
- Foundations of Machine Learning and Statistical Inference · Winter 2022
- Introduction to Probabilistic Models · Fall 2021

### Grinnell College
Teaching Assistant

- General Physics I · Spring 2020
- Modern Physics · Fall 2019
- Classical Mechanics · Spring 2019
- General Physics I · Fall 2018
