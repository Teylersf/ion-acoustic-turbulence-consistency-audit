# Growth-law and model consistency in driven ion-acoustic turbulence

Author: **Taylor Kalin**. Website: https://taylorkalin.com . ORCID: https://orcid.org/0009-0003-9000-9315 .

This audit pairs Liu and colleagues' *A two-dimensional numerical study of ion-acoustic turbulence*, Journal of Plasma Physics 90, 965900101 (2024), https://doi.org/10.1017/S0022377824000060, with its acknowledgement-only erratum, https://doi.org/10.1017/S0022377824000291 . The supplied original is arXiv:2309.05563v2; the current publisher version was also obtained normally.

The reproducible controls identify a nonintegrated time-dependent growth expression, a nonreproducible literal numerical threshold, and displayed force/dielectric/beta inconsistencies. They retain a valid alternative thermal convention and the article's positive normalization and benchmark evidence. Existing simulation curves are not shown wrong. The article's published erratum is credited as an existing editorial correction.

The computational controls are original mathematical examples. They do not reproduce the source's nonlinear simulations or establish that the deposited input files match every executed run. The real article-linked input decks and documented historical solver revision were identified and checked. The declared Main configuration includes weak self-collisions and fixed spatial source forcing. A conditional initial Poisson-energy contribution is derived without claiming a measured source power or nonlinear heating error.

Numerical reproduction uses only Python's standard library:

```text
python reproduction/run_audit.py --no-plots
```

To regenerate the explanatory figures, install the versions in `requirements.txt` and run without `--no-plots`. The three numerical outputs match between Python 3.12.14 and 3.13.7. Independent derivations and checks remain separate from the producer and are not imported by it. The separate independent high-precision verifiers use mpmath 1.3.0; the numerical producer itself remains standard-library-only. See REPRODUCIBILITY.md for the distinct commands and dependencies. There are 24 exact growth controls, 20 threshold controls, four forcing and five beta cases, tabulated positive controls, and exact Fourier source-energy examples. None is a replacement for the original plasma simulations.

`SOURCE_CONCORDANCE.md` and source-provenance records distinguish the 39-page v2, current journal article, acknowledgement-only erratum and institutional comparison. Third-party input copies retain their upstream MIT notice. Complete historical solver modules and source PDFs are excluded from the software archive. Original code is MIT licensed; original audit text and figures are CC BY 4.0; third-party rights remain separate.

The manuscript and its eventual publication records are separate from the computational snapshot. A software archive or public preprint does not establish journal acceptance or external human peer review.

Taylor Kalin self-funds this work. AI systems assist source comparison, mathematical checks, programming and drafting. Internal independent checks are distinct from external human peer review.
