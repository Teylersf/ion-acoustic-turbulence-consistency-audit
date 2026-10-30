# Computational reproduction and scope

Author: Taylor Kalin. This software snapshot contains original exact display-consistency controls, two synthetic explanatory figures, independent source-bound checks and provenance, and thirteen article-linked input files with their upstream MIT notice. It excludes the manuscript, PDF/build files, source PDFs, complete historical solver modules, original simulation outputs and private publishing records. A software publication is not manuscript acceptance or external human peer review.

## Original producer

Use ordinary Python 3 from this directory:

```text
python reproduction/run_audit.py --no-plots
```

Numerical production uses only the standard library. The three numerical outputs were already compared byte for byte in Python 3.12.14 and 3.13.7. To regenerate the two explanatory PNGs, install NumPy 2.3.5 and Matplotlib 3.11.2 from requirements.txt and omit --no-plots. PNG byte identity can depend on plotting/font/runtime versions; the archived PNG bytes themselves are fixed. This publication freeze does not rerun the scientific producer or expand its QA claims.

## Separate existing verifiers

These independent checks require mpmath 1.3.0 in addition to the standard library:

```text
python audit/independent-math/verify_iat_math.py
python audit/producer-independent-review/verify_outputs.py
```

They do not import or execute the producer and do not run a plasma simulation. Their existing receipts record their actual parameters, 80-digit precision, checks and limitations. They write their corresponding result JSON files, so use a disposable checkout when comparing newly generated output with archived hashes. Ordinary Python is required; -O disables assertions and is explicitly rejected by these programs.

The bundled source-copy checker uses only the standard library:

```text
python audit/source-review/verify_integrated_sources.py
```

It checks all 25 source-manifest entries and the exact bytes/recorded Git blob identities of thirteen upstream input files, without Git, network access, PDFs or solver execution. Source PDF and unbundled solver-module hashes remain recorded acquisition identities; this offline check does not freshly rehash absent sources.

## Immutable inventory and rights

The self-excluded computational-artifact manifest records every other bundled file size and SHA256. The published Git commit and software archive identify the complete snapshot, including the manifest itself. Source and third-party notices are preserved byte for byte; no text normalization is applied. The first code snapshot has no manuscript release, tag or DOI supplied by this freeze operation; later publication records are kept outside its computational tree.

LICENSE.md grants MIT terms for Taylor Kalin's original code and CC BY 4.0 for original text/figures. The thirteen upstream input files retain Ammar Hakim/Gkeyll Team copyright and the exact MIT notice under third_party/. Historical solver source has different terms and is not bundled. Attributed third-party works are not relicensed.

The README was expanded administratively after its producer-review snapshot; that does not replace or invalidate the producer, numerical-output or figure hashes. Frozen source/provenance copies and scientific files remain exact. The separate freeze receipt records that documentation-only history explicitly.
