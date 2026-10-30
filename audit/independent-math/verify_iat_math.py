"""Independent source-bound algebra and scalar controls for IAT displays.

No source solver, other verifier, simulation output or network is used. Rational
identities use Fraction. Transcendental controls use mpmath at 80 decimal digits.
This verifies printed formulas/conditional conventions, not the source figures.
"""
from fractions import Fraction as Q
from pathlib import Path
import hashlib,json,math,platform,sys
import mpmath as mp

ROOT=Path(__file__).resolve().parent
mp.mp.dps=80

def M(x):
    if isinstance(x,Q):return mp.mpf(x.numerator)/x.denominator
    return mp.mpf(x)
def pack(x):
    if isinstance(x,Q):return str(x)
    if isinstance(x,mp.mpf):return mp.nstr(x,70)
    if isinstance(x,mp.mpc):return {'real':mp.nstr(x.real,70),'imag':mp.nstr(x.imag,70)}
    if isinstance(x,dict):return {k:pack(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [pack(v) for v in x]
    return x
def ca(a,b):return (a[0]+b[0],a[1]+b[1])
def cn(a):return (-a[0],-a[1])
def cm(a,b):return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def cd(a,b):
    norm=b[0]**2+b[1]**2
    return ((a[0]*b[0]+a[1]*b[1])/norm,(a[1]*b[0]-a[0]*b[1])/norm)

def dielectric_reduction():
    rows=[];i=(Q(0),Q(1));one=(Q(1),Q(0))
    for p in [(Q(1,2),Q(1,3)),(Q(2),Q(-1)),(Q(3,5),Q(0))]:
        for k in [Q(1,2),Q(2)]:
            for v in [Q(-2),Q(1,3),Q(2)]:
                numerator=cm(i,(k,Q(0)))
                left=cd(numerator,ca(p,(Q(0),k*v)))
                right=cd(one,ca((v,Q(0)),cn(cd(cm(i,p),(k,Q(0))))))
                assert left==right
                rows.append({'p':p,'k':k,'v':v,'A1_integrand_factor':left,'correct_reduced_factor':right})
    cold=[]
    for omega in [Q(1,2),Q(1),Q(2)]:
        for sign in [-1,1]:
            p=(Q(0),sign*omega);p2=cm(p,p)
            correct=ca(one,cd((omega**2,Q(0)),p2))
            printed=ca(one,cd((Q(0),omega**2),p2))
            assert correct==(0,0) and printed==(1,-1)
            cold.append({'omega_p':omega,'p':p,'correct_epsilon':correct,'printed_A2_epsilon':printed})
    return {'exact_integrand_cases':rows,'cold_limit_controls':cold,
      'identity':'i*k/(p+i*k*v)=1/(v-i*p/k); the prefactor i cancels.',
      'cold_limit':'Correct epsilon=1+omega_p^2/p^2; literal A2=1+i*omega_p^2/p^2.',
      'scope':'Displayed reduction only; no claim about the root routine used for Figures12/15/18.'}

def growth_controls():
    rows=[]
    for a in [Q(1,100),Q(1,7),Q(2,3)]:
        for t0 in [Q(0),Q(1),Q(3,2)]:
            for dt in [Q(1,2),Q(2)]:
                t=t0+dt
                exponent=a*(t*t-t0*t0)
                integral=mp.quad(lambda z:2*M(a)*z,[M(t0),M(t)])
                assert abs(integral-M(exponent))<mp.mpf('1e-75')
                # Correct log derivative=2*a*t; printed 2*a*t^2 gives4*a*t.
                residual=4*a*t-2*a*t
                assert residual==2*a*t and residual>0
                rows.append({'a':a,'t0':t0,'t':t,'correct_log_energy_ratio':exponent,
                  'literal_printed_log_factor':2*a*t*t,'printed_ODE_log_residual':residual})
    constant=[]
    for gamma in [Q(1,5),Q(3,4)]:
        for dt in [Q(1),Q(3)]:
            assert 2*gamma*dt==Q(2)*gamma*dt
            constant.append({'constant_gamma':gamma,'elapsed_time':dt,'log_energy_ratio':2*gamma*dt})
    return {'time_dependent_cases':rows,'constant_growth_positive_controls':constant,
      'correct_law':'W(t)/W(t0)=exp[a*(t^2-t0^2)] for gamma(t)=a*t and Wdot=2*gamma*W.',
      'E11_bridge':{'correct_energy_growth_multiplier':Q(1),'literal_E2_multiplier':Q(2),
        'E6_fraction':Q(1,2),'correct_RHS_prefactor_excluding_sqrt_pi_over8':Q(1,4),
        'RHS_from_literal_E2':Q(1,2)},
      'important_positive':'The printed E11 1/4 coefficient follows from repaired integrated growth plus the displayed E6/E10 conventions.'}

def threshold_root(r,noise,C):
    # Set x=S^(1/4), S=r*Etilde^2/2. The equation is
    # 2*x*log(x/sqrt(noise))=C, with unique physical root x>sqrt(noise).
    x=C/(2*mp.lambertw(C/(2*mp.sqrt(noise))))
    exact=mp.sqrt(2/r)*x*x
    def f(E):
        S=r*E*E/2
        return mp.log(mp.sqrt(S)/noise)-C*S**(-mp.mpf(1)/4)
    lo=noise*mp.sqrt(2/r);hi=mp.mpf(1)
    assert f(lo)<0<f(hi)
    for _ in range(260):
        middle=(lo+hi)/2
        if f(middle)>0:hi=middle
        else:lo=middle
    bisection=(lo+hi)/2
    assert abs((exact-bisection)/exact)<mp.mpf('1e-68')
    assert abs(f(exact))<mp.mpf('1e-70')
    return exact

def threshold_controls():
    C=mp.sqrt(mp.pi/8)/4;rows=[]
    for r in [25,100,1836]:
        for noise in [mp.mpf('1e-4'),mp.mpf('1e-6'),mp.mpf('1e-8'),mp.mpf('1e-10')]:
            root=threshold_root(mp.mpf(r),noise,C)
            rows.append({'mass_ratio':r,'W0_over_nTe':noise,'E11_literal_critical_Etilde':root})
    r=mp.mpf(25);E=mp.mpf('5.6e-4');noise=mp.mpf('1e-8');S=r*E*E/2
    lhs=mp.log(mp.sqrt(S)/noise);rhs=C*S**(-mp.mpf(1)/4)
    needed_noise=mp.sqrt(S)*mp.exp(-rhs)
    prefactor_ratio=lhs/rhs
    repaired=threshold_root(r,noise,C)
    from_printed_E2=threshold_root(r,noise,2*C)
    # Order-one trapping-width sensitivity is a real benign counterargument.
    # A width multiplier b multiplies the threshold RHS by b^2.
    width_multiplier=mp.sqrt(prefactor_ratio)
    assert abs(threshold_root(r,noise,C*width_multiplier**2)-E)<mp.mpf('1e-70')
    return {'normalization':'Eunit^2=4*pi*n0*Te0; S=(r/2)*Etilde^2.',
      'root_method':'Independent monotone260-step bisection and LambertW closed form agree to relative1e-68.',
      'literal_roots':rows,'claimed_E12':E,'claimed_noise':noise,'at_claimed_E12':{'S':S,'E11_lhs':lhs,'E11_rhs':rhs,'lhs_minus_rhs':lhs-rhs},
      'root_of_printed_E11_for_claimed_parameters':repaired,
      'root_if_literal_printed_E2_propagated':from_printed_E2,
      'noise_required_for_claimed_E12_with_literal_E11':needed_noise,
      'RHS_coefficient_multiplier_required':prefactor_ratio,
      'trapping_width_multiplier_that_reconciles_claim':width_multiplier,
      'physical_limit':'All trapping/saturation estimates use order-one conventions; these roots test the displayed numerical calculation, not a universal nonlinear threshold or refutation of observed runs.'}

def ZFC(z):return 1j*mp.sqrt(mp.pi)*mp.exp(-z*z)*mp.erfc(-1j*z)
def maxwellian_convention_controls():
    rows=[]
    for sigma in [mp.mpf('0.7'),mp.mpf('1.2')]:
        for drift in [mp.mpf('-0.2'),mp.mpf('0.3')]:
            phase=mp.mpc('0.4','0.8')
            F=lambda v:mp.exp(-(v-drift)**2/(2*sigma*sigma))/(mp.sqrt(2*mp.pi)*sigma)
            direct=mp.quad(lambda v:-(v-drift)/(sigma*sigma)*F(v)/(v-phase),[-mp.inf,drift,mp.inf])
            zeta=(phase-drift)/sigma
            normalized_Z=ZFC(zeta/mp.sqrt(2))/mp.sqrt(2)
            repaired=-(1+zeta*normalized_Z)/(sigma*sigma)
            literal_standard=-(1+zeta*ZFC(zeta))/(sigma*sigma)
            assert abs(direct-repaired)<mp.mpf('1e-65')
            assert abs(direct-literal_standard)>mp.mpf('1e-5')
            rows.append({'sigma':sigma,'drift':drift,'phase_velocity':phase,
              'direct_Gaussian_derivative_integral':direct,'variance_one_Z_form':repaired,
              'rescue_absolute_error':abs(direct-repaired),'error_if_unrescaled_Fried_Conte_Z_used':abs(direct-literal_standard)})
    return {'cases':rows,'classification':'Normalization ambiguity, not an unconditional error.',
      'benign_rescue':'Zsigma(z)=ZFC(z/sqrt(2))/sqrt(2) makes3.4/3.5 exactly consistent.',
      'Debye_qualification':'Common total-electron plasma frequency with explicit bulk/tail weights is consistent; component-density double counting is not established.'}

def forcing_beta_and_thermal():
    forcing=[]
    for r in [25,50,100,200,1836]:
        E=Q(1,400);n=Q(1);e=Q(1);me=Q(1);mi=Q(r)
        physical=n*e*e*E*(1/me+1/mi)
        literal=n*e*(E-E)
        assert literal==0 and physical>0
        forcing.append({'mass_ratio':r,'physical_Jdot':physical,'literal_common_acceleration_Jdot':literal,
                        'ion_correction_relative_to_electron_only':Q(1,r)})
    beta=[]
    for value in [Q(1,4),Q(1),Q(4)]:
        correct=1/value;printed=value
        beta.append({'beta_e':value,'correct_normalized_beta_factor':correct,'printed_conclusion_beta_factor':printed,
                     'printed_over_correct':value*value})
    thermal=[]
    for alpha in [Q(1,4),Q(1,2),Q(3,4)]:
        for du in [Q(0),Q(1),Q(3)]:
            ub=Q(1,3);ut=ub+du;sigma_b2=Q(1);sigma_t2=Q(2)
            mean=(1-alpha)*ub+alpha*ut
            raw=(1-alpha)*(sigma_b2+ub*ub)+alpha*(sigma_t2+ut*ut)
            central=raw-mean*mean
            split=(1-alpha)*sigma_b2+alpha*sigma_t2+alpha*(1-alpha)*du*du
            assert central==split
            boost=Q(7,5)
            boosted_raw=(1-alpha)*(sigma_b2+(ub+boost)**2)+alpha*(sigma_t2+(ut+boost)**2)
            assert boosted_raw-(mean+boost)**2==central
            thermal.append({'alpha':alpha,'relative_drift':du,'central_variance':central,
                            'component_drift_variance':alpha*(1-alpha)*du*du,'uniform_boost_invariant':True})
    return {'forcing':forcing,'forcing_scope':'Printed2.2 lacks species q/m on physical Eext; public Main.lua supplies physical ExternalField and opposite species charges, so no implemented forcing error is inferred.',
      'beta':beta,'correct_Gaussian_relation':'Erec/Eunit=(2*gamma/beta_e)*sqrt(me/mi)*(vTe/c); Erec physical Gaussian units=gamma*VA*B0/c.',
      'internal_positive':'Dividing corrected Erec/Eunit by ENL/Eunit gives12*pi*gamma/beta_e*(vTe/c)*sqrt(mi/me)*(Ti/Te), agreeing with the preceding conclusion ratio atgamma=.1.',
      'mixture_variance':thermal,'thermal_scope':'Kinetic variance is defined for non-Maxwellians; mixture-drift broadening need not be irreversible heating. Public deck asks for intM2Thermal, so a raw-second-moment implementation error is not established.'}

def source_energy_controls():
    # Rational Fourier coefficients; -Delta phi=rho absorbs the fixed Poisson
    # coefficient into the units. Uniform background charge is projected out.
    def cosine(k,amplitude):return {k:amplitude/2,(-k[0],-k[1]):amplitude/2}
    def inner(a,b):return sum((v*b.get((-k[0],-k[1]),Q(0)) for k,v in a.items()),Q(0))
    rows=[]
    for harmonics in [[((1,0),Q(1))],[((1,0),Q(1)),((0,2),Q(-1,3))],
                      [((1,0),Q(1)),((0,2),Q(-1,3)),((1,2),Q(2))]]:
        G={k:v for wave,amplitude in harmonics for k,v in cosine(wave,amplitude).items()}
        assert (0,0) not in G
        perturb=Q(1,10000);noise=Q(1,1000000)
        rho={k:perturb*v for k,v in G.items()}
        phi={k:v/(k[0]**2+k[1]**2) for k,v in rho.items()}
        U=inner(rho,phi)/2;assert U>0
        for sign in [-1,0,1]:
            S={k:sign*noise*v for k,v in G.items()}
            phi_dot={k:v/(k[0]**2+k[1]**2) for k,v in S.items()}
            derivative=(inner(S,phi)+inner(rho,phi_dot))/2
            assert derivative==inner(phi,S)==2*sign*noise/perturb*U
            assert S.get((0,0),Q(0))==0
            rows.append({'harmonic_count':len(harmonics),'alignment_sign':sign,'perturbation':perturb,'noise':noise,
                         'initial_field_energy':U,'source_field_energy_derivative':derivative,
                         'source_log_field_energy_rate':derivative/U,'global_particle_moment_source':Q(0)})
        orthogonal=cosine((3,4),noise)
        assert inner(phi,orthogonal)==0
    return {'exact_Fourier_cases':rows,'orthogonal_source_controls':3,
      'identity':'Under self-adjoint periodic Poisson closure, Udot_source=mean(phi*S_rho). If S_rho=(noise/perturb)*delta_rho0 then Udot_source(0)=2*(noise/perturb)*U0.',
      'source_specific_initial_rate':Q(1,50),
      'limit':'Initial continuum conditional identity, not actual run power. The source has zero spatial-mean particle moments, which does not force zero electrostatic work. Later correlation can differ in sign/magnitude; a Vlasov-Maxwell/Ampere implementation needs its own Gauss/source treatment and actual outputs.'}

def printed_table_controls():
    ENL=[]
    for name,r,ratio,published in [('Main',100,50,'2.7e-2'),('M25E10',25,50,'1.1e-1'),('M50E10',50,50,'5.3e-2'),('M200E10',200,50,'1.3e-2'),('M25E1',25,50,'1.1e-1'),('M25E2',25,50,'1.1e-1'),('M25E4',25,50,'1.1e-1'),('M25E6',25,50,'1.1e-1'),('M25E8',25,50,'1.1e-1'),('T20',25,20,'4.2e-2'),('T100',25,100,'2.1e-1')]:
        actual=mp.mpf(ratio)/(6*mp.pi*r)
        assert float(format(float(actual),'.1e'))==float(published)
        ENL.append({'run':name,'normalized_ENL':actual,'published_two_significant_digits':published})
    Wsat=[]
    for name,r,E,published in [('M25E2',25,'.0005','.18'),('M25E4',25,'.001','.35'),('M25E10',25,'.0025','.88'),('Main',100,'.0025','1.77'),('M200E10',200,'.0025','2.50')]:
        percent=100*mp.mpf(E)*mp.sqrt(mp.mpf(r)/2)
        assert f'{float(percent):.2f}'==f'{float(published):.2f}'
        Wsat.append({'run':name,'predicted_percent':percent,'printed_percent':published})
    lifetime=(Q(202,10)*10*Q(1,40)-1)/(Q(8,100)*Q(1,40))
    assert lifetime==2025
    return {'ENL_table1':ENL,'Wsat_table2':Wsat,'Main_Eq4_7_tau_omega_pe':lifetime,
      'heating_fit_coefficient':M(Q(286,10))/mp.sqrt(2),
      'positive_assumptions':'Table normalization, quasi-linear saturation estimate and empirical duration algebra; not independent reproduction of nonlinear source data.'}

def main():
    if not __debug__:raise RuntimeError('Do not use -O; assertions must remain enabled.')
    result={'status':'all controls passed','runtime':{'python':platform.python_version(),'mpmath':mp.__version__,'mpmath_decimal_digits':mp.mp.dps},
      'program_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      'source_provenance':{'publisher_VOR_SHA256':'ece6a9ed59a5646d817db11c5468398a281b3704f223e59819f37faf75e29034',
        'erratum_SHA256':'2aa9f637c6a841943bfdc41ea7ca25a10b709fb3c6679c84707eab07ddc2c830',
        'v2_TeX_SHA256':'a7a5f1ead913eaebd8bc2c793693bd8b5083d9c2459a4061fd3b90e96da710a2',
        'public_Main_Lua_SHA256':'940969dfec824be5ec9244d50cb2e9d7f25642eedda3fe033d3e69c4831b84e6',
        'semantics':'Recorded hashes independently checked during source reading, not rehashed by this standalone scalar program.'},
      'dielectric_reduction':dielectric_reduction(),'growth':growth_controls(),'threshold':threshold_controls(),
      'Maxwellian_convention':maxwellian_convention_controls(),'forcing_beta_thermal':forcing_beta_and_thermal(),
      'conditional_source_energy':source_energy_controls(),
      'positive_tables':printed_table_controls(),
      'counts':{'A1_integrand_cases':18,'cold_limit_controls':6,'growth_cases':18,'constant_growth_controls':4,
                'literal_threshold_roots':12,'Gaussian_normalization_rescue_cases':4,'forcing_mass_ratios':5,
                'beta_cases':3,'mixture_variance_cases':9,'source_energy_Fourier_cases':9,
                'orthogonal_source_energy_controls':3,'ENL_rows':11,'Wsat_rows':5},
      'limits':['No source figures/raw nonlinear histories reconstructed.','Unknown display-versus-implementation correspondence remains explicit.','The1p erratum corrects editor acknowledgement wording only and is already reflected in currentVOR.',
                'Literal numerical threshold inconsistency is distinguished from order-one trapping/saturation conventions and empirical regime classification.']}
    output=ROOT/'independent-math-checks.json'
    output.write_text(json.dumps(pack(result),indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'status':result['status'],'counts':result['counts'],'E11_root':mp.nstr(result['threshold']['root_of_printed_E11_for_claimed_parameters'],18),
                      'root_from_literal_E2':mp.nstr(result['threshold']['root_if_literal_printed_E2_propagated'],18),
                      'width_reconciliation_multiplier':mp.nstr(result['threshold']['trapping_width_multiplier_that_reconciles_claim'],18),
                      'result_sha256':hashlib.sha256(output.read_bytes()).hexdigest()}))

if __name__=='__main__':main()
