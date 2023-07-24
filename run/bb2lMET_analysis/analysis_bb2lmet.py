
#flavour option - HOW DO I GET THIS TO BE COMMAND LINE?
flavour = "SFOS"

#running in screen on lxplus782 subjobs
#for batch submission 
processList = {
    # "pwp8_pp_hh_lambda100_5f_hhbbww":{'chunks':200, 'output':"FCChh_EvtGen_pwp8_pp_hh_lambda100_5f_hhbbww"}, #put the name of your input file here (without .root), the output file will have the same name
    # "pwp8_pp_hh_lambda100_5f_hhbbtata":{'chunks':200, 'output':"FCChh_EvtGen_pwp8_pp_hh_lambda100_5f_hhbbtata"}, #put the name of your input file here (without .root), the output file will have the same name
    # "pwp8_pp_hh_lambda100_5f_hhbbzz_zleptonic":{'chunks':200, 'output':"FCChh_EvtGen_pwp8_pp_hh_lambda100_5f_hhbbww"}, #put the name of your input file here (without .root), the output file will have the same name
    # "mgp8_pp_tt012j_5f":{'chunks':2499, 'output':"FCChh_EvtGen_mgp8_pp_tt012j_5f"}, #put the name of your input file here (without .root), the output file will have the same name 
    # "mgp8_pp_h012j_5f":{'chunks':200}, #put the name of your input file here (without .root), the output file will have the same name
    # "mgp8_pp_vbf_h01j_5f":{'chunks':200}, #put the name of your input file here (without .root), the output file will have the same name
    # "mgp8_pp_vh012j_5f":{'chunks':200}, #put the name of your input file here (without .root), the output file will have the same name
    # "mgp8_pp_tth01j_5f":{'chunks':200},
    # "mgp8_pp_ttw_5f":{'chunks':200},
    # "mgp8_pp_ttz_5f":{'chunks':200},
    # "mgp8_pp_ttzz_5f":{'chunks':200},
    # "mgp8_pp_ttwz_5f":{'chunks':200},
    # "mgp8_pp_ttww_4f":{'chunks':200},
    # "mgp8_pp_vj_5f_HT_500_1000":{'chunks':200},
    # "mgp8_pp_vj_5f_HT_1000_2000":{'chunks':200},
    "mgp8_pp_vj_5f_HT_2000_5000":{'chunks':200},
    # "mgp8_pp_vj_5f_HT_5000_10000":{'chunks':200},
    # "mgp8_pp_vj_5f_HT_10000_27000":{'chunks':200},
    # "mgp8_pp_vj_5f_HT_27000_100000":{'chunks':200},
}


#for local testing:
# processList= {
# #     # "pwp8_pp_hh_lambda100_5f_hhbbtata":{'output':"FCChh_EvtGen_pwp8_pp_hh_lambda100_5f_hhbbtata"}, 
#     "pwp8_pp_hh_lambda100_5f_hhbbww":{}, 
# #     # "pwp8_pp_hh_lambda100_5f_hhbbaa":{'output':"FCChh_EvtGen_pwp8_pp_hh_lambda100_5f_hhbbaa"}, 
# #     # "pwp8_pp_hh_lambda100_5f_hhbbzz_4l":{'output':"FCChh_EvtGen_pwp8_pp_hh_lambda100_5f_hhbbzz_4l"}, 
# #     "pwp8_pp_hh_lambda100_5f_hhbbww/events_000013364":{'output':"pwp8_pp_hh_lambda100_5f_hhbbww_events_000013364_tester"}, 
# #     # "mgp8_pp_tt012j_5f":{'output':"FCChh_EvtGen_mgp8_pp_tt012j_5f"}, 
#     # "mgp8_pp_vj_5f_HT_500_1000":{'output':"FCChh_EvtGen_mgp8_pp_vj_5f_HT_500_1000"}, 
# }

# /eos/user/b/bistapf/FCChh_EvtGen/bb2lMET_ntuples/SFOS/

#Mandatory: input directory when not running over centrally produced edm4hep events. 
inputDir    = "/eos/experiment/fcc/hh/generation/DelphesEvents/fcc_v05_scenarioI/" #your directory with the input file

#Optional: output directory, default is local dir
outputDir   = "/eos/user/b/bistapf/FCChh_EvtGen/bb2lMET_ntuples/{}/".format(flavour)

#Optional: ncpus, default is 4
nCPUS       = 8

#Optional running on HTCondor, default is False
# runBatch    = False
runBatch    = True





#Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis():

    #__________________________________________________________
    #Mandatory: analysers funtion to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df, out_name):
        import ROOT

        df2 = (df

              ########################################### EVENT HEADER ########################################### 
              .Define("weight",  "EventHeader.weight")
              

              ########################################### JETS ########################################### 
              # all jets - before any object overlap removal
              .Define("n_jets_noiso",  "FCCAnalyses::ReconstructedParticle::get_n(JetNoIso)")
              .Define("px_jets_noiso",  "FCCAnalyses::ReconstructedParticle::get_px(JetNoIso)")
              .Define("py_jets_noiso",  "FCCAnalyses::ReconstructedParticle::get_py(JetNoIso)")
              .Define("pz_jets_noiso",  "FCCAnalyses::ReconstructedParticle::get_pz(JetNoIso)")
              .Define("E_jets_noiso",  "FCCAnalyses::ReconstructedParticle::get_e(JetNoIso)")
              .Define("pT_jets_noiso",  "FCCAnalyses::ReconstructedParticle::get_pt(JetNoIso)")
              .Define("eta_jets_noiso",  "FCCAnalyses::ReconstructedParticle::get_eta(JetNoIso)")

              # get the flavour tags for those jets:
              .Alias("JetNoIso_pids","JetNoIso#3.index") 

              #LOOSE WP
              .Define("b_tagged_jets_loose_noiso", "AnalysisFCChh::get_tagged_jets(JetNoIso, JetNoIso_pids, ParticleIDs, ParticleIDs_0, 0)") #bit 0 = loose WP, see: https://github.com/delphes/delphes/blob/master/cards/FCC/scenarios/FCChh_I.tcl
              .Define("n_b_jets_loose_noiso", "FCCAnalyses::ReconstructedParticle::get_n(b_tagged_jets_loose_noiso)")
              .Define("px_b_jets_loose_noiso",  "FCCAnalyses::ReconstructedParticle::get_px(b_tagged_jets_loose_noiso)")
              .Define("py_b_jets_loose_noiso",  "FCCAnalyses::ReconstructedParticle::get_py(b_tagged_jets_loose_noiso)")
              .Define("pz_b_jets_loose_noiso",  "FCCAnalyses::ReconstructedParticle::get_pz(b_tagged_jets_loose_noiso)")
              .Define("E_b_jets_loose_noiso",  "FCCAnalyses::ReconstructedParticle::get_e(b_tagged_jets_loose_noiso)")
              .Define("pT_b_jets_loose_noiso",  "FCCAnalyses::ReconstructedParticle::get_pt(b_tagged_jets_loose_noiso)")
              .Define("eta_b_jets_loose_noiso",  "FCCAnalyses::ReconstructedParticle::get_eta(b_tagged_jets_loose_noiso)")


              # jets after overlap removal is performed between jets and isolated electrons, muons and photons
              .Define("n_jets",  "FCCAnalyses::ReconstructedParticle::get_n(Jet)")
              .Define("px_jets",  "FCCAnalyses::ReconstructedParticle::get_px(Jet)")
              .Define("py_jets",  "FCCAnalyses::ReconstructedParticle::get_py(Jet)")
              .Define("pz_jets",  "FCCAnalyses::ReconstructedParticle::get_pz(Jet)")
              .Define("E_jets",  "FCCAnalyses::ReconstructedParticle::get_e(Jet)")
              .Define("pT_jets",  "FCCAnalyses::ReconstructedParticle::get_pt(Jet)")
              .Define("eta_jets",  "FCCAnalyses::ReconstructedParticle::get_eta(Jet)")

              # #selected jets above a pT threshold of 20 GeV
              .Define("selected_jets", "FCCAnalyses::ReconstructedParticle::sel_pt(20.)(Jet)") 
              .Define("n_jets_sel",  "FCCAnalyses::ReconstructedParticle::get_n(selected_jets)")
              .Define("px_jets_sel",  "FCCAnalyses::ReconstructedParticle::get_px(selected_jets)")
              .Define("py_jets_sel",  "FCCAnalyses::ReconstructedParticle::get_py(selected_jets)")
              .Define("pz_jets_sel",  "FCCAnalyses::ReconstructedParticle::get_pz(selected_jets)")
              .Define("E_jets_sel",  "FCCAnalyses::ReconstructedParticle::get_e(selected_jets)")
              .Define("pT_jets_sel",  "FCCAnalyses::ReconstructedParticle::get_pt(selected_jets)")
              .Define("eta_jets_sel",  "FCCAnalyses::ReconstructedParticle::get_eta(selected_jets)")

              # #b-tagged jets:
              .Alias("Jet3","Jet#3.index") 

              #LOOSE WP
              .Define("b_tagged_jets_loose", "AnalysisFCChh::get_tagged_jets(Jet, Jet3, ParticleIDs, ParticleIDs_0, 0)") #bit 0 = loose WP, see: https://github.com/delphes/delphes/blob/master/cards/FCC/scenarios/FCChh_I.tcl
              .Define("n_b_jets_loose", "FCCAnalyses::ReconstructedParticle::get_n(b_tagged_jets_loose)")
              .Define("px_b_jets_loose",  "FCCAnalyses::ReconstructedParticle::get_px(b_tagged_jets_loose)")
              .Define("py_b_jets_loose",  "FCCAnalyses::ReconstructedParticle::get_py(b_tagged_jets_loose)")
              .Define("pz_b_jets_loose",  "FCCAnalyses::ReconstructedParticle::get_pz(b_tagged_jets_loose)")
              .Define("E_b_jets_loose",  "FCCAnalyses::ReconstructedParticle::get_e(b_tagged_jets_loose)")
              .Define("pT_b_jets_loose",  "FCCAnalyses::ReconstructedParticle::get_pt(b_tagged_jets_loose)")
              .Define("eta_b_jets_loose",  "FCCAnalyses::ReconstructedParticle::get_eta(b_tagged_jets_loose)")

              #MEDIUM WP
              .Define("b_tagged_jets_medium", "AnalysisFCChh::get_tagged_jets(Jet, Jet3, ParticleIDs, ParticleIDs_0, 1)") #bit 1 = medium WP, see: https://github.com/delphes/delphes/blob/master/cards/FCC/scenarios/FCChh_I.tcl
              .Define("n_b_jets_medium", "FCCAnalyses::ReconstructedParticle::get_n(b_tagged_jets_medium)")
              .Define("px_b_jets_medium",  "FCCAnalyses::ReconstructedParticle::get_px(b_tagged_jets_medium)")
              .Define("py_b_jets_medium",  "FCCAnalyses::ReconstructedParticle::get_py(b_tagged_jets_medium)")
              .Define("pz_b_jets_medium",  "FCCAnalyses::ReconstructedParticle::get_pz(b_tagged_jets_medium)")
              .Define("E_b_jets_medium",  "FCCAnalyses::ReconstructedParticle::get_e(b_tagged_jets_medium)")
              .Define("pT_b_jets_medium",  "FCCAnalyses::ReconstructedParticle::get_pt(b_tagged_jets_medium)")
              .Define("eta_b_jets_medium",  "FCCAnalyses::ReconstructedParticle::get_eta(b_tagged_jets_medium)")

              #TIGHT WP
              .Define("b_tagged_jets_tight", "AnalysisFCChh::get_tagged_jets(Jet, Jet3, ParticleIDs, ParticleIDs_0, 2)") #bit 2 = tight WP, see: https://github.com/delphes/delphes/blob/master/cards/FCC/scenarios/FCChh_I.tcl
              .Define("n_b_jets_tight", "FCCAnalyses::ReconstructedParticle::get_n(b_tagged_jets_tight)")
              .Define("px_b_jets_tight",  "FCCAnalyses::ReconstructedParticle::get_px(b_tagged_jets_tight)")
              .Define("py_b_jets_tight",  "FCCAnalyses::ReconstructedParticle::get_py(b_tagged_jets_tight)")
              .Define("pz_b_jets_tight",  "FCCAnalyses::ReconstructedParticle::get_pz(b_tagged_jets_tight)")
              .Define("E_b_jets_tight",  "FCCAnalyses::ReconstructedParticle::get_e(b_tagged_jets_tight)")
              .Define("pT_b_jets_tight",  "FCCAnalyses::ReconstructedParticle::get_pt(b_tagged_jets_tight)")
              .Define("eta_b_jets_tight",  "FCCAnalyses::ReconstructedParticle::get_eta(b_tagged_jets_tight)")

              #Tau-jets, here also 3 WP

              #LOOSE WP
              .Define("tau_tagged_jets_loose", "AnalysisFCChh::get_tau_jets(Jet, Jet3, ParticleIDs, ParticleIDs_0, 0)") #bit 0 = loose WP, see: https://github.com/delphes/delphes/blob/master/cards/FCC/scenarios/FCChh_I.tcl
              .Define("n_tau_jets_loose", "FCCAnalyses::ReconstructedParticle::get_n(tau_tagged_jets_loose)")
              .Define("px_tau_jets_loose", "FCCAnalyses::ReconstructedParticle::get_px(tau_tagged_jets_loose)")
              .Define("py_tau_jets_loose", "FCCAnalyses::ReconstructedParticle::get_py(tau_tagged_jets_loose)")
              .Define("pz_tau_jets_loose", "FCCAnalyses::ReconstructedParticle::get_pz(tau_tagged_jets_loose)")
              .Define("E_tau_jets_loose", "FCCAnalyses::ReconstructedParticle::get_e(tau_tagged_jets_loose)")
              .Define("pT_tau_jets_loose", "FCCAnalyses::ReconstructedParticle::get_pt(tau_tagged_jets_loose)")
              .Define("eta_tau_jets_loose", "FCCAnalyses::ReconstructedParticle::get_eta(tau_tagged_jets_loose)")

              #MEDIUM WP
              .Define("tau_tagged_jets_medium", "AnalysisFCChh::get_tau_jets(Jet, Jet3, ParticleIDs, ParticleIDs_0, 1)") #bit 1 = medium WP, see: https://github.com/delphes/delphes/blob/master/cards/FCC/scenarios/FCChh_I.tcl
              .Define("n_tau_jets_medium", "FCCAnalyses::ReconstructedParticle::get_n(tau_tagged_jets_medium)")
              .Define("px_tau_jets_medium", "FCCAnalyses::ReconstructedParticle::get_px(tau_tagged_jets_medium)")
              .Define("py_tau_jets_medium", "FCCAnalyses::ReconstructedParticle::get_py(tau_tagged_jets_medium)")
              .Define("pz_tau_jets_medium", "FCCAnalyses::ReconstructedParticle::get_pz(tau_tagged_jets_medium)")
              .Define("E_tau_jets_medium", "FCCAnalyses::ReconstructedParticle::get_e(tau_tagged_jets_medium)")
              .Define("pT_tau_jets_medium", "FCCAnalyses::ReconstructedParticle::get_pt(tau_tagged_jets_medium)")
              .Define("eta_tau_jets_medium", "FCCAnalyses::ReconstructedParticle::get_eta(tau_tagged_jets_medium)")


              #TIGHT WP
              .Define("tau_tagged_jets_tight", "AnalysisFCChh::get_tau_jets(Jet, Jet3, ParticleIDs, ParticleIDs_0, 2)") #bit 2 = tight WP, see: https://github.com/delphes/delphes/blob/master/cards/FCC/scenarios/FCChh_I.tcl
              .Define("n_tau_jets_tight", "FCCAnalyses::ReconstructedParticle::get_n(tau_tagged_jets_tight)")
              .Define("px_tau_jets_tight", "FCCAnalyses::ReconstructedParticle::get_px(tau_tagged_jets_tight)")
              .Define("py_tau_jets_tight", "FCCAnalyses::ReconstructedParticle::get_py(tau_tagged_jets_tight)")
              .Define("pz_tau_jets_tight", "FCCAnalyses::ReconstructedParticle::get_pz(tau_tagged_jets_tight)")
              .Define("E_tau_jets_tight", "FCCAnalyses::ReconstructedParticle::get_e(tau_tagged_jets_tight)")
              .Define("pT_tau_jets_tight", "FCCAnalyses::ReconstructedParticle::get_pt(tau_tagged_jets_tight)")
              .Define("eta_tau_jets_tight", "FCCAnalyses::ReconstructedParticle::get_eta(tau_tagged_jets_tight)")

              ########################################### ELECTRONS ########################################### 

              #pre-isolation:
              .Alias("ElectronNoIso", "ElectronNoIso#0.index")
              .Define("electrons_noiso",  "FCCAnalyses::ReconstructedParticle::get(ElectronNoIso, ReconstructedParticles)")
              .Define("n_electrons_noiso",  "FCCAnalyses::ReconstructedParticle::get_n(electrons_noiso)")
              .Define("px_electrons_noiso",  "FCCAnalyses::ReconstructedParticle::get_px(electrons_noiso)")
              .Define("py_electrons_noiso",  "FCCAnalyses::ReconstructedParticle::get_py(electrons_noiso)")
              .Define("pz_electrons_noiso",  "FCCAnalyses::ReconstructedParticle::get_pz(electrons_noiso)")
              .Define("E_electrons_noiso",  "FCCAnalyses::ReconstructedParticle::get_e(electrons_noiso)")
              .Define("pT_electrons_noiso",  "FCCAnalyses::ReconstructedParticle::get_pt(electrons_noiso)")
              .Define("eta_electrons_noiso",  "FCCAnalyses::ReconstructedParticle::get_eta(electrons_noiso)")

              # isolation variable
              .Define("isoVar_electrons_noiso", "ElectronNoIso_IsolationVar")

              #all isolated 
              .Alias("Electron0", "Electron#0.index")
              .Define("electrons",  "FCCAnalyses::ReconstructedParticle::get(Electron0, ReconstructedParticles)")
              .Define("n_electrons",  "FCCAnalyses::ReconstructedParticle::get_n(electrons)")
              .Define("px_electrons",  "FCCAnalyses::ReconstructedParticle::get_px(electrons)")
              .Define("py_electrons",  "FCCAnalyses::ReconstructedParticle::get_py(electrons)")
              .Define("pz_electrons",  "FCCAnalyses::ReconstructedParticle::get_pz(electrons)")
              .Define("E_electrons",  "FCCAnalyses::ReconstructedParticle::get_e(electrons)")
              .Define("pT_electrons",  "FCCAnalyses::ReconstructedParticle::get_pt(electrons)")
              .Define("eta_electrons",  "FCCAnalyses::ReconstructedParticle::get_eta(electrons)")

              #isolated from b-jets - using the medium WP only for now!!
              .Define("electrons_iso", "AnalysisFCChh::sel_isolated(electrons, b_tagged_jets_medium)")
              .Define("n_electrons_iso", "FCCAnalyses::ReconstructedParticle::get_n(electrons_iso)")
              .Define("px_electrons_iso",  "FCCAnalyses::ReconstructedParticle::get_px(electrons_iso)")
              .Define("py_electrons_iso",  "FCCAnalyses::ReconstructedParticle::get_py(electrons_iso)")
              .Define("pz_electrons_iso",  "FCCAnalyses::ReconstructedParticle::get_pz(electrons_iso)")
              .Define("E_electrons_iso",  "FCCAnalyses::ReconstructedParticle::get_e(electrons_iso)")
              .Define("pT_electrons_iso",  "FCCAnalyses::ReconstructedParticle::get_pt(electrons_iso)")
              .Define("eta_electrons_iso",  "FCCAnalyses::ReconstructedParticle::get_eta(electrons_iso)")

              #selection: isolated and above the pT threshold
              .Define("selected_electrons", "FCCAnalyses::ReconstructedParticle::sel_pt(10.)(electrons_iso)")
              .Define("n_electrons_sel", "FCCAnalyses::ReconstructedParticle::get_n(selected_electrons)") 
              .Define("px_electrons_sel",  "FCCAnalyses::ReconstructedParticle::get_px(selected_electrons)")
              .Define("py_electrons_sel",  "FCCAnalyses::ReconstructedParticle::get_py(selected_electrons)")
              .Define("pz_electrons_sel",  "FCCAnalyses::ReconstructedParticle::get_pz(selected_electrons)")
              .Define("E_electrons_sel",  "FCCAnalyses::ReconstructedParticle::get_e(selected_electrons)")
              .Define("pT_electrons_sel",  "FCCAnalyses::ReconstructedParticle::get_pt(selected_electrons)")
              .Define("eta_electrons_sel",  "FCCAnalyses::ReconstructedParticle::get_eta(selected_electrons)")

              ########################################### MUONS ########################################### 
              #pre-isolation
              .Alias("MuonNoIso", "MuonNoIso#0.index")
              .Define("muons_noiso",  "FCCAnalyses::ReconstructedParticle::get(MuonNoIso, ReconstructedParticles)") 
              .Define("n_muons_noiso",  "FCCAnalyses::ReconstructedParticle::get_n(muons_noiso)")
              .Define("px_muons_noiso",  "FCCAnalyses::ReconstructedParticle::get_px(muons_noiso)")
              .Define("py_muons_noiso",  "FCCAnalyses::ReconstructedParticle::get_py(muons_noiso)")
              .Define("pz_muons_noiso",  "FCCAnalyses::ReconstructedParticle::get_pz(muons_noiso)")
              .Define("E_muons_noiso",  "FCCAnalyses::ReconstructedParticle::get_e(muons_noiso)")
              .Define("pT_muons_noiso",  "FCCAnalyses::ReconstructedParticle::get_pt(muons_noiso)")
              .Define("eta_muons_noiso",  "FCCAnalyses::ReconstructedParticle::get_eta(muons_noiso)")

              # isolation variable
              .Define("isoVar_muons_noiso", "MuonNoIso_IsolationVar")

              # all isolated
              .Alias("Muon0", "Muon#0.index")
              .Define("muons",  "FCCAnalyses::ReconstructedParticle::get(Muon0, ReconstructedParticles)") 
              .Define("n_muons",  "FCCAnalyses::ReconstructedParticle::get_n(muons)")
              .Define("px_muons",  "FCCAnalyses::ReconstructedParticle::get_px(muons)")
              .Define("py_muons",  "FCCAnalyses::ReconstructedParticle::get_py(muons)")
              .Define("pz_muons",  "FCCAnalyses::ReconstructedParticle::get_pz(muons)")
              .Define("E_muons",  "FCCAnalyses::ReconstructedParticle::get_e(muons)")
              .Define("pT_muons",  "FCCAnalyses::ReconstructedParticle::get_pt(muons)")
              .Define("eta_muons",  "FCCAnalyses::ReconstructedParticle::get_eta(muons)")

              #isolated from b-jets - using the medium WP only for now!!
              .Define("muons_iso", "AnalysisFCChh::sel_isolated(muons, b_tagged_jets_medium)")
              .Define("n_muons_iso", "FCCAnalyses::ReconstructedParticle::get_n(muons_iso)")
              .Define("px_muons_iso",  "FCCAnalyses::ReconstructedParticle::get_px(muons_iso)")
              .Define("py_muons_iso",  "FCCAnalyses::ReconstructedParticle::get_py(muons_iso)")
              .Define("pz_muons_iso",  "FCCAnalyses::ReconstructedParticle::get_pz(muons_iso)")
              .Define("E_muons_iso",  "FCCAnalyses::ReconstructedParticle::get_e(muons_iso)")
              .Define("pT_muons_iso",  "FCCAnalyses::ReconstructedParticle::get_pt(muons_iso)")
              .Define("eta_muons_iso",  "FCCAnalyses::ReconstructedParticle::get_eta(muons_iso)")

              #selection: isolated and above the pT threshold
              .Define("selected_muons", "FCCAnalyses::ReconstructedParticle::sel_pt(10.)(muons_iso)")
              .Define("n_muons_sel", "FCCAnalyses::ReconstructedParticle::get_n(selected_muons)") 
              .Define("px_muons_sel",  "FCCAnalyses::ReconstructedParticle::get_px(selected_muons)")
              .Define("py_muons_sel",  "FCCAnalyses::ReconstructedParticle::get_py(selected_muons)")
              .Define("pz_muons_sel",  "FCCAnalyses::ReconstructedParticle::get_pz(selected_muons)")
              .Define("E_muons_sel",  "FCCAnalyses::ReconstructedParticle::get_e(selected_muons)")
              .Define("pT_muons_sel",  "FCCAnalyses::ReconstructedParticle::get_pt(selected_muons)")
              .Define("eta_muons_sel",  "FCCAnalyses::ReconstructedParticle::get_eta(selected_muons)")


              ########################################### PHOTONS ########################################### 
              #pre-isolation
              .Alias("PhotonNoIso", "PhotonNoIso#0.index") 
              .Define("photons_noiso",  "FCCAnalyses::ReconstructedParticle::get(PhotonNoIso, ReconstructedParticles)") 
              .Define("n_photons_noiso",  "FCCAnalyses::ReconstructedParticle::get_n(photons_noiso)") 
              .Define("px_photons_noiso",  "FCCAnalyses::ReconstructedParticle::get_px(photons_noiso)")
              .Define("py_photons_noiso",  "FCCAnalyses::ReconstructedParticle::get_py(photons_noiso)")
              .Define("pz_photons_noiso",  "FCCAnalyses::ReconstructedParticle::get_pz(photons_noiso)")
              .Define("E_photons_noiso",  "FCCAnalyses::ReconstructedParticle::get_e(photons_noiso)")
              .Define("pT_photons_noiso",  "FCCAnalyses::ReconstructedParticle::get_pt(photons_noiso)")
              .Define("eta_photons_noiso",  "FCCAnalyses::ReconstructedParticle::get_eta(photons_noiso)")

              # isolation variable
              .Define("isoVar_photons_noiso", "PhotonNoIso_IsolationVar")

              #all, after isolation

              .Alias("Photon0", "Photon#0.index") 
              .Define("photons",  "FCCAnalyses::ReconstructedParticle::get(Photon0, ReconstructedParticles)") 
              .Define("n_photons",  "FCCAnalyses::ReconstructedParticle::get_n(photons)") 
              .Define("px_photons",  "FCCAnalyses::ReconstructedParticle::get_px(photons)")
              .Define("py_photons",  "FCCAnalyses::ReconstructedParticle::get_py(photons)")
              .Define("pz_photons",  "FCCAnalyses::ReconstructedParticle::get_pz(photons)")
              .Define("E_photons",  "FCCAnalyses::ReconstructedParticle::get_e(photons)")
              .Define("pT_photons",  "FCCAnalyses::ReconstructedParticle::get_pt(photons)")
              .Define("eta_photons",  "FCCAnalyses::ReconstructedParticle::get_eta(photons)")

              #isolated from b-jets - using the medium WP only for now!!
              .Define("photons_iso", "AnalysisFCChh::sel_isolated(photons, b_tagged_jets_medium)")
              .Define("n_photons_iso", "FCCAnalyses::ReconstructedParticle::get_n(photons_iso)")
              .Define("px_photons_iso",  "FCCAnalyses::ReconstructedParticle::get_px(photons_iso)")
              .Define("py_photons_iso",  "FCCAnalyses::ReconstructedParticle::get_py(photons_iso)")
              .Define("pz_photons_iso",  "FCCAnalyses::ReconstructedParticle::get_pz(photons_iso)")
              .Define("E_photons_iso",  "FCCAnalyses::ReconstructedParticle::get_e(photons_iso)")
              .Define("pT_photons_iso",  "FCCAnalyses::ReconstructedParticle::get_pt(photons_iso)")
              .Define("eta_photons_iso",  "FCCAnalyses::ReconstructedParticle::get_eta(photons_iso)")

              #selection: isolated and above the pT threshold
              .Define("selected_photons", "FCCAnalyses::ReconstructedParticle::sel_pt(20.)(photons_iso)")
              .Define("n_photons_sel", "FCCAnalyses::ReconstructedParticle::get_n(selected_photons)") 
              .Define("px_photons_sel",  "FCCAnalyses::ReconstructedParticle::get_px(selected_photons)")
              .Define("py_photons_sel",  "FCCAnalyses::ReconstructedParticle::get_py(selected_photons)")
              .Define("pz_photons_sel",  "FCCAnalyses::ReconstructedParticle::get_pz(selected_photons)")
              .Define("E_photons_sel",  "FCCAnalyses::ReconstructedParticle::get_e(selected_photons)")
              .Define("pT_photons_sel",  "FCCAnalyses::ReconstructedParticle::get_pt(selected_photons)")
              .Define("eta_photons_sel",  "FCCAnalyses::ReconstructedParticle::get_eta(selected_photons)")

              ########################################### LINK BACK TO MC PARTICLES ########################################### 
              #currently not used
              # .Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
              # .Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
              # .Define('RP_MC_index', "ReconstructedParticle2MC::getRP2MC_index(MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles)") 



              ########################################### MET ########################################### 
              .Define("MET", "FCCAnalyses::ReconstructedParticle::get_pt(MissingET)")
              .Define("MET_x", "FCCAnalyses::ReconstructedParticle::get_px(MissingET)")
              .Define("MET_y", "FCCAnalyses::ReconstructedParticle::get_py(MissingET)")
              .Define("MET_phi", "FCCAnalyses::ReconstructedParticle::get_phi(MissingET)")

              ########################################### EVENT WIDE KINEMATIC VARIABLES########################################### 
              # OLD TESTERS - TO REMOVE?
              #H(bb) system - using the medium WP b-jets only for now!! -> if the events has < 2 bjets these variables do not get filled!
              # .Define("bb_pairs_unmerged", "AnalysisFCChh::getPairs(b_tagged_jets_medium)") #currently gets only leading pT pair, as a RecoParticlePair
              # #get angles between the two bs:
              # .Define("dPhi_bb", "AnalysisFCChh::get_angularDist_pair(bb_pairs_unmerged, TString(\"dPhi\")) ")
              # .Define("dEta_bb", "AnalysisFCChh::get_angularDist_pair(bb_pairs_unmerged, TString(\"dEta\")) ")
              # .Define("dR_bb", "AnalysisFCChh::get_angularDist_pair(bb_pairs_unmerged, TString(\"dR\")) ")

              # #then merge the bb pair into one object and get its kinematic properties
              # .Define("bb_pairs", "AnalysisFCChh::merge_pairs(bb_pairs_unmerged)") #merge into one object to access inv masses etc
              # .Define("m_bb", "FCCAnalyses::ReconstructedParticle::get_mass(bb_pairs)")
              # .Define("px_Hbb_cand",  "FCCAnalyses::ReconstructedParticle::get_px(bb_pairs)")
              # .Define("py_Hbb_cand",  "FCCAnalyses::ReconstructedParticle::get_py(bb_pairs)")
              # .Define("pz_Hbb_cand",  "FCCAnalyses::ReconstructedParticle::get_pz(bb_pairs)")
              # .Define("E_Hbb_cand",  "FCCAnalyses::ReconstructedParticle::get_e(bb_pairs)")
              # .Define("pT_Hbb_cand",  "FCCAnalyses::ReconstructedParticle::get_pt(bb_pairs)")
              # .Define("eta_Hbb_cand",  "FCCAnalyses::ReconstructedParticle::get_eta(bb_pairs)")

              # #H(WW->emu+MET) if it exists,  if there is no emu pair, doesnt get filled 
              # .Define("OS_emu_pairs", "AnalysisFCChh::getDFOSPairs(selected_electrons, selected_muons)") #returns all possible pairs sorted by pT of the elecs and muons
              # .Define("n_OS_emu_pairs", "AnalysisFCChh::get_n_pairs(OS_emu_pairs)")

              # ##select the leading pT DFOS pair only
              # .Define("OS_emu_pair_lead", "AnalysisFCChh::get_first_pair(OS_emu_pairs)")
              # .Define("H_2l_cand", "AnalysisFCChh::merge_pairs(OS_emu_pair_lead)")
              # .Define("m_ll", "FCCAnalyses::ReconstructedParticle::get_mass(H_2l_cand)")
              # .Define("dPhi_ll_MET", "AnalysisFCChh::get_angularDist_MET(H_2l_cand, MissingET, TString(\"dPhi\")) ")

              ########################################### MC PARTICLES ########################################### 

              #all MC particles
              .Define("mc_particles", "Particle")
              .Alias("mc_parents", "Particle#0")
              .Alias("mc_daughters", "Particle#1")


               )

       
       #additional (truth based) information to filter for bbWW(lvlv) events for the efficiency checks: 
        if "hhbbww" in out_name :
              df2 = (df2
                     .Define("truth_leps_from_higgs", "AnalysisFCChh::getLepsFromW(mc_particles, mc_parents)") 
                     .Define("n_truth_leps_from_HWW", "MCParticle::get_n(truth_leps_from_higgs)") 
                     .Define("pdgID_truth_leps_from_HWW", "MCParticle::get_pdg(truth_leps_from_higgs)")
                     .Define("pT_truth_leps_from_HWW", "MCParticle::get_pt(truth_leps_from_higgs)")
                     .Define("eta_truth_leps_from_HWW", "MCParticle::get_eta(truth_leps_from_higgs)")
                     .Define("E_truth_leps_from_HWW", "MCParticle::get_e(truth_leps_from_higgs)")
                     .Define("phi_truth_leps_from_HWW", "MCParticle::get_phi(truth_leps_from_higgs)")
                     .Define("P_truth_leps_from_HWW", "MCParticle::get_p(truth_leps_from_higgs)")

                     # # .Filter("n_truth_leps_from_HWW == 2", "WW_dilep_filter")  #dont use yet, can check if BRs are correct that way! 

                     # #Adapted truth matching code to be able to extract the isoVar as computed by Delphes: Truth matching returns indices rather than the particles
                     #  #electrons
                     # .Define("indices_truthmatched_reco_ele_from_higgs_noiso", "AnalysisFCChh::find_truth_to_reco_matches_indices(truth_leps_from_higgs, electrons_noiso, 11)")
                     # # .Define("isoVar_truthmatched_ele_from_higgs", "AnalysisFCChh::get(indices_truthmatched_reco_ele_from_higgs_noiso, ElectronNoIso_IsolationVar)")
                     # .Define("truthmatched_reco_ele_from_higgs_noiso", "AnalysisFCChh::get(indices_truthmatched_reco_ele_from_higgs_noiso, electrons_noiso)") #getting the actual objects!
                     # .Define("n_truthmatched_ele_from_HWW", "ReconstructedParticle::get_n(truthmatched_reco_ele_from_higgs_noiso)") 
                     # .Define("pT_truthmatched_ele_from_HWW", "ReconstructedParticle::get_pt(truthmatched_reco_ele_from_higgs_noiso)") 
                     # .Define("eta_truthmatched_ele_from_HWW", "ReconstructedParticle::get_eta(truthmatched_reco_ele_from_higgs_noiso)") 
                     # .Define("phi_truthmatched_ele_from_HWW", "ReconstructedParticle::get_phi(truthmatched_reco_ele_from_higgs_noiso)") 
                     # .Define("P_truthmatched_ele_from_HWW", "ReconstructedParticle::get_p(truthmatched_reco_ele_from_higgs_noiso)") 
                     # .Define("E_truthmatched_ele_from_HWW", "ReconstructedParticle::get_e(truthmatched_reco_ele_from_higgs_noiso)") 

                     # #same for muons 
                     # .Define("indices_truthmatched_reco_mu_from_higgs_noiso", "AnalysisFCChh::find_truth_to_reco_matches_indices(truth_leps_from_higgs, muons_noiso, 13)")
                     # # .Define("isoVar_truthmatched_mu_from_higgs", "AnalysisFCChh::get(indices_truthmatched_reco_mu_from_higgs_noiso, MuonNoIso_IsolationVar)")
                     # .Define("truthmatched_reco_mu_from_higgs_noiso", "AnalysisFCChh::get(indices_truthmatched_reco_mu_from_higgs_noiso, muons_noiso)") #getting the actual objects!
                     # .Define("n_truthmatched_mu_from_HWW", "ReconstructedParticle::get_n(truthmatched_reco_mu_from_higgs_noiso)") 
                     # .Define("pT_truthmatched_mu_from_HWW", "ReconstructedParticle::get_pt(truthmatched_reco_mu_from_higgs_noiso)") 
                     # .Define("eta_truthmatched_mu_from_HWW", "ReconstructedParticle::get_eta(truthmatched_reco_mu_from_higgs_noiso)") 
                     # .Define("phi_truthmatched_mu_from_HWW", "ReconstructedParticle::get_phi(truthmatched_reco_mu_from_higgs_noiso)") 
                     # .Define("P_truthmatched_mu_from_HWW", "ReconstructedParticle::get_p(truthmatched_reco_mu_from_higgs_noiso)") 
                     # .Define("E_truthmatched_mu_from_HWW", "ReconstructedParticle::get_e(truthmatched_reco_mu_from_higgs_noiso)") 

                     # #merge the collections: 
                     # .Define("truthmatched_reco_leps_from_higgs_noiso", "ReconstructedParticle::merge(truthmatched_reco_ele_from_higgs_noiso, truthmatched_reco_mu_from_higgs_noiso)")
                     # .Define("n_truthmatched_leps_from_HWW_noiso", "ReconstructedParticle::get_n(truthmatched_reco_leps_from_higgs_noiso)")
                     # .Define("pT_truthmatched_leps_from_HWW_noiso",  "FCCAnalyses::ReconstructedParticle::get_pt(truthmatched_reco_leps_from_higgs_noiso)")
                     # .Define("eta_truthmatched_leps_from_HWW_noiso",  "FCCAnalyses::ReconstructedParticle::get_eta(truthmatched_reco_leps_from_higgs_noiso)") 
                     # .Define("E_truthmatched_leps_from_HWW_noiso",  "FCCAnalyses::ReconstructedParticle::get_e(truthmatched_reco_leps_from_higgs_noiso)") 
                     # .Define("phi_truthmatched_leps_from_HWW_noiso",  "FCCAnalyses::ReconstructedParticle::get_phi(truthmatched_reco_leps_from_higgs_noiso)") 
                     # .Define("P_truthmatched_leps_from_HWW_noiso",  "FCCAnalyses::ReconstructedParticle::get_p(truthmatched_reco_leps_from_higgs_noiso)") 

                     )

        ########################################### PRE-SELECT BASED ON THE LEPTON PAIR ########################################### 
        if flavour == "DFOS":

          df_DFOS_leps = (df2

              .Define("OS_ll_pairs", "AnalysisFCChh::getDFOSPairs(selected_electrons, selected_muons)") #returns all possible pairs sorted by pT of the elecs and muons
              .Define("n_OS_ll_pairs", "AnalysisFCChh::get_n_pairs(OS_ll_pairs)")

              # #select the leading pT DFOS pair only
              .Define("OS_ll_pair_lead", "AnalysisFCChh::get_first_pair(OS_ll_pairs)")


            )

          # filter - pre-selection
          df_filter_2l = df_DFOS_leps.Filter("n_OS_ll_pairs > 0")

          df_filter_2b = df_filter_2l.Filter("n_b_jets_medium > 1")

          # df_leps = df_DFOS_leps

        elif flavour == "SFOS":

          df_SFOS_leps = (df2

              #for SF analysis need to pair electrons and muons separately at first
              .Define("OS_ee_pairs", "AnalysisFCChh::getOSPairs(selected_muons)") 
              .Define("OS_mm_pairs", "AnalysisFCChh::getOSPairs(selected_electrons)") 
              .Define("n_OS_ll_pairs", "AnalysisFCChh::get_n_pairs(OS_ee_pairs)+AnalysisFCChh::get_n_pairs(OS_mm_pairs)")

              # #select the leading pT SFOS pair only
              .Define("OS_ll_pair_lead", "AnalysisFCChh::getLeadingPair(OS_ee_pairs, OS_mm_pairs)")

            )

          # df_leps = df_SFOS_leps

          #filter - pre-selection
          df_filter_2l = df_SFOS_leps.Filter("n_OS_ll_pairs > 0")

          df_filter_2b = df_filter_2l.Filter("n_b_jets_medium > 1")



          ########################################### FILL EVENT WIDE VARIABLES ########################################### 

        df_out = (df_filter_2b
        # df_out = (df_leps

          #H(bb) system
          .Define("bb_pairs_unmerged", "AnalysisFCChh::getPairs(b_tagged_jets_medium)") #currently gets only leading pT pair, as a RecoParticlePair
          #get angles between the two bs:
          .Define("dPhi_bb", "AnalysisFCChh::get_angularDist_pair(bb_pairs_unmerged, TString(\"dPhi\")) ")
          .Define("dEta_bb", "AnalysisFCChh::get_angularDist_pair(bb_pairs_unmerged, TString(\"dEta\")) ")
          .Define("dR_bb", "AnalysisFCChh::get_angularDist_pair(bb_pairs_unmerged, TString(\"dR\")) ")

          #then merge the bb pair into one object and get its kinematic properties
          .Define("bb_pairs", "AnalysisFCChh::merge_pairs(bb_pairs_unmerged)") #merge into one objects to access inv masses etc
          .Define("m_bb", "ReconstructedParticle::get_mass(bb_pairs)")
          .Define("px_Hbb_cand",  "ReconstructedParticle::get_px(bb_pairs)")
          .Define("py_Hbb_cand",  "ReconstructedParticle::get_py(bb_pairs)")
          .Define("pz_Hbb_cand",  "ReconstructedParticle::get_pz(bb_pairs)")
          .Define("E_Hbb_cand",  "ReconstructedParticle::get_e(bb_pairs)")
          .Define("pT_Hbb_cand",  "ReconstructedParticle::get_pt(bb_pairs)")
          .Define("eta_Hbb_cand",  "ReconstructedParticle::get_eta(bb_pairs)")

          #H(2l+MET) system

          #angles between the two leptons
          .Define("dPhi_ll", "AnalysisFCChh::get_angularDist_pair(OS_ll_pair_lead, TString(\"dPhi\")) ")
          .Define("dEta_ll", "AnalysisFCChh::get_angularDist_pair(OS_ll_pair_lead, TString(\"dEta\")) ")
          .Define("dR_ll", "AnalysisFCChh::get_angularDist_pair(OS_ll_pair_lead, TString(\"dR\")) ")

          #merge the pair to access invariant mass, pt etc
          .Define("H_2l_cand", "AnalysisFCChh::merge_pairs(OS_ll_pair_lead)")
          # .Define("m_ll", "ReconstructedParticle::get_mass(H_2l_cand)")
          .Define("m_ll", "ReconstructedParticle::get_mass(H_2l_cand)")
          .Define("px_ll", "ReconstructedParticle::get_px(H_2l_cand)")
          .Define("py_ll", "ReconstructedParticle::get_py(H_2l_cand)")
          .Define("pz_ll", "ReconstructedParticle::get_pz(H_2l_cand)")
          .Define("E_ll", "ReconstructedParticle::get_e(H_2l_cand)")
          .Define("pT_ll", "ReconstructedParticle::get_pt(H_2l_cand)")
          .Define("eta_ll", "ReconstructedParticle::get_eta(H_2l_cand)")

          # # #angular variables in the 2l+MET system:
          .Define("dPhi_ll_MET", "AnalysisFCChh::get_angularDist_MET(H_2l_cand, MissingET, TString(\"dPhi\")) ")
          .Define("dEta_ll_MET", "AnalysisFCChh::get_angularDist_MET(H_2l_cand, MissingET, TString(\"dEta\"))")
          .Define("dR_ll_MET", "AnalysisFCChh::get_angularDist_MET(H_2l_cand, MissingET, TString(\"dR\"))")

          # #invariant masses, as inspired by H(tautau) analysis -> to double check if calculations are correct!

          # #to get the colinear masses for the Htautau decay, need to split the ll pair again
          .Define("selected_OS_lep1", "AnalysisFCChh::get_first_from_pair(OS_ll_pair_lead)")
          .Define("pT_pair_lep1", "ReconstructedParticle::get_pt(selected_OS_lep1)")
          .Define("px_pair_lep1", "ReconstructedParticle::get_px(selected_OS_lep1)")
          .Define("py_pair_lep1", "ReconstructedParticle::get_py(selected_OS_lep1)")
          .Define("pz_pair_lep1", "ReconstructedParticle::get_pz(selected_OS_lep1)")
          .Define("E_pair_lep1", "ReconstructedParticle::get_e(selected_OS_lep1)")
          .Define("eta_pair_lep1", "ReconstructedParticle::get_eta(selected_OS_lep1)")

          .Define("selected_OS_lep2", "AnalysisFCChh::get_second_from_pair(OS_ll_pair_lead)")
          .Define("pT_pair_lep2", "ReconstructedParticle::get_pt(selected_OS_lep2)")
          .Define("px_pair_lep2", "ReconstructedParticle::get_px(selected_OS_lep2)")
          .Define("py_pair_lep2", "ReconstructedParticle::get_py(selected_OS_lep2)")
          .Define("pz_pair_lep2", "ReconstructedParticle::get_pz(selected_OS_lep2)")
          .Define("E_pair_lep2", "ReconstructedParticle::get_e(selected_OS_lep2)")
          .Define("eta_pair_lep2", "ReconstructedParticle::get_eta(selected_OS_lep2)")

          #test getting mT of the subleading lepton for bbWW vs bbtautau separation
          .Define("mT_lep1", "AnalysisFCChh::get_mT(selected_OS_lep1, MissingET)")
          .Define("mT_lep2", "AnalysisFCChh::get_mT(selected_OS_lep2, MissingET)")
          # .Define("mT_lep2_new", "AnalysisFCChh::get_mT_new(selected_OS_lep2, MissingET)") #different fct agreed in test cases

          .Define("x_lep1", "AnalysisFCChh::get_x_fraction(selected_OS_lep1, MissingET)")
          .Define("x_lep2", "AnalysisFCChh::get_x_fraction(selected_OS_lep2, MissingET)")
          .Define("m_collinear", "AnalysisFCChh::get_mtautau_col(H_2l_cand, x_lep1, x_lep2)")


          #variables merging the H(2l+MET) and H(bb) systems

          #vector sum of ll and etmiss
          .Define("H_2l_MET_cand", "AnalysisFCChh::merge_parts_TLVs(H_2l_cand, MissingET)")
          .Define("sum_pT_ll_MET", "ReconstructedParticle::get_pt(H_2l_MET_cand)")

          #HT variables (see ATLAS bblvlv paper arXiv:1908.06765)
          .Define("HT2_H2l_plus_Hbb", "AnalysisFCChh::get_HT2(H_2l_MET_cand, bb_pairs)")
          .Define("HT_MET_bb_2l", "AnalysisFCChh::get_HT_wInv(MissingET, OS_ll_pair_lead, bb_pairs_unmerged)")
          .Define("HT2_ratio", "AnalysisFCChh::get_HT2_ratio(HT2_H2l_plus_Hbb, HT_MET_bb_2l)")

          #similarly, get met significance
          .Define("HT_true", "AnalysisFCChh::get_HT_true(OS_ll_pair_lead, bb_pairs_unmerged)")
          .Define("MET_significance", "AnalysisFCChh::get_MET_significance(MissingET, HT_true)")

          # # #to reconstruct variables of the HH system, merge the visible and reconstructed decay products, the bb and ll pair:
          .Define("HH_vis", "AnalysisFCChh::merge_parts_TLVs(H_2l_cand, bb_pairs)")
          .Define("mT_bbll_MET", "AnalysisFCChh::get_mT(HH_vis, MissingET)")
          .Define("m_pseudo_HH", "AnalysisFCChh::get_m_pseudo(HH_vis, MissingET)")
          .Define("mT_pseudo_HH", "AnalysisFCChh::get_mT_pseudo(HH_vis, MissingET)")
          .Define("mT2_HH", "AnalysisFCChh::get_mT2(H_2l_cand, bb_pairs, MissingET)")
          .Define("mT2_HH_125", "AnalysisFCChh::get_mT2_125(H_2l_cand, bb_pairs, MissingET)")

          .Define("mT2_H_2l_MET", "AnalysisFCChh::get_mT2(selected_OS_lep1, selected_OS_lep2, MissingET)")

          #truth MET the other way round: pT of the vectorial sum of the main objects in the hard scattering, here bb-pair and emu
          .Define("pT_HH_vis", "ReconstructedParticle::get_pt(HH_vis)")
          .Define("eta_HH_vis", "ReconstructedParticle::get_eta(HH_vis)")
          .Define("px_HH_vis", "ReconstructedParticle::get_px(HH_vis)")
          .Define("py_HH_vis", "ReconstructedParticle::get_py(HH_vis)")
          .Define("pz_HH_vis", "ReconstructedParticle::get_pz(HH_vis)")
          .Define("E_HH_vis", "ReconstructedParticle::get_e(HH_vis)")

          ## combining one lepton and one bjet each, to see if compatible with top-decay:
          .Define("lb_pairs", "AnalysisFCChh::make_lb_pairing(OS_ll_pair_lead, bb_pairs_unmerged)")
          .Define("mlb_reco", "AnalysisFCChh::get_mlb_reco(lb_pairs)")
          .Define("mlb_reco_MET", "AnalysisFCChh::get_mlb_MET_reco(lb_pairs, MissingET)")
          .Define("dPhi_lb", "AnalysisFCChh::get_angularDist_pair(lb_pairs, TString(\"dPhi\")) ") #note this returns it only for the first pair!
          .Define("dEta_lb", "AnalysisFCChh::get_angularDist_pair(lb_pairs, TString(\"dEta\")) ")
          .Define("dR_lb", "AnalysisFCChh::get_angularDist_pair(lb_pairs, TString(\"dR\")) ")

          #pzeta variables used in CMS tautau analyses
          .Define("pzeta_vis", "AnalysisFCChh::get_pzeta_vis(OS_ll_pair_lead)")
          .Define("pzeta_miss", "AnalysisFCChh::get_pzeta_miss(OS_ll_pair_lead, MissingET)")
          .Define("dzeta_85", "AnalysisFCChh::get_dzeta(pzeta_miss, pzeta_vis)")

          #angles between the two Higgses
          .Define("dPhi_HH", "AnalysisFCChh::get_angularDist_MET(bb_pairs, H_2l_MET_cand, TString(\"dPhi\")) ")
          .Define("dEta_HH", "AnalysisFCChh::get_angularDist_MET(bb_pairs, H_2l_MET_cand, TString(\"dEta\"))")
          .Define("dR_HH", "AnalysisFCChh::get_angularDist_MET(bb_pairs, H_2l_MET_cand, TString(\"dR\"))")

          )

  
        return df_out

    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list.

    #REMEMBER TO ADD ALL THE OUTPUT BRANCHES TO THIS LIST 

    def output(out_name):
        branchList = [ 
                      "weight",
                      # Jets before overlap removal:
                      "n_jets_noiso", "px_jets_noiso", "py_jets_noiso", "pz_jets_noiso", "E_jets_noiso", "pT_jets_noiso", "eta_jets_noiso",
                      "n_b_jets_loose_noiso", "px_b_jets_loose_noiso", "py_b_jets_loose_noiso", "pz_b_jets_loose_noiso", "E_b_jets_loose_noiso", "pT_b_jets_loose_noiso", "eta_b_jets_loose_noiso",
                      # Jets:
                      "n_jets", "px_jets", "py_jets", "pz_jets", "E_jets", "pT_jets", "eta_jets",
                      "n_jets_sel", "px_jets_sel", "py_jets_sel", "pz_jets_sel", "E_jets_sel", "pT_jets_sel", "eta_jets_sel",
                      # B-jets:
                      "n_b_jets_loose", "px_b_jets_loose", "py_b_jets_loose", "pz_b_jets_loose", "E_b_jets_loose", "pT_b_jets_loose", "eta_b_jets_loose",
                      "n_b_jets_medium", "px_b_jets_medium", "py_b_jets_medium", "pz_b_jets_medium", "E_b_jets_medium", "pT_b_jets_medium", "eta_b_jets_medium",
                      "n_b_jets_tight", "px_b_jets_tight", "py_b_jets_tight", "pz_b_jets_tight", "E_b_jets_tight", "pT_b_jets_tight", "eta_b_jets_tight",
                      # Tau-jets:
                      "n_tau_jets_loose", "px_tau_jets_loose", "py_tau_jets_loose", "pz_tau_jets_loose", "E_tau_jets_loose", "pT_tau_jets_loose", "eta_tau_jets_loose",
                      "n_tau_jets_medium", "px_tau_jets_medium", "py_tau_jets_medium", "pz_tau_jets_medium", "E_tau_jets_medium", "pT_tau_jets_medium", "eta_tau_jets_medium",
                      "n_tau_jets_tight", "px_tau_jets_tight", "py_tau_jets_tight", "pz_tau_jets_tight", "E_tau_jets_tight", "pT_tau_jets_tight", "eta_tau_jets_tight",
                      # Electrons:
                      "n_electrons_noiso", "px_electrons_noiso", "py_electrons_noiso", "pz_electrons_noiso", "E_electrons_noiso", "pT_electrons_noiso", "eta_electrons_noiso",
                      "n_electrons", "px_electrons", "py_electrons", "pz_electrons", "E_electrons", "pT_electrons", "eta_electrons",
                      "n_electrons_iso", "px_electrons_iso", "py_electrons_iso", "pz_electrons_iso", "E_electrons_iso", "pT_electrons_iso", "eta_electrons_iso",
                      "n_electrons_sel", "px_electrons_sel", "py_electrons_sel", "pz_electrons_sel", "E_electrons_sel", "pT_electrons_sel", "eta_electrons_sel",
                      # Muons:
                      "n_muons_noiso", "px_muons_noiso", "py_muons_noiso", "pz_muons_noiso", "E_muons_noiso", "pT_muons_noiso", "eta_muons_noiso",
                      "n_muons", "px_muons", "py_muons", "pz_muons", "E_muons", "pT_muons", "eta_muons",
                      "n_muons_iso", "px_muons_iso", "py_muons_iso", "pz_muons_iso", "E_muons_iso", "pT_muons_iso", "eta_muons_iso",
                      "n_muons_sel", "px_muons_sel", "py_muons_sel", "pz_muons_sel", "E_muons_sel", "pT_muons_sel", "eta_muons_sel",
                      # Photons:
                      "n_photons_noiso", "px_photons_noiso", "py_photons_noiso", "pz_photons_noiso", "E_photons_noiso", "pT_photons_noiso", "eta_photons_noiso",
                      "n_photons", "px_photons", "py_photons", "pz_photons", "E_photons", "pT_photons", "eta_photons",
                      "n_photons_iso", "px_photons_iso", "py_photons_iso", "pz_photons_iso", "E_photons_iso", "pT_photons_iso", "eta_photons_iso",
                      "n_photons_sel", "px_photons_sel", "py_photons_sel", "pz_photons_sel", "E_photons_sel", "pT_photons_sel", "eta_photons_sel",
                      #isolation variables:
                      "isoVar_electrons_noiso", "isoVar_muons_noiso", "isoVar_photons_noiso",
                      # ETMiss:
                      "MET","MET_x", "MET_y", "MET_phi",
                      # # Hbb decay:
                      # "m_bb", "px_Hbb_cand", "py_Hbb_cand", "pz_Hbb_cand", "E_Hbb_cand", "pT_Hbb_cand", "eta_Hbb_cand", "dPhi_bb", "dEta_bb", "dR_bb",
                      # #H(WW->emu+MET) decay:
                      # "n_OS_emu_pairs", "m_ll", "dPhi_ll_MET",
                      # #Hbb decay:
                      "m_bb", "px_Hbb_cand", "py_Hbb_cand", "pz_Hbb_cand", "E_Hbb_cand", "pT_Hbb_cand", "eta_Hbb_cand",
                      "dPhi_bb", "dEta_bb", "dR_bb",

                      ### H(2l+MET) decay:
                      "n_OS_ll_pairs",
                      "dPhi_ll", "dEta_ll", "dR_ll", "m_ll", 
                      "pT_ll", "px_ll", "py_ll", "pz_ll", "E_ll", "eta_ll",
                      "dPhi_ll_MET", "dEta_ll_MET", "dR_ll_MET",
                      "sum_pT_ll_MET", 

                      # #HT variables, for the full HH system
                      "HT2_H2l_plus_Hbb", "HT_MET_bb_2l", "HT2_ratio",
                      "HT_true", "MET_significance",

                      # #separate the leptons from the DFOS pair
                      "pT_pair_lep1", "px_pair_lep1", "py_pair_lep1", "pz_pair_lep1", "E_pair_lep1", "eta_pair_lep1",
                      "pT_pair_lep2", "px_pair_lep2", "py_pair_lep2", "pz_pair_lep2", "E_pair_lep2", "eta_pair_lep2",
                      "mT_lep1", "mT_lep2",

                      # #colinear mass
                      "x_lep1", "x_lep2", "m_collinear",

                      # #pseudo masses
                      "mT_bbll_MET", "m_pseudo_HH", "mT_pseudo_HH", "mT2_HH", "mT2_HH_125", "mT2_H_2l_MET",

                      #properties of the vectorial sum of bbemu
                      "pT_HH_vis", "eta_HH_vis", "px_HH_vis", "py_HH_vis", "pz_HH_vis", "E_HH_vis",

                      #ttbar suppression
                      "mlb_reco", "mlb_reco_MET", "dPhi_lb", "dEta_lb", "dR_lb",

                      #pzeta variables
                      "pzeta_vis", "pzeta_miss", "dzeta_85",

                      #angle between higgs candidates
                      "dPhi_HH", "dEta_HH", "dR_HH"
            
        ]

        if "hhbbww" in out_name:
              #truth leptons
              branchList.append("n_truth_leps_from_HWW")
              branchList.append("pdgID_truth_leps_from_HWW")
              branchList.append("pT_truth_leps_from_HWW")
              branchList.append("eta_truth_leps_from_HWW")
              branchList.append("E_truth_leps_from_HWW")
              branchList.append("phi_truth_leps_from_HWW")
              branchList.append("P_truth_leps_from_HWW")
              # #reco leptons matched to truth in cone 0.1, before isolation
              # branchList.append("n_truthmatched_leps_from_HWW_noiso")
              # branchList.append("pT_truthmatched_leps_from_HWW_noiso")
              # branchList.append("eta_truthmatched_leps_from_HWW_noiso")
              # branchList.append("E_truthmatched_leps_from_HWW_noiso")
              # branchList.append("phi_truthmatched_leps_from_HWW_noiso")
              # branchList.append("P_truthmatched_leps_from_HWW_noiso")
              # #reco leptons matched to truth in cone 0.2, before isolation
              # branchList.append("n_truthmatched_leps_from_HWW_noiso_dr02")
              # branchList.append("pT_truthmatched_leps_from_HWW_noiso_dr02")
              # branchList.append("eta_truthmatched_leps_from_HWW_noiso_dr02")
              # branchList.append("E_truthmatched_leps_from_HWW_noiso_dr02")
              # branchList.append("phi_truthmatched_leps_from_HWW_noiso_dr02")
              # branchList.append("P_truthmatched_leps_from_HWW_noiso_dr02")
              # #reco leptons matched to truth in cone 0.1, after isolation
              # branchList.append("n_truthmatched_leps_from_HWW")
              # branchList.append("pT_truthmatched_leps_from_HWW")
              # branchList.append("eta_truthmatched_leps_from_HWW")
              # branchList.append("E_truthmatched_leps_from_HWW")
              # branchList.append("phi_truthmatched_leps_from_HWW")
              # branchList.append("P_truthmatched_leps_from_HWW")

              # #split truth - reco matching for the isoVar extraction:
              # #electrons
              # # branchList.append("isoVar_truthmatched_ele_from_higgs")
              # branchList.append("n_truthmatched_ele_from_HWW")
              # branchList.append("pT_truthmatched_ele_from_HWW")
              # branchList.append("eta_truthmatched_ele_from_HWW")
              # branchList.append("phi_truthmatched_ele_from_HWW")
              # branchList.append("P_truthmatched_ele_from_HWW")
              # branchList.append("E_truthmatched_ele_from_HWW")
              # #muons
              # # branchList.append("isoVar_truthmatched_mu_from_higgs")
              # branchList.append("n_truthmatched_mu_from_HWW")
              # branchList.append("pT_truthmatched_mu_from_HWW")
              # branchList.append("eta_truthmatched_mu_from_HWW")
              # branchList.append("phi_truthmatched_mu_from_HWW")
              # branchList.append("P_truthmatched_mu_from_HWW")
              # branchList.append("E_truthmatched_mu_from_HWW")




        return branchList


# local test: fccanalysis run analysis_bb2lmet.py --nevents 100 - also switch runBatch to False

