import numpy as np
from astropy import constants

from photochem.utils import stars
from photochem.utils import species_file_for_climate, settings_file_for_climate
from photochem.clima import AdiabatClimate

def blackbody_spectrum(outputfile, stellar_flux, Teff):
    wv = np.logspace(np.log10(0.1), np.log10(100), 1000)*1e3 # nm
    F = stars.blackbody(Teff, wv)*np.pi
    stars.save_photochem_spectrum(
        wv=wv, 
        F=F, 
        outputfile=outputfile, 
        stellar_flux=stellar_flux, 
        scale_to_planet=True, 
    )

def main():

    # Make some input files
    species_file_for_climate(
        filename='species.yaml',
        species=['H2O','N2','CO2'],
        condensates=['H2O','CO2']
    )
    settings_file_for_climate(
        filename='settings.yaml',
        planet_mass=float(constants.M_earth.cgs.value),
        planet_radius=float(constants.R_earth.cgs.value),
        surface_albedo=0.2
    )
    blackbody_spectrum(
        outputfile='star.txt', 
        stellar_flux=1360.0, 
        Teff=5700.0
    )

    # Initialize
    c = AdiabatClimate(
        species_file='species.yaml', 
        settings_file='settings.yaml', 
        flux_file='star.txt',
    )

    # Run a simple test case
    P_i = np.ones(len(c.species_names))*1.0e-15
    P_i[c.species_names.index('N2')] = 1.0
    P_i[c.species_names.index('H2O')] = 270.0
    P_i[c.species_names.index('CO2')] = 400.0e-6
    P_i *= 1e6
    c.T_trop = 200
    c.solve_for_T_trop = True
    T_surf = c.surface_temperature(P_i, T_guess=290.0)
    print(f"Surface Temperature = {T_surf:.0f} K")

    assert np.isfinite(T_surf)
    assert 150.0 < T_surf < 500.0

if __name__ == "__main__":
    main()



