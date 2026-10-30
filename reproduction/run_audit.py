"""Original deterministic controls; no imports from independent reviewers.

The original article's data, simulation outputs and solver are not executed.
Use --no-plots with only Python's standard library for numerical reproduction.
"""
from argparse import ArgumentParser
from fractions import Fraction as F
from pathlib import Path
import csv
import cmath
import json
import math

ROOT=Path(__file__).resolve().parents[1]


def check(condition,message):
    if not condition:
        raise RuntimeError(message)


def rational(value):
    return str(value)


def growth_controls():
    rows=[]
    for t0 in (F(1),F(2),F(5)):
        for gamma0 in (F(1,10),F(1,4)):
            for ratio in (F(1),F(3,2),F(2),F(3)):
                t=t0*ratio;a=gamma0/t0
                exact_log=a*(t*t-t0*t0)
                printed_log=2*a*t*t
                derivative_exact=2*a*t
                derivative_printed=4*a*t
                check(derivative_printed==2*derivative_exact,'Growth derivative ratio changed.')
                if ratio==1:check(exact_log==0 and printed_log!=0,'Initial anchoring control failed.')
                rows.append(dict(t0=rational(t0),gamma0=rational(gamma0),t=rational(t),
                    correct_log_energy_ratio=rational(exact_log),printed_log_energy_ratio=rational(printed_log),
                    required_log_derivative=rational(derivative_exact),printed_log_derivative=rational(derivative_printed)))
    return rows


def threshold_terms(field,mass_ratio,noise):
    check(field>0 and mass_ratio>0 and noise>0,'Positive threshold inputs required.')
    saturation=field*math.sqrt(mass_ratio/2)
    left=math.log(saturation/noise)
    right=0.25*math.sqrt(math.pi/8)*(2/(mass_ratio*field*field))**0.25
    return left,right


def threshold_root(mass_ratio,noise,rhs_multiplier=1.0):
    # Difference is strictly increasing: 1/x + positive/(2*x**(3/2)).
    low=noise*math.sqrt(2/mass_ratio)
    high=max(1.0,low*2)
    def residual(x):
        left,right=threshold_terms(x,mass_ratio,noise)
        return left-rhs_multiplier*right
    check(residual(low)<0 and residual(high)>0,'Root not bracketed.')
    for _ in range(200):
        mid=(low+high)/2
        if residual(mid)>0:high=mid
        else:low=mid
    result=(low+high)/2
    check(abs(residual(result))<1e-12,'Threshold root residual too large.')
    return result


def threshold_controls():
    rows=[]
    for mass_ratio in (25,100,400,1836):
        for noise in (1e-12,1e-10,1e-8,1e-6,1e-4):
            root=threshold_root(mass_ratio,noise)
            direct_root=threshold_root(mass_ratio,noise,2)
            check(abs(root*math.sqrt(mass_ratio)-threshold_root(25,noise)*5)<1e-12,'Mass-ratio collapse failed.')
            rows.append(dict(mass_ratio=mass_ratio,initial_noise_over_nTe=noise,
                literal_E11_equality_root=root,root_following_literal_E2_coefficient=direct_root,
                normalized_root_times_sqrt_mass=root*math.sqrt(mass_ratio)))
    quoted=5.6e-4;left,right=threshold_terms(quoted,25,1e-8)
    return rows,dict(mass_ratio=25,initial_noise_over_nTe=1e-8,reported_E12=quoted,
        E11_left=left,E11_right=right,equality_residual=left-right,
        literal_E11_root=threshold_root(25,1e-8),
        following_literal_E2_root=threshold_root(25,1e-8,2),
        relative_width_factor_restoring_reported_field=math.sqrt(left/right),
        interpretation='Literal numerical-equality check only. Order-one trapping-width choices prevent a universal physical-threshold or simulation-regime refutation.')


