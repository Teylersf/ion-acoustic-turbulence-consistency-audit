# Independent mathematical audit: current-driven ion-acoustic turbulence

Target: Liu, White, Francisquez, Milanese and Loureiro, *A two-dimensional numerical study of ion-acoustic turbulence*, **Journal of Plasma Physics 90**, 965900101 (2024), DOI **10.1017/S0022377824000060**, and the one-page erratum **10.1017/S0022377824000291**.

## Scope and source reading

All 39 pages of the official current VOR were read, including every appendix, caption, qualification and reference, together with the complete one-page erratum. Seven key VOR pages (5, 7, 10, 23, 25, 28 and 30) were inspected in full-page pixels. The corresponding v2 author-TeX displays were checked. The public `Main.lua` was read, and the source/version reviewer independently handles the full edition concordance and solver-deposit provenance.

Independently rehashed local evidence:

| Artifact | SHA-256 |
|---|---|
| Current 39-page VOR | `ece6a9ed59a5646d817db11c5468398a281b3704f223e59819f37faf75e29034` |
| One-page erratum | `2aa9f637c6a841943bfdc41ea7ca25a10b709fb3c6679c84707eab07ddc2c830` |
| v2 author TeX | `a7a5f1ead913eaebd8bc2c793693bd8b5083d9c2459a4061fd3b90e96da710a2` |
| Public `Main.lua` | `940969dfec824be5ec9244d50cb2e9d7f25642eedda3fe033d3e69c4831b84e6` |

The erratum corrects an editorial acknowledgement phrase. The current VOR p.24 already has the corrected wording. It does not claim a scientific correction, and it should not be portrayed as an admission concerning the mathematical points below.

The standalone original program `verify_iat_math.py` imports no source program, other verifier or simulation output. It runs offline with standard-library exact rational arithmetic and mpmath at 80 decimal digits. It tests displays and controlled scalar limits; it does not reproduce a Vlasov simulation, a diagnostic curve, or the actual dispersion-root routine used by the authors.

## Assessment

The most defensible findings are a nonintegrated time-dependent growth formula, a nonreproducible literal numerical threshold, and a stray imaginary prefactor in a stated dielectric-function reduction. The species-forcing coefficient and the final beta scaling also have identifiable displayed inconsistencies. Recognizable transcription or normalization problems are strong benign explanations. The public input supplies a physical external field with correct opposite charges and masses, so an implemented forcing error is not demonstrated.

Two attractive but stronger allegations should be excluded: the Maxwellian expression has an exact alternative plasma-dispersion-function convention; and the temperature discussion does not establish use of a raw rather than central second moment. The source's tabulated weak-field normalization, saturation-energy numbers and empirical duration algebra pass direct controls. No invalidation of its reported nonlinear regimes follows from this audit.

## 1. Time-dependent growth: Eqs. (3.1), (E1) and (E2)

VOR p.6 defines the instability rate through conventional linear theory. On p.7 it assumes

\[
\gamma(t,k)\simeq\gamma(t_0,k)t/t_0=a t.
\]

For wave energy, the instantaneous growth equation is

\[
\frac{d\log W}{dt}=2\gamma(t,k),\qquad
\frac{W(t)}{W(t_0)}=\exp\!\left[a(t^2-t_0^2)\right].
\]

Printed (3.1) instead substitutes the instantaneous rate into the constant-rate expression, giving `W(t0)*exp(2*a*t^2)`. Its logarithmic derivative is `4*a*t`, twice the required one. It also fails its own `W(t0)` anchor for positive `t0`. Absorbing a constant into an arbitrary prefactor could repair the anchor but cannot repair the factor of two in the time-dependent derivative.

Appendix (E1), p.28, likewise gives

\[
\gamma(t)=a t,\qquad
a=k\sqrt{\frac{\pi m_e}{8m_i}}\frac{eE_{\rm ext}}{m_e},
\]

while (E2) prints `W0*exp(2*a*t^2)`. Direct integration from zero gives `W0*exp(a*t^2)`. This is the same error. Interpreting W as a field amplitude rather than energy would not rescue the display: its coefficient would then be `a/2`, not `2*a`, and the article repeatedly identifies W as wave energy.

Eighteen rational growth cases are checked against independent high-precision quadrature of `2*gamma(t)`, with four constant-rate positive controls. These establish the formula discrepancy. They do not identify the formula actually used to draw the black dashed curve in Fig.1 or quantify its fitting error. The author-provided input decks do not supply that postprocessing calculation.

