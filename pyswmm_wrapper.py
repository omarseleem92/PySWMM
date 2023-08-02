# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2022 Bryant E. McDonnell
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------
"""
Function developed to execute a PySWMM Simulation on the command line. To run,
execute the following on the command line:

python --help # Produces a list of options

python <path>/pyswmm_wrapper.py <path>/*.inp <path>/*.rpt <path>/*.out # optional args
"""

import argparse
import pathlib
import pyswmm
import pyswmm
from pyswmm import Simulation,Subcatchments,Nodes,SystemStats,LidControls,LidGroups
import numpy as np
import pandas as pd
import math
import multiprocessing
import concurrent.futures
import os
import swmmio

def run_model():
    """Run Model."""
    # Argument Resolution
    parser = argparse.ArgumentParser()
    parser.add_argument('inp_file', type=pathlib.Path,
                        help='Input File Path')
    parser.add_argument('rpt_file', type=pathlib.Path, nargs='?',
                        help='Report File Path (Optional).')
    parser.add_argument('out_file', type=pathlib.Path, nargs='?',
                        help='Output File Path (Optional).')
    parser.add_argument('A2', type= float, help='Catchment 2 area ratio')
    parser.add_argument('Surface_thickness_value', type= float, help='Surface_thickness_value')                    
    parser.add_argument('Soil_thickness_value', type= float, help='Soil_thickness_value')                    
    parser.add_argument('Storage_thickness_value', type= float, help='Storage_thickness_value')                    
    parser.add_argument('Drain_offset_value', type= float, help='Drain_offset_value')                    
    parser.add_argument('Seepage_rate_value', type= float, help='Seepage_rate_value')                    
    

    report_prog_help = "--report-progress can be useful for longer model runs. The drawback "\
                       +"is that it slows the simulation down.  Use an integer to specify how "\
                       +"frequent to interrup the simulation. This depends of the number of time "\
                       +"steps"
    parser.add_argument('--report_progress', default=False, type=int,
                        help=report_prog_help)
    args = parser.parse_args()

    # File Naming -> Str Paths
    inp_file = str(args.inp_file)
    if args.rpt_file:
        rpt_file = str(args.rpt_file)
    else:
        rpt_file = args.rpt_file
    out_file = str(args.out_file)
    if args.out_file:
        out_file = str(args.out_file)
    else:
        out_file = args.out_file
    A2=args.A2
    Surface_thickness_value=args.Surface_thickness_value
    Soil_thickness_value=args.Soil_thickness_value
    Storage_thickness_value=args.Storage_thickness_value
    Drain_offset_value=args.Drain_offset_value
    Seepage_rate_value=args.Seepage_rate_value

    # Running the simulation without and with progress reporting.
    if args.report_progress == False:
        sim = pyswmm.Simulation(inp_file, rpt_file, out_file)
        subcatch_object= Subcatchments(sim)
        Bio_retention = LidControls(sim)["Typ1"]


        # Subcathment parameters
        SC1 = subcatch_object["S1"]
        SC2 = subcatch_object["S2"]
        
        SC2.area=np.round(A2*0.1,3)
        SC1.area=np.round((1-A2)*0.1,3)

        #print("A1=",SC1.area)
        #print("A2=",SC2.area)


        SC1.width=np.round(0.5*math.sqrt(SC1.area*10000),3)
        SC2.width=np.round(0.5*math.sqrt(SC2.area*10000),3)
        #print("W1=",SC1.width)
        #print("W2=",SC2.width)

            # Lid parameters
            # Surface layer
        Bio_retention.surface.thickness=Surface_thickness_value
        #print("Berm_Height=",Bio_retention.surface.thickness)


        Bio_retention.soil.thickness=Soil_thickness_value
        #print("Soil_thickness=",Bio_retention.soil.thickness)

        Bio_retention.storage.thickness=Storage_thickness_value
        #print("Storage_thickness=",Bio_retention.storage.thickness)

        Bio_retention.drain.offset=Drain_offset_value
        #print("Drain_offset=",Bio_retention.drain.offset)  
                            
        Bio_retention.storage.k_saturated=Seepage_rate_value
        #print("Seepage_rate_value=",Bio_retention.storage.k_saturated)

            # Lid area
        sub_2_lid_units = LidGroups(sim)["S2"]
        first_unit = sub_2_lid_units[0]
            #print(first_unit)
        #print("Original Unit_area = ", first_unit.unit_area)

        first_unit.unit_area=SC2.area*10000
        #print("Modified_Unit_Area=",first_unit.unit_area)


        for ind,step in enumerate(sim):
             pass
        S1_stat=SC1.statistics

            #Outflow_SC2.append(SC2.runoff)
        S2_stat=SC2.statistics
        system_routing = SystemStats(sim)
        System_stat=system_routing.runoff_stats
        
        print(SC2.area)
        print(Bio_retention.surface.thickness)
        print(Bio_retention.soil.thickness)
        print(Bio_retention.storage.thickness)
        print(Bio_retention.drain.offset)
        print(Bio_retention.storage.k_saturated)
        print(S1_stat)
        print(S2_stat)
        print(System_stat)

        
        #sim.execute()
    else:
        with pyswmm.Simulation(inp_file, rpt_file, out_file) as sim:
            for ind, step in enumerate(sim):
                if ind % args.report_progress == 0:
                    print(round(sim.percent_complete*1000)/10.0)

    return 0

if __name__ in "__main__":
    run_model()