def coefficient_controls():
    forcing=[]
    for ratio in (25,100,400,1836):
        field=F(1,400);electron_mass=F(1);ion_mass=F(ratio)
        # q_e=-1,q_i=+1,n=1. Uniform identical accelerations cancel in total J.
        literal_current_derivative=field-field
        physical_current_derivative=field*(1/electron_mass+1/ion_mass)
        check(literal_current_derivative==0 and physical_current_derivative>0,'Forcing witness failed.')
        forcing.append(dict(mass_ratio=ratio,physical_field=rational(field),
            printed_common_acceleration_total_Jdot=rational(literal_current_derivative),
            correct_charge_weighted_total_Jdot=rational(physical_current_derivative),
            physical_ion_electron_acceleration_ratio=rational(-1/F(ratio))))
    beta=[]
    for b in (F(1,10),F(1,3),F(1),F(3),F(10)):
        check(b*b>0,'Positive beta required.')
        temperature=0.0004;mass_ratio=100;rate=0.1
        magnetic=math.sqrt(8*math.pi*temperature/float(b))
        alfven=magnetic/math.sqrt(4*math.pi*mass_ratio)
        field_unit=math.sqrt(4*math.pi)*math.sqrt(temperature)
        direct=rate*alfven*magnetic/field_unit
        beta1=2*rate*math.sqrt(1/mass_ratio)*math.sqrt(temperature)
        check(abs(direct/beta1-float(1/b))<1e-13,'Direct Gaussian field-unit reduction failed.')
        beta.append(dict(beta=rational(b),correct_coefficient_relative_to_beta1=rational(1/b),
            printed_coefficient_relative_to_beta1=rational(b),printed_to_correct=rational(b*b),
            direct_Gaussian_field_reduction_over_beta1=direct/beta1))
    p=1+1j;k=2.0
    residual=max(abs(1j*k/(p+1j*k*v)-1/(v-1j*p/k)) for v in (0,0.5,2,-3))
    check(residual<1e-14,'A1 denominator conversion failed.')
    literal_pole=cmath.sqrt(-1j)
    check(abs(1+1j/(literal_pole*literal_pole))<1e-14 and literal_pole.real>0,'Cold-limit literal-root control failed.')
    check(1+1/(1j*1j)==0,'Correct cold plasma poles failed.')
    return forcing,beta,dict(
        exact_algebra='i*k/(p+i*k*v) = 1/(v-i*p/k)',
        correct_cold_dielectric='1 + omega_p^2/p^2',
        literal_A2_cold_dielectric='1 + i*omega_p^2/p^2',
        correct_cold_poles='p = +/- i*omega_p',
        literal_A2_positive_real_pole_over_omega_p=1/math.sqrt(2),
        denominator_identity_control_points=4,denominator_identity_max_residual=residual,
        literal_cold_pole_residual=abs(1+1j/(literal_pole*literal_pole)),
        interpretation='Algebraic display diagnostic, not evidence that the source used this expression in its numerical dispersion calculation.')


def positive_controls():
    parameters=[('Main',100,50),('M25E10',25,50),('M50E10',50,50),('M200E10',200,50),
        ('M25E1',25,50),('M25E2',25,50),('M25E4',25,50),('M25E6',25,50),('M25E8',25,50),('T20',25,20),('T100',25,100)]
    en=[dict(run=name,mass_ratio=ratio,Te_Ti=temp,ENL_over_field_unit=temp/(6*math.pi*ratio)) for name,ratio,temp in parameters]
    expected_en=(0.027,0.11,0.053,0.013,0.11,0.11,0.11,0.11,0.11,0.042,0.21)
    for row,expected in zip(en,expected_en):
        check(float(format(row['ENL_over_field_unit'],'.2g'))==expected,'Printed Table1 ENL rounding mismatch.')
    wave=[dict(run=name,mass_ratio=ratio,field=field,Wsat_percent=100*field*math.sqrt(ratio/2))
        for name,ratio,field in [('M25E2',25,0.0005),('M25E4',25,0.001),('M25E10',25,0.0025),('Main',100,0.0025),('M200E10',200,0.0025)]]
    for row,expected in zip(wave,(0.18,0.35,0.88,1.77,2.50)):
        check(round(row['Wsat_percent'],2)==expected,'Printed Table2 Wsat rounding mismatch.')
    tau=(20.2*10*math.sqrt(100)*0.0025-1)/(0.08*math.sqrt(100)*0.0025)
    check(abs(tau-2025)<1e-10,'Positive resistivity-duration arithmetic failed.')
    return dict(Table1= en,Table2=wave,Main_tau_res_omega_pe=tau,
        normal_Gaussian_rescue='Z_N(zeta)=Z_FC(zeta/sqrt(2))/sqrt(2); with variance vT^2 this makes the printed unscaled zeta and 1+zeta Z_N(zeta) consistent.',
        Z_convention_finding='Undeclared convention only; no unconditional missing-sqrt(2) or computed-root failure is asserted.',
        model_scope='Self-species conservative regularization, available input decks and order-one trapping conventions require separate configuration review. No simulations are run by this producer.')


