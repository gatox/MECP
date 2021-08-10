#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 18:12:12 2021

@author: edisonsalazar
"""

import numpy as np
import pandas as pd
import os

"""
Script to generate a file with number of MECP optimized steps, 
the distance between C12-C4, the energies S1 and S2 and 
the norm of the NAC with ETF for Closed DTE.
"""

natoms = 43 
atom1 = 4
atom2 = 12
folder = "MECP_S1S2"

em_df = pd.DataFrame()
for filename in os.listdir(folder):
    nacs = []
    if filename == "sf_closed_pf_mecp_S2S1_bhhlyp.out":
        with open(os.path.join(folder,filename), 'r+') as file: 
            counter = 0
            for line in file:
                if 'Standard Nuclear Orientation' in line:
                    counter += 1
                    C12_C4 = []
                    for _ in range(atom1 + 1): file.readline() # locate in the carbon 4
                    C_4 = file.readline().split()
                    C_4 = [float(C_4[2]),float(C_4[3]),float(C_4[4])]
                    for _ in range(atom2-atom1-1): file.readline() # locate in the carbon 12
                    C_12 = file.readline().split()
                    C_12 = [float(C_12[2]),float(C_12[3]),float(C_12[4])]
                    dist_C12_C4 = np.sqrt((C_12[0]-C_4[0])**2+(C_12[1]-C_4[1])**2\
                                          +(C_12[2]-C_4[2])**2)
                elif 'SF-CIS Derivative Couplings' in line:
                    for _ in range(6): file.readline() # skip 6 lines
                    Ei = file.readline().split()
                    Ei = float(Ei[-1])
                    Ej = file.readline().split()
                    Ej = float(Ej[-1]) 
                    
                elif 'SF-CIS derivative coupling with ETF' in line:
                    matrx = []
                    for _ in range(2): file.readline() # skip 2 lines
                    for i in range(natoms): # read in x, y, z NAC coordinates
                        coords = file.readline().split()
                        try:
                            matrx.append([float(coords[1]),float(coords[2]),float(coords[3])])
                        except:
                            print('error message')
                    nac = np.linalg.norm(np.array(matrx), "fro")
                    nacs.append([counter,dist_C12_C4,Ei,Ej,nac])      
    """
    Making Dataframe 
    """
    lt1_df = pd.DataFrame(nacs)
    em_df = em_df.append(lt1_df)                
"""
Processing Dataframe 
"""
em_df.columns = ["#Steps","C1-C4", "S1", "S2", "NAC"]
#em_df = em_df.sort_values(by="#C1-C4")
em_df = em_df.drop_duplicates(subset=["NAC"])
em_df.to_csv("DATA_PY/sf_closed_mecp_s2s1", index = False, sep='\t')
print(em_df)

    

        

                
         
            

                          