import CalculationsBis
import numpy as np
import pandas as pd

#############################################################################


def fig(stacking,theta,tAA,tAB,ElectricField,N,bands):
    fig = CalculationsBis.BlackBox(stacking,theta,tAA,tAB,ElectricField,N,bands)
    return fig

def dataframe():
    data = np.loadtxt('bulkek.dat-valley-K')
    dataprime = np.loadtxt('bulkek.dat-valley-Kprime')

    ks = data[:,0]
    Es = data[:,1]
    ksprime = dataprime[:,0]
    Esprime = dataprime[:,1]

    dataframe=pd.DataFrame({
    'Ks (K valley)':ks,
    'Energies (K valley)':Es,
    "Ks (K' valley)":ksprime,
    "Energies (K' valley)":Esprime
    })

    return dataframe

def schematic(stacking):
    encoded_image=CalculationsBis.Schematic(stacking)
    return encoded_image