## 2. The threshold chain: a positive algebra control and a numerical mismatch

Do not call printed (E11), p.30, an independently erroneous trapping reduction. Using the **correct integrated energy law**, and keeping the displayed half-width in (E6), the saturation and trapping estimates (E3), (E7)–(E10) give exactly the printed `1/4` prefactor in (E11). Propagating the literal factor-two exponent in (E2) would instead produce `1/2`. Thus (E11) is consistent with the repaired growth law, which is a useful internal positive result.

Let `r=mi/me`, `q=W0/(n0*Te0)` and

\[
S=\frac{E_{\rm ext}^2}{8\pi n_0T_{e0}}\,r
 =\frac r2\widetilde E_{\rm ext}^{\,2}.
\]

The last identity follows directly from `lambda_De^2=Te0/(4*pi*n0*e^2)` and the source's field normalization, so it does not involve a hidden c or thermal-speed convention. Literal equality in printed (E11) is

\[
\log\left(\frac{\sqrt S}{q}\right)
= C S^{-1/4},\qquad C=\frac14\sqrt{\frac\pi8}.
\]

It has a unique root in the physical branch `sqrt(S)>q`. An independent closed form follows by setting `x=S^(1/4)`:

\[
x=\frac{C}{2W\!\left(C/(2\sqrt q)\right)},\qquad
\widetilde E_{\rm crit}=\sqrt{\frac2r}\,x^2,
\]

where W here is the principal Lambert function, not wave energy. A separate 260-step monotone bisection agrees with the closed form to relative error below `1e-68` in all 12 tested mass-ratio/noise cases.

For the values explicitly stated beside (E12), `r=25` and `q=1e-8`, the root is

\[
\widetilde E_{\rm crit}=6.81838750469781469\times10^{-5}.
\]

The printed value `5.6e-4` instead gives

\[
\text{LHS}=12.1959712919,\qquad \text{RHS}=3.52085739124.
\]

If the literal (E2) exponent is propagated, the alternative root is `2.19105893484557380e-4`, which also does not reproduce (E12). With the printed (E11) prefactor, reproducing (E12) would require noise `q=5.85536667854e-5`, rather than the stated `1e-8`.

**Strong benign qualification:** these trapping and saturation relations contain order-one conventions. Increasing the approximate trapping width by just **1.86116115367** multiplies the right side by **3.46392083992** and reconciles the printed field at the stated noise. Consequently the rigorous statement is that the quoted numerical calculation is not reproducible from its literal displayed prefactors and inputs. It is not a universally corrected physical threshold. It does not falsify the observed classification of M25E1 or M25E2 as extremely weak-field runs. Unknown noise amplitude, spectral mode allocation and trapping-width conventions materially limit such an inference.

## 3. Appendix (A1) to (A2): the imaginary factor must cancel

With k aligned along z, the actual integrand factor obeys

\[
\frac{i k}{p+i k v_z}=\frac1{v_z-i p/k}.
\]

Therefore the `i` outside the integral in (A1), p.24, cancels while rewriting its denominator. Printed (A2), p.25, retains that `i`, despite defining F as the ordinary one-dimensional velocity distribution. Eighteen exact complex-rational controls verify the cancellation. No choice of the thermal Gaussian normalization can restore the extra prefactor while preserving the same stated (A1).

A controlled cold-plasma limit makes the difference transparent. With a stationary delta distribution, the consistent reduction gives `epsilon=1+omega_p^2/p^2`; its roots are the purely oscillatory `p=+/-i*omega_p`. Printed (A2) gives `epsilon=1+i*omega_p^2/p^2`. Evaluated at either correct root it equals `1-i`, not zero. Six cold-limit controls pass exactly.

This is a displayed algebraic error, plausibly a stray character. It is not evidence that the authors' actual linear root computation used that character. Their separate linear benchmarks in Appendix F are positive evidence against assuming that the implemented calculation was literally the defective display.

## 4. Physical forcing in (2.2), and what the public deck actually shows

VOR p.5 prints the same external `Eext` directly as an acceleration for both species while retaining `q_alpha/m_alpha` on the self-consistent electric field. Elsewhere Eext is a physical electric field with a Gaussian field normalization. A consistent dimensional equation uses

\[
\frac{q_\alpha}{m_\alpha}
\left(\boldsymbol E_{\rm ext}-\nabla\varphi\right).
\]

