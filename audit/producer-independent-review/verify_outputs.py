"""Read-only independent formula checks; never imports/executes the producer.

Requires mpmath. Source formulas were read independently. Optional comparison
of already produced second-runtime files performs no new scientific run.
"""
from pathlib import Path
from fractions import Fraction as F
from argparse import ArgumentParser
import csv,hashlib,json,math,sys
import mpmath as mp

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
mp.mp.dps=80

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def close(actual,expected,relative=mp.mpf('2e-15')):
    error=abs(mp.mpf(str(actual))-expected)
    assert error<=relative*max(abs(expected),mp.mpf('1e-30'))
    return error/max(abs(expected),mp.mpf('1e-30'))
def inner(a,b):return sum((v*b.get(-k,F(0)) for k,v in a.items()),F(0))

def main():
    if not __debug__:raise RuntimeError('Do not run this independent verifier with -O.')
    parser=ArgumentParser();parser.add_argument('--cross-runtime-dir',type=Path);args=parser.parse_args()
    paths=['data/consistency-controls.json','data/growth-controls.csv','data/threshold-controls.csv']
    before={n:sha(ROOT/n) for n in paths}
    data=json.loads((ROOT/paths[0]).read_bytes());assert data['all_checks_passed'] is True
    counts={};max_root=mp.mpf(0)
    for row in data['growth']:
        t0,g0,t=map(F,[row['t0'],row['gamma0'],row['t']])
        expected=g0*(t*t-t0*t0)/t0
        assert F(row['correct_log_energy_ratio'])==expected
        assert F(row['printed_log_energy_ratio'])==2*g0*t*t/t0
        assert F(row['required_log_derivative'])==2*g0*t/t0
        assert F(row['printed_log_derivative'])==4*g0*t/t0
    counts['rational_growth_states']=len(data['growth']);assert counts['rational_growth_states']==24
    # Closed LambertW solution independently checks both bisection branches.
    C=mp.sqrt(mp.pi/8)/4
    def threshold(r,q,multiplier):
        coefficient=C*multiplier
        x=coefficient/(2*mp.lambertw(coefficient/(2*mp.sqrt(q))))
        return mp.sqrt(2/r)*x*x
    for row in data['thresholds']:
        r=mp.mpf(row['mass_ratio']);q=mp.mpf(str(row['initial_noise_over_nTe']))
        for name,multiplier in [('literal_E11_equality_root',1),('root_following_literal_E2_coefficient',2)]:
            max_root=max(max_root,close(row[name],threshold(r,q,multiplier)))
        close(row['normalized_root_times_sqrt_mass'],threshold(r,q,1)*mp.sqrt(r))
    counts['threshold_rows']=len(data['thresholds']);assert counts['threshold_rows']==20
    quoted=data['quoted_threshold_check'];E=mp.mpf('5.6e-4');S=mp.mpf(25)*E*E/2
    left=mp.log(mp.sqrt(S)/mp.mpf('1e-8'));right=C*S**(-mp.mpf(1)/4)
    for key,value in [('E11_left',left),('E11_right',right),('equality_residual',left-right),
                      ('relative_width_factor_restoring_reported_field',mp.sqrt(left/right))]:close(quoted[key],value)
    for row in data['forcing']:
        r=F(row['mass_ratio']);E=F(row['physical_field'])
        assert F(row['printed_common_acceleration_total_Jdot'])==0
        assert F(row['correct_charge_weighted_total_Jdot'])==E*(1+1/r)
        assert F(row['physical_ion_electron_acceleration_ratio'])==-1/r
    counts['forcing_rows']=len(data['forcing']);assert counts['forcing_rows']==4
    for row in data['beta']:
        b=F(row['beta']);assert F(row['correct_coefficient_relative_to_beta1'])==1/b
        assert F(row['printed_coefficient_relative_to_beta1'])==b and F(row['printed_to_correct'])==b*b
        close(row['direct_Gaussian_field_reduction_over_beta1'],mp.mpf(b.denominator)/b.numerator,mp.mpf('1e-13'))
    counts['beta_rows']=len(data['beta']);assert counts['beta_rows']==5
    cold=data['cold_limit'];assert cold['denominator_identity_control_points']==4
    assert cold['denominator_identity_max_residual']<1e-14 and cold['literal_cold_pole_residual']<1e-14
    close(cold['literal_A2_positive_real_pole_over_omega_p'],1/mp.sqrt(2))
    positive=data['positive_controls']
    for row in positive['Table1']:close(row['ENL_over_field_unit'],mp.mpf(row['Te_Ti'])/(6*mp.pi*row['mass_ratio']))
    for row in positive['Table2']:close(row['Wsat_percent'],100*mp.mpf(str(row['field']))*mp.sqrt(mp.mpf(row['mass_ratio'])/2))
    assert abs(positive['Main_tau_res_omega_pe']-2025)<1e-9
    counts['ENL_rows']=len(positive['Table1']);counts['Wsat_rows']=len(positive['Table2'])
    assert counts['ENL_rows']==11 and counts['Wsat_rows']==5
    config=data['released_configuration_controls']
    for row in config['self_collision_exposure']:
        t=row['omega_pe_time'];assert F(row['electron_self_collision_exposure'])==F(t,10000)
        assert F(row['ion_self_collision_exposure'])==F(t,50000)
    counts['collisional_exposure_rows']=len(config['self_collision_exposure']);assert counts['collisional_exposure_rows']==7
    for row in config['initial_source_energy_witnesses']:
        epsilon=F(row['density_perturbation']);noise=F(row['source_amplitude']);rho={};source={}
        for mode in row['modes']:
            k=mode['wave'];amplitude=F(mode['amplitude'])
            rho[k]=rho[-k]=epsilon*amplitude/2;source[k]=source[-k]=noise*amplitude/2
        phi={k:v/(k*k) for k,v in rho.items()}
        energy=inner(rho,phi)/2;power=inner(phi,source)
        assert F(row['initial_field_energy'])==energy and F(row['initial_source_field_power'])==power
        assert F(row['power_over_field_energy'])==power/energy==F(1,50)
        assert 0 not in source and row['global_source_particle_moments_zero'] is True
        assert epsilon*sum(abs(F(m['amplitude'])) for m in row['modes'])<1
    counts['source_energy_Fourier_rows']=len(config['initial_source_energy_witnesses']);assert counts['source_energy_Fourier_rows']==3
    with (ROOT/paths[1]).open(newline='',encoding='utf-8') as f:csv_growth=list(csv.DictReader(f))
    assert csv_growth==data['growth']
    with (ROOT/paths[2]).open(newline='',encoding='utf-8') as f:csv_thresholds=list(csv.DictReader(f))
    assert len(csv_thresholds)==20
    for c,row in zip(csv_thresholds,data['thresholds']):
        assert set(c)==set(row)
        assert all(float(c[key])==value for key,value in row.items())
    assert before=={n:sha(ROOT/n) for n in paths}
    inputs={n:sha(ROOT/n) for n in [*paths,'reproduction/run_audit.py',
      'figures/growth-and-threshold-controls.png','figures/normalization-and-configuration-controls.png']}
    result={'status':'passed','method':'Independent exact Fraction identities, 80-digit closed LambertW roots, direct finite Fourier Poisson inner products and CSV/JSON checks; producer never imported or executed.',
      'verifier_sha256':sha(Path(__file__)),'counts':counts,'max_threshold_relative_error_vs_80digit_closed_form':mp.nstr(max_root,30),
      'both_CSVs_match_JSON':True,'input_sha256':inputs,'all_numeric_inputs_unchanged':True,
      'limits':'Display consistency and conditional continuum witnesses only; no source simulation/output or actual source-power calculation.'}
    (HERE/'checks.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
    if args.cross_runtime_dir:
        comparison=[]
        for name in paths:
            other=args.cross_runtime_dir/Path(name).name
            assert other.read_bytes()==(ROOT/name).read_bytes()
            comparison.append({'filename':Path(name).name,'bytes':other.stat().st_size,'sha256':sha(other),'byte_identical':True})
        runtime={'status':'passed','scope':'Comparison of existing3.12.14 producer output and existing3.13.7 --no-plots output, without a rerun.','files':comparison}
        (HERE/'runtime-byte-comparison.json').write_text(json.dumps(runtime,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'status':'passed','counts':counts,'max_threshold_relative_error':mp.nstr(max_root,20),'cross_runtime_compared':bool(args.cross_runtime_dir)}))

if __name__=='__main__':main()
