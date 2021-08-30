# import modules
import subprocess
import numpy as np
import pandas as pd

# plotly
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import Axes3D
import base64

def BlackBox(stacking,theta,tAA,tAB,ElectricField,N,bands):
    """
    outputs figure object
    stacking is a list of strings
    twist is layer number to have twist angle (1 is between lowest and second lowest, etc)
    assumes all of the fortran files are in the directory and "make" has been completed
    meta-code method is not scalable
    """
    import os
    cwd=os.getcwd()
    
    # write data into system.in
    ReadWriteData(stacking,theta,tAA,tAB,ElectricField,N,bands)
    
    # execute ./tg_kpgen
    subprocess.run(["./tg_kpgen"])
    
    # create figure
    fig = MakeFigure()
    
    os.chdir(cwd)
    return fig

def UnpackStack(stacking):
    """
    Returns stacking pattern sequence, number of layers, and twist angle
    """
    twist=stacking.find("-")
    wo_twist=stacking.replace("-","")
    layers=len(wo_twist)
    list_wo_twist=[x for x in wo_twist]
    stacking_sequences="{}".format(list_wo_twist).replace("[","").replace("]","").replace(","," ")

    return stacking_sequences, layers, twist

def ReadWriteData(stacking,theta,tAA,tAB,ElectricField,N,bands):
    """
    Writes input parameters into system.in file
    """    
    # unpack stack
    stacking_sequences,layers,twist=UnpackStack(stacking)
    
    # twisted angle array input
    twist_list="{}".format([0 for _ in range(twist)]+[1 for _ in range(twist,layers+1)])
    twist_input=twist_list.replace("[","").replace("]","").replace(","," ")

    # interlayer coupling input
    intercoupling_ratio_list="{}".format(['1' for _ in range(layers)])
    intercoupling_ratio_input=intercoupling_ratio_list.replace(","," ").replace("[","").replace("]","")
    
    # open file
    f = open("system-initial.in","r")
    systemIn=f.read()
    f.close()

    Lines=systemIn.split("\n")

    Lines[1]="number_layers={}".format(layers) # number of layers
    Lines[2]="twisted_angle_degree={}".format(theta) # twist angle
    Lines[3]="twisted_angle_array_input={}".format(twist_input) # twisted layers, 0 and 1
    Lines[4]="interlayercoupling_ratio_array_input = {}".format(intercoupling_ratio_input) # all ones
    Lines[5]="stacking_sequences_input = {}".format(stacking_sequences) # type of stacking (A,B,C)
    Lines[6]="u_AA={}".format(tAA/1000) # in eV
    Lines[7]="u_AB={}".format(tAB/1000) # in eV
    Lines[10]="Qcutoff={}".format(N) # moiré cutoff
    Lines[11]="Num_bands={}".format(bands) # no. of bands
    Lines[12]="Nk={}".format(100) # fixed
    Lines[13]="Electric_field={}".format(ElectricField/1000) # eV/Angstrom

    systemIn="\n".join(Lines)

    Output = open("system.in","w")
    Output.write(systemIn)
    Output.close()

def make_bands(ks,Es):
    """
    Turns scatter arrays into bands to be plotted
    """
    ks_unique,ks_index=np.unique(ks,return_index=True)
    
    # index after which ks repeat
    jump=np.max(ks_index)+1
    
    # reshape into (no. of ks, no. of bands)
    ks=ks.reshape(-1,jump).T
    Es=Es.reshape(-1,jump).T
    return ks,Es


