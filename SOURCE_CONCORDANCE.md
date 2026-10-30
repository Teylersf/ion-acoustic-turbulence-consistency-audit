# Source editions, existing erratum and reading scope

This preflight pairs two queue entries: the one-page 2024 erratum, DOI 10.1017/S0022377824000291, and the original ion-acoustic-turbulence study, arXiv:2309.05563. It does not treat a published correction as an original discovery and does not decide that every inspected issue requires a new publication.

## Identities and existing correction

The supplied original is byte-identical to the official versioned arXiv v2 PDF: 39 pages, 7,124,730 bytes, SHA-256 65abe8f1ed9b23f393b0f21a82ff62a88a80c17fb770b7e73688de1c969bf5d3. Version 1 was submitted 11 September 2023 at 15:49:28 UTC; version 2 was submitted 2 January 2024 at 06:38:44 UTC. The v2 PDF is dated 2 January 2024. Official v1 has 21 pages, 4,085,502 bytes and SHA-256 caf708ac5a8526b160f20977afa154a29c737030bedae50c713a4dd47a4c234e. The abstract page still lists four authors, but the actual v2 PDF already includes Manaure Francisquez as the fifth author; the v1 PDF has four. Abstract metadata must not be substituted for the inspected PDF byline.

The authentic publisher VOR was downloaded normally from Cambridge, with HTTP 200 and no challenge bypass: 39 pages, 3,480,337 bytes, SHA-256 ece6a9ed59a5646d817db11c5468398a281b3704f223e59819f37faf75e29034. The journal article is *A two-dimensional numerical study of ion-acoustic turbulence*, Journal of Plasma Physics 90(1), 965900101, DOI 10.1017/S0022377824000060, published online 2 February 2024. The journal byline is Zhuo Liu, Ryan White, Manaure Francisquez, Lucio M. Milanese and Nuno F. Loureiro. The received, revised and accepted dates are 3 October 2023, 31 December 2023 and 5 January 2024. The VOR is CC BY 4.0.

The supplied erratum is byte-identical to the official Cambridge PDF: one page, 46,063 bytes, SHA-256 2aa9f637c6a841943bfdc41ea7ca25a10b709fb3c6679c84707eab07ddc2c830. It is JPP 90(2), 945900201, published online 4 April 2024, and is CC BY 4.0. Its sole correction removes an accidentally inserted conference phrase from an editorial acknowledgement. It changes no equation, numerical result or scientific conclusion. The current VOR acknowledgement on printed/PDF page 24 already contains the corrected wording. Crossref explicitly links the original via updated-by and the erratum via update-to. The metadata's update date refers to the original article date; it is not substituted for the erratum's independently verified online date.

## Institutional comparison and version changes

The local institutional file is 40 pages, 3,494,569 bytes, SHA-256 c5af7f9f0d4354fb53d23ff08123f84eca1c0894ae64adb25a1cf18c070a9e1f. It has a MIT report cover followed by 39 publisher-styled article pages. All 39 article pages match current VOR text after NFKC and whitespace normalization, removal of the VOR DOI footer, and exclusion of first-page publisher frontmatter. The full pairwise result is recorded in institutional-page-correspondence.json. This is a text comparison, not PDF byte or pixel identity. The cover's historical submission language does not make the body the arXiv manuscript. It is not the standalone erratum and does not append that one-page notice.

Version 2 changes the v1 two-column presentation to a JPP-style manuscript and expands the scientific explanation. Directly inspected differences include the fifth PDF author, a new time-dependent-growth display and Figure 1 comparison, the dedicated linear-theory Appendix A, and numerical-resolution Appendix F. V1's appendices on 1D comparison, distribution fits, EAW dispersion and extremely weak fields become v2 Appendices B–E. These known edition changes are not attributed to the acknowledgement erratum. The v1 comparison is bounded; this reviewer does not claim a separate full 21-page scientific audit of v1.

