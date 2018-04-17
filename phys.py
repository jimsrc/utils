#
import numpy as np

#--- universal constants
qe          = (4.8032*1e-10) # [statC] carga PROTON
mo          = 1.6726e-24 # [gr] masa PROTON
c           = 3e10            # [cm/s] light speed
AU_in_cm    = 1.5e13     # [cm]
E_reposo    = 938272013.0  # [eV] PROTON

def calc_Rlarmor(rigidity, Bo):
    """
    input:
    Ek      : [eV] kinetic energy
    rigi..  : [V] rigidity
    Bo      : [G] magnetic field in Gauss
    output:
    Rl      : [cm] larmor radii
    """

    #rigidity = sqrt(Ek*Ek + 2.*Ek*E_reposo);
    #------------------------CALCULO DE GAMMA Y BETA
    gamma = np.sqrt((rigidity/E_reposo)**2 + 1.)
    beta  = np.sqrt(1. - 1./(gamma*gamma))
    #------------------------------CALCULO CICLOTRON
    omg = q * Bo / (gamma * mo * c)     # [s^-1]
    #---------------------------CALCULO RADIO LARMOR
    v   = beta * c              # [cm/s]
    #Rl[0]  = (v / omg) /AU_in_cm  # [AU]
    return (v / omg) # [cm]

def calc_beta_relativist(Ek):
    """
    Ek      : [eV] kinetic energy
    """
    rigidity = np.sqrt(Ek + 2.*Ek*E_reposo)
    gamma    = np.sqrt((rigidity/E_reposo)**2 + 1.)
    beta     = np.sqrt(1. - 1./(gamma*gamma))
    return beta

def K2mfp(Kdiff, Ek):
    """
    convert spatial diffusion coeff to mean-free-path
    Kdiff       : [cm^2/s] spatial diffusion coeff
    """
    v   = c * calc_beta_relativist(Ek) # [cm/s]
    mfp = (3./v) * Kdiff        # [cm]
    mfp_in_AU = mfp / AU_in_cm  # [AU]
    return mfp_in_AU

#EOF