def released_configuration_controls():
    # Original one/two-mode continuum witnesses, not the deposited random field.
    rows=[]
    epsilon=F(1,10000);source=F(1,1000000)
    for modes in (((1,F(1)),),((2,F(1)),),((1,F(1)),(2,F(1,3)))):
        energy=sum(epsilon*epsilon*amplitude*amplitude/(4*wave*wave) for wave,amplitude in modes)
        power=sum(epsilon*source*amplitude*amplitude/(2*wave*wave) for wave,amplitude in modes)
        check(power==2*source/epsilon*energy,'Source field-energy identity failed.')
        check(epsilon*sum(abs(amplitude) for _,amplitude in modes)<1,'Positive density witness failed.')
        rows.append(dict(modes=[dict(wave=wave,amplitude=rational(amplitude)) for wave,amplitude in modes],
            density_perturbation=rational(epsilon),source_amplitude=rational(source),
            initial_field_energy=rational(energy),initial_source_field_power=rational(power),
            power_over_field_energy=rational(power/energy),global_source_particle_moments_zero=True))
    exposure=[]
    for time in (500,750,1000,2000,3500,4300,5000):
        exposure.append(dict(omega_pe_time=time,electron_self_collision_exposure=rational(F(time,10000)),
            ion_self_collision_exposure=rational(F(time,50000))))
    return dict(initial_source_energy_witnesses=rows,self_collision_exposure=exposure,
        interpretation='Conditional continuum source contribution with self-adjoint periodic Poisson solve. Zero global source particle-kinetic moments do not imply zero electrostatic source power. This does not measure source power in the actual run or establish that it explains a plotted curve.',
        conservative_self_collision_note='Self-species collisions may conserve total particle momentum and energy while modifying the distribution. No direct electron-ion collision drag is inferred.')


def write_csv(path,rows):
    with path.open('w',newline='',encoding='utf-8') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)


def main():
    parser=ArgumentParser();parser.add_argument('--out',type=Path,default=ROOT/'data');parser.add_argument('--no-plots',action='store_true')
    args=parser.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    growth=growth_controls();thresholds,quoted=threshold_controls();force,beta,cold=coefficient_controls()
    result=dict(all_checks_passed=True,growth=growth,thresholds=thresholds,quoted_threshold_check=quoted,
        forcing=force,beta=beta,cold_limit=cold,positive_controls=positive_controls(),
        released_configuration_controls=released_configuration_controls(),
        scope='Original mathematical consistency controls; no source simulation or measured curve is reproduced or disproved.')
    (args.out/'consistency-controls.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    write_csv(args.out/'growth-controls.csv',growth);write_csv(args.out/'threshold-controls.csv',thresholds)
    if not args.no_plots:
        import numpy as np
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        plt.rcParams.update({'font.size':14,'axes.titlesize':14,'axes.labelsize':14,
            'xtick.labelsize':12,'ytick.labelsize':12,'legend.fontsize':11.5})
        directory=ROOT/'figures';directory.mkdir(exist_ok=True)
        fig,axes=plt.subplots(1,2,figsize=(10.6,4.0),constrained_layout=True)
        time=np.linspace(1,3,180);a=0.25
        axes[0].plot(time,a*(time*time-1),label='Integrated energy growth')
        axes[0].plot(time,2*a*time*time,'--',label='Literal printed expression')
        axes[0].set(xlabel=r'$t/t_0$',ylabel=r'$\ln[W(t)/W(t_0)]$',title='Synthetic growth-law control')
        axes[0].legend();axes[0].grid(alpha=.2)
        noise=np.logspace(-12,-4,100)
        roots=np.array([threshold_root(25,float(q)) for q in noise])
        literal=np.array([threshold_root(25,float(q),2) for q in noise])
        axes[1].loglog(noise,roots,label='Displayed E11 equality')
        axes[1].loglog(noise,literal,'--',label='Following literal E2 coefficient')
        axes[1].scatter([1e-8],[5.6e-4],color='black',marker='x',s=55,label='Reported E12')
        axes[1].set(xlabel=r'$W_0/(n_0 T_{e0})$',ylabel=r'$\widetilde E_{\rm crit}$',title='Literal estimates, mass ratio 25')
        axes[1].legend(loc='lower right');axes[1].grid(alpha=.2)
        fig.savefig(directory/'growth-and-threshold-controls.png',dpi=210);plt.close(fig)
        fig,axes=plt.subplots(1,2,figsize=(10.6,3.8),constrained_layout=True)
        betas=np.logspace(-1,1,160)
        axes[0].loglog(betas,1/betas,label='Gaussian field-unit reduction')
        axes[0].loglog(betas,betas,'--',label='Printed beta dependence')
        axes[0].set(xlabel=r'$\beta_e$',ylabel='Coefficient relative to beta = 1',title='Conditional normalization control')
        axes[0].legend();axes[0].grid(alpha=.2)
        times=np.linspace(0,5000,160)
        axes[1].plot(times,1e-4*times,label='Electron self-collisions')
        axes[1].plot(times,2e-5*times,label='Ion self-collisions')
        axes[1].set(xlabel=r'$\omega_{pe}t$',ylabel=r'$\nu_{ss}t$',title='Released Main input parameters')
        axes[1].legend();axes[1].grid(alpha=.2)
        fig.savefig(directory/'normalization-and-configuration-controls.png',dpi=210);plt.close(fig)
    print(json.dumps(dict(all_checks_passed=True,growth_states=len(growth),threshold_states=len(thresholds),
        forcing_states=len(force),beta_states=len(beta),literal_E11_root=quoted['literal_E11_root'],
        reported_E12=quoted['reported_E12'],simulation_runs=0)))


if __name__=='__main__':main()