For uniform initially resting singly charged species, the physical current derivative is

\[
\dot J=n_0e^2E_{\rm ext}\left(\frac1{m_e}+\frac1{m_i}\right).
\]

If both species receive the literal same acceleration, their relative velocity and net current derivative are zero. Five exact mass-ratio controls demonstrate this distinction. The paper's electron-only free-current formula on p.6 is a good approximation to the physical expression: its neglected correction is only `me/mi`, one percent for run Main.

The public `Main.lua` supplies `ExternalField=-5e-5`, electron charge/mass `-1/1`, and ion charge/mass `+1/100`. This is a physical-field specification with species coupling, not a common species-independent acceleration. The displayed omission must therefore not be promoted into an implemented forcing error. An unstated species-dependent acceleration normalization could make an individual term numerical, but it would need an explicit definition to coexist with the paper's single physical Eext and current-rate equation.

The source/version reviewer also identifies weak self-collision operators and a source/seed in the public deck; these are not displayed in (2.2). `Main.lua` has `nu_ee=1e-4`, `nu_ii=2e-5`, with cross-collisions disabled. Over its nominal `tEnd=5000`, the dimensionless products are 0.5 and 0.1. These numbers alone neither establish negligible long-time effects nor demonstrate an error in the reported heating. Momentum/energy-conserving self-collisions do not directly create interspecies resistivity; regularization sensitivity would need a separate controlled study. The declared solver revision evaluates the source profile once, according to the independent provenance review, so the apparent time-dependent Lua profile must not be called white-in-time forcing. Exact executed-binary identity remains unverified.

### 4.1. Conditional electrostatic work from a zero-mean source

Zero global source moments do not imply zero electrostatic work. Under a periodic, self-adjoint Poisson closure, with mean-zero charge perturbation and a consistent gauge,

\[
U=\frac12\langle\rho\varphi\rangle,
\qquad \dot U_{\rm source}=\langle\varphi S_\rho\rangle.
\]

The two terms in the differentiated energy are equal by self-adjointness; there is no extra one-half on the last expression. For an ion source `S_i=noise*G(x)*M_i(v)` and an initial perturbation `delta_f_i=perturbation*G(x)*M_i(v)`, the same G and Maxwellian imply

\[
S_\rho=\frac{\mathrm{noise}}{\mathrm{perturbation}}\delta\rho_0,
\qquad
\dot U_{\rm source}(0)=2\frac{\mathrm{noise}}{\mathrm{perturbation}}U_0.
\]

The input values `noise=1e-6`, `perturbation=1e-4` yield the conditional initial logarithmic rate **0.02** in `omega_pe=1` units. In contrast, integrating any fixed velocity moment of this separable source over space gives zero when G is a sum of nonzero periodic Fourier modes. Thus zero globally injected particles, momentum and particle kinetic energy are compatible with nonzero field-energy work.

Nine independent exact rational Fourier cases verify the field-energy identity, including aligned, absent and anti-aligned sources; three orthogonal-mode controls give zero work. These are initial continuum controls. They are not a measured power in the author's run, and do not show that the noise source dominates the instability. Later `mean(phi(t)*S_rho)` need not have the same sign or the same proportionality to U. The public input invokes a Vlasov–Maxwell/electrostatic-field interface; its precise source/Gauss-law treatment, initialization and outputs would need inspection before transferring this Poisson identity to a discrete energy budget. The strongest supported request is to disclose and check the source contribution, not to infer a nonlinear heating error from its coefficient alone.

## 5. Final reconnection-field normalization

The conclusion on p.23 gives a ratio proportional to `1/beta_e` and then a normalized reconnection field proportional to `beta_e`. These cannot both follow from the same preceding definitions except at beta one. In Gaussian units with conventional `beta_e=8*pi*n0*Te/B0^2`,

\[
E_{\rm rec}=\gamma V_A B_0/c,\qquad
\frac{E_{\rm rec}}{4\pi en_0\lambda_{De}}
=\frac{2\gamma}{\beta_e}\sqrt{\frac{m_e}{m_i}}\frac{v_{Te}}c.
\]

Combining this expression with the positively checked (2.1) normalization yields

\[
\frac{E_{\rm rec}}{E_{\rm NL}}
=\frac{12\pi\gamma}{\beta_e}\frac{v_{Te}}c
\sqrt{\frac{m_i}{m_e}}\frac{T_i}{T_e},
\]

