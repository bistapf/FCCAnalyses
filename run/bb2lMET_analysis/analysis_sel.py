#Input directory where the files produced at the pre-selection level are
inputDir  = "/eos/user/b/bistapf/FCChh_EvtGen/bb2lMET_ntuples/SFOS/"


#TESTER FOR THE ee+mm but no Z selection
#Input directory where the files produced at the pre-selection level are
outputDir  = "/eos/user/b/bistapf/FCChh_EvtGen/bb2lMET_ntuples/SFOS/noZ/"

processList = {
    # 'pwp8_pp_hh_lambda100_5f_hhbbww':{}, 
    # 'pwp8_pp_hh_lambda100_5f_hhbbtata':{}, #Run over the statistics from stage2 input files <inputDir>/p8_ee_WW_ecm240_out/*.root. Keep the same output name as input
    # 'pwp8_pp_hh_lambda100_5f_hhbbzz_zleptonic':{} #Run over the full statistics from stage2 input file <inputDir>/p8_ee_ZH_ecm240_out.root. Change the output name to MySample_p8_ee_ZH_ecm240
    # 'mgp8_pp_tt012j_5f':{},
    #single Higgs bkg
    # 'mgp8_pp_h012j_5f':{},
    # 'mgp8_pp_vbf_h01j_5f':{},
    # 'mgp8_pp_vh012j_5f':{},
    # 'mgp8_pp_tth01j_5f':{},
    #V+jets bkg
    "mgp8_pp_vj_5f_HT_500_1000":{},
    "mgp8_pp_vj_5f_HT_1000_2000":{},
    "mgp8_pp_vj_5f_HT_5000_10000":{},
    "mgp8_pp_vj_5f_HT_10000_27000":{},
    "mgp8_pp_vj_5f_HT_27000_100000":{},
}

#Link to the dictonary that contains all the cross section informations etc...
procDict = "FCChh_procDict_v05_scenarioI.json"

#Add MySample_p8_ee_ZH_ecm240 as it is not an offical process
# procDictAdd={"pwp8_pp_hh_lambda100_5f_hhbbzz_zleptonic": {"numberOfEvents": 50000, "sumOfWeights": 50000.0, "crossSection": 0.0032097804, "kfactor": 1.08, "matchingEfficiency": 1.0}}
# procDictAdd={"pwp8_pp_hh_lambda100_5f_hhbbww": {"numberOfEvents": 50000, "sumOfWeights": 50000.0, "crossSection": 0.28332, "kfactor": 1.08, "matchingEfficiency": 1.0}}
# procDictAdd={"pwp8_pp_hh_lambda100_5f_hhbbtata": {"numberOfEvents": 4997958, "sumOfWeights": 4997958.0, "crossSection": 0.08214306096, "kfactor": 1.08, "matchingEfficiency": 1.0}}
# procDictAdd={"mgp8_pp_tt012j_5f": {"numberOfEvents": 79190000, "sumOfWeights": 79190000.0, "crossSection": 43110.0, "kfactor": 1.74, "matchingEfficiency": 1.0},}

#Number of CPUs to use
nCPUS = 4

#produces ROOT TTrees, default is False
doTree = True

# saveTabular = True

###Dictionnay of the list of cuts. The key is the name of the selection that will be added to the output file
cutList = { "sel1_lepton_pair":"n_OS_ll_pairs > 0", 
            "sel2_bJets_medium":"n_OS_ll_pairs > 0 && n_b_jets_medium > 1", 
            # "sel2_bJets_loose":"n_OS_ll_pairs > 0 && n_b_jets_loose > 1", 
            # "sel2_bJets_tight":"n_OS_ll_pairs > 0 && n_b_jets_tight > 1", 
            "sel3_mbb":"n_OS_ll_pairs > 0 && n_b_jets_medium > 1 && m_bb[0] > 85 && m_bb[0] < 150",
            "sel4_dRbb":"n_OS_ll_pairs > 0 && n_b_jets_medium > 1 && m_bb[0] > 85 && m_bb[0] < 150 && dR_bb[0] < 2.0",
            "sel5_mll":"n_OS_ll_pairs > 0 && n_b_jets_medium > 1 && m_bb[0] > 85 && m_bb[0] < 150 && dR_bb[0] < 2.0 && m_ll[0] > 10 && m_ll[0] < 80",
            "sel6_dRll":"n_OS_ll_pairs > 0 && n_b_jets_medium > 1 && m_bb[0] > 85 && m_bb[0] < 150 && dR_bb[0] < 2.0 && m_ll[0] > 10 && m_ll[0] < 80 && dR_ll[0] < 1.8",
            "sel7_dphillMET":"n_OS_ll_pairs > 0 && n_b_jets_medium > 1 && m_bb[0] > 85 && m_bb[0] < 150 && dR_bb[0] < 2.0 && m_ll[0] > 10 && m_ll[0] < 80 && dR_ll[0] < 1.8 && abs(dPhi_ll_MET[0]) < 2.0",
            "sel8_HT2_ratio":"n_OS_ll_pairs > 0 && n_b_jets_medium > 1 && m_bb[0] > 85 && m_bb[0] < 150 && dR_bb[0] < 2.0 && m_ll[0] > 10 && m_ll[0] < 80 && dR_ll[0] < 1.8 && abs(dPhi_ll_MET[0]) < 2.0 && HT2_ratio[0] > 0.8",
            "sel9_mlb_150":"n_OS_ll_pairs > 0 && n_b_jets_medium > 1 && m_bb[0] > 85 && m_bb[0] < 150 && dR_bb[0] < 2.0 && m_ll[0] > 10 && m_ll[0] < 80 && dR_ll[0] < 1.8 && abs(dPhi_ll_MET[0]) < 2.0 && HT2_ratio[0] > 0.8 && mlb_reco[0] > 150.",

            }

#Dictionary for the ouput variable/hitograms. The key is the name of the variable in the output files. "name" is the name of the variable in the input file, "title" is the x-axis label of the histogram, "bin" the number of bins of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.
histoList = {
}

# fccanalysis final analysis_sel.py