def Figure(Ks,Es,KsP,EsP):
    """
    Figure object for App.
    Ks,Es have dimensions (# of k-points, # of bands)
    Makes plot displaying energies and DOS for K and Kprime (P) valleys
    """
    lim=np.max(np.abs(Es))

    fig = make_subplots(rows=1, cols=1, shared_yaxes=True, horizontal_spacing=0.01)

    # energies
    for j in range(Es.shape[1]):
        # only one trace in legend
        showlegend=False
        if j==0:
            showlegend=True

        fig.add_trace(go.Scatter(x=Ks[:,j], y=Es[:,j],
        marker=dict(size=1,color='rgba(207, 0, 15, 0.6)'),
        mode='lines',
        name='K valley',
        showlegend=showlegend,
        legendgroup='a'),
        row=1, col=1)

    for j in range(EsP.shape[1]):
        showlegend=False
        if j==0:
            showlegend=True

        fig.add_trace(go.Scatter(x=KsP[:,j], y=EsP[:,j],
        marker=dict(size=1,color='rgba(44, 130, 201, 0.6)'),
        mode='lines',
        name="K' valley",
        showlegend=showlegend,
        legendgroup='b'),
        row=1, col=1)       

    # labels
    fig.update_yaxes(title_text="Energy [eV]", range=[-lim,lim], row=1, col=1)

    a=np.max(Ks)/(3+np.sqrt(3)/2)
    fig.update_xaxes(title_text="Momentum [Moiré zone]", 
    tickmode="array", 
    tickvals=[0,a/2,3/2*a,(3/2+np.sqrt(3)/2)*a,(2+np.sqrt(3)/2)*a,(3+np.sqrt(3)/2)*a],
    ticktext=["M","K","Γ","M","K'","Γ"],
    row=1, col=1)

    # set layout
    fig.update_layout(autosize=True,
    height=750, 
    title={
        'text':'Bandstructure of Twisted Mixed Multilayer Graphene',
        'y':0.94,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1),
        )

    return fig

def MakeFigure():
    """
    Creates fig object for dash
    weight not yet incorporated (TODO)
    """ 
    data = np.loadtxt('bulkek.dat-valley-K')
    dataprime = np.loadtxt('bulkek.dat-valley-Kprime')

    ks = data[:,0]
    Es = data[:,1]
    ksprime = dataprime[:,0]
    Esprime = dataprime[:,1]
    
    ks_clean,Es_clean=make_bands(ks,Es)
    ksprime_clean,Esprime_clean=make_bands(ksprime,Esprime)
    
    fig=Figure(ks_clean,Es_clean,ksprime_clean,Esprime_clean)
    
    return fig

### Calculations for Schematic
def AddLayer(ax,z,rot,stack):
    """
    rot = True or False
    stack = A, B or C
    """
    t=0
    if rot:
        t=15*np.pi/180
    # list of vertices originally at (1,1), (-1,1), (1,-1), (-1,-1)   
    x_rot = [-1*np.cos(t)+1*np.sin(t),1*np.cos(t)+1*np.sin(t),1*np.cos(t)-1*np.sin(t),-1*np.cos(t)-1*np.sin(t)]
    y_rot = [-1*np.sin(t)-1*np.cos(t),1*np.sin(t)-1*np.cos(t),1*np.sin(t)+1*np.cos(t),-1*np.sin(t)+1*np.cos(t)]
    z_rot = [z,z,z,z]
    verts = [list(zip(x_rot,y_rot,z_rot))]
    if stack=='A':
        ax.add_collection3d(Poly3DCollection(verts,facecolor='crimson'))
    if stack=='B':
        ax.add_collection3d(Poly3DCollection(verts,facecolor='dodgerblue'))
    elif stack=='C':
        ax.add_collection3d(Poly3DCollection(verts,facecolor='forestgreen'))

def Schematic(stacking):
    """
    Return matplotlib sketch
    Input is stacking string, ex: 'A-BC'
    """
    # start mpl process
    fig = plt.figure(figsize=(2,1))
    ax=fig.add_subplot(1, 1, 1, projection = '3d')
    
    twist=stacking.find("-")
    stackingfix=stacking.replace("-","")
    rot=False # only adapted for single twist
    
    for i in range(len(stackingfix)):
        z=i
        if i>=twist:
            rot=True # rest of layers are also twisted
        stack=stackingfix[i]
        AddLayer(ax,z,rot,stack)
    
    ax.set_xlim([-1.2,1.2])
    ax.set_ylim([-1.2,1.2])
    ax.set_zlim([0,len(stackingfix)])

    # Hide grid lines
    ax.grid(False)

    # Hide axes ticks
    ax.set_axis_off()

    # save image
    path='schematic.png'
    plt.savefig(path, transparent=True)
    plt.close()

    encoded_image = base64.b64encode(open(path, 'rb').read())

    return encoded_image