which agrees with the conclusion's preceding ratio for `gamma=.1`. Its subsequent `2*gamma*beta_e` factor should instead be inverse-beta under that convention. The introductory `Erec~gamma*VA*B0` also omits the Gaussian c that reappears in the normalized formulas. Three beta controls show that the printed-to-consistent ratio is `beta_e^2`.

This is a notation/scaling inconsistency in the illustrative astrophysical estimate. At beta one the factors coincide. Because the numerical example does not specify all plasma parameters, the quoted `5e-5` is not independently disproved here, and the conclusion about temporal opportunity for IAT is not quantitatively overturned by this algebra alone.

## 6. Exact benign thermal convention for (3.5)

Equation (3.4), p.9, uses a Gaussian of variance `vT^2`, while (3.5), p.10, states `zeta=(omega-ku)/(k*vT)`. With the usual Fried–Conte function, the familiar argument is divided by sqrt(2). But the article does not explicitly give the defining Gaussian integral of Z. There is an exact legitimate rescue:

\[
Z_\sigma(\zeta)=\frac1{\sqrt{2\pi}}
\int\frac{e^{-s^2/2}}{s-\zeta}\,ds
=\frac1{\sqrt2}Z_{\rm FC}(\zeta/\sqrt2).
\]

Then `1+zeta*Zsigma(zeta)` with the stated Debye length is precisely the Maxwellian susceptibility. Four independent upper-half-plane Gaussian derivative integrals agree with this expression to about `1e-81`; inserting the unrescaled Fried–Conte function instead does not agree. Thus the correct classification is an unspecified plasma-dispersion-function convention, conditional on the intended Z definition, not an unconditional missing-sqrt(2) error or evidence of wrong plotted roots.

Likewise, explicit bulk/tail population weights can consistently accompany Debye lengths based on a common total-electron plasma frequency. The prose's species labels do not unambiguously establish component-density double counting. No such error is asserted.

## 7. Temperature interpretation and retained controls

The paper explicitly notes non-Maxwellian distributions and explains on p.20 that accelerating the tail broadens the total electron distribution. A kinetic central second moment remains a well-defined temperature/pressure even for non-Maxwellians. For a two-Maxwellian mixture,

\[
\operatorname{Var}(v)=(1-\alpha)\sigma_b^2+\alpha\sigma_t^2
+\alpha(1-\alpha)(u_b-u_t)^2.
\]

Nine exact controls verify this identity and invariance under a common boost. They show why relative-population drift broadening need not demonstrate irreversible heating, while also showing why it can legitimately increase a central variance. The public deck requests `intM2Thermal`; no raw-second-moment implementation or failure to subtract the mean drift is demonstrated. Distinguishing local pressure from the variance of a spatially averaged distribution would need the actual diagnostic/postprocessing definition. This is an interpretation/reproducibility limit, not an additional proved numerical error.

Positive checks:

- All **11 Table1** values follow `ENL/Eunit=(Te0/Ti0)/(6*pi*r)` to their displayed precision.
- All **five Table2** theoretical saturation values follow `Wsat/(n0*Te0)=Etilde*sqrt(r/2)` to their printed precision; Appendix (E3) is the same normalization.
- `28.6/sqrt(2)=20.223...` supports the rounded coefficient 20.2 in (4.6).
- Equation (4.7) gives `tau_res*omega_pe=2025` for Main with theta ten, agreeing with the quoted roughly 2000. This is a consistency check of an empirical fit, not an independent prediction from first principles.
- The source supplies a 1D/2D comparison, linear benchmarks, and nonlinear resolution tests, and explicitly acknowledges the finite box, unresolved short modes in M200E10, non-Maxwellian stability limitations and the lack of an ultimate steady state. Those qualifications are credited.
- Main's supplied grid and polynomial order provide a plausible degrees-of-freedom interpretation of the stated resolution, rather than proving a factor-three resolution error: velocity-cell widths divided by three give about 0.0208 and 0.0417 times the electron thermal speed, matching the quoted 0.021/0.042. This is a convention-based reconciliation, not an assertion that DG nodal spacing is literally uniform.

The audit supports a bounded technical clarification of printed growth/normalization algebra. It supplies neither a new nonlinear IAT theory nor evidence that the source's qualitative stages, anomalous resistivity shutdown, or numerical figures are false. No production project, manuscript, Git change, DOI deposit, queue edit or publication action was performed.