## Exact equation concordance for focused checking

| Expression | Supplied arXiv v2 PDF page | Current VOR printed/PDF page | Preflight observation |
|---|---:|---:|---|
| External-field kinetic equation (2.2) | 5 | 5 | The external field lacks the displayed species q/m factor; the declared input plus resolved solver source does apply that factor. |
| Time-dependent growth (3.1) | 6 | 7 | Same instantaneous-rate exponential and initial-normalization issue; later analysis must integrate the stated rate. |
| Maxwellian (3.4) | 9 | 9 | Variance is explicitly vT squared. |
| Dispersion relation (3.5), zeta definition | 9 | 10 | Same zeta without square-root-two; this is conditional on the unspecified Gaussian convention for Z. |
| Dielectric (A1) and reduction (A2) | 24 | 24–25 | The retained imaginary-unit prefactor in (A2) requires an algebra check against (A1). |
| Time-dependent growth (E1)–(E2) | 28–29 | 28 | Same doubled quadratic exponent; the following threshold relation must be rederived independently. |
| Threshold relation (E11) and reported value (E12) | 29–30 | 30 | Same formula/value. Correcting the growth display does not automatically require changing the displayed one-quarter coefficient. |
| Reconnection-field normalization, section 5 | 23 | 23 | The two neighboring beta dependencies need a consistent Gaussian-unit derivation. |
| Acknowledgement and input availability | 24 | 24 | VOR contains corrected acknowledgement and real linked input repository. |

Seven relevant VOR pages (5, 7, 10, 23, 25, 28, 30) and the entire erratum were inspected visually. The original reviewer read all 39 supplied v2 pages, including every appendix and reference page. Full-text and numbered-page extractions exist for all acquired PDFs. A separate reviewer is reading the entire VOR; this note does not inflate the first reviewer's targeted VOR inspection into an additional complete VOR reading.

## Available inputs and solver identity

The data statement positively identifies public input files; their availability must be credited. The original ammarhakim GitHub link redirects normally to gkeyllorg/gkyl-paper-inp. All 12 Lua decks and the article README are frozen at directory commit 7209ddbfe432b1826df3aa1f7f9fa7f32053a3af, dated 3 October 2023. All 13 downloaded files independently match Git blob hashes and sizes. The README identifies solver short commit 69f26286dcc7; this resolves in the surviving historical fork liangwang0734/gkyl to 69f26286dcc7640024804ba6b1c5ea16d409f759, tree 770d75a658c55d7b4d1ecd247ab6d4ebacc683a4. Relevant modules are pinned and checked in private scratch. This identifies source, not an exact executable, build flags, local changes or embedded input recovered from raw output.

The deposited Main input includes self-Dougherty collisions, an additive ion source and a small initial tail modification. Weak regularization and seeding are plausible; text inspection does not show that the reported numerical results are wrong. In the named solver revision the source profile is evaluated once at t=0 and then added with default constant time dependence. It is consequently fixed spatial forcing under that clean-source interpretation, not refreshed noise. The same solver multiplies the external field by species charge/mass and uses the Poisson branch when hasMagneticField=false. Detailed locators, conservative source-moment controls, field-energy qualifications and collisionality calculations are in available-input-and-solver-semantics.md and deck-model-controls.json.

The input repository's pinned root README explicitly grants MIT terms, copyright 2012–2020 Ammar Hakim and the Gkeyll Team. Its exact notice must accompany copied decks. The historical solver root README has different research-use language and is not declared MIT; no complete solver source file is included in the public evidence bundle. The arXiv abstract reports its nonexclusive distribution licence; it is not silently replaced by the publisher VOR's CC BY licence.

No target raw-output archive, dispersion-plotting program or compiled executable was identified in the inspected 13-file directory. This bounded directory inventory is not an exhaustive absence claim. No source PDF was altered, no simulation was run, and no external publication or author contact occurred.
