#for batch submission
processList = {
    "pwp8_pp_hh_lambda100_5f_hhbbww":{'chunks':200, 'output':"FCChh_EvtGen_pwp8_pp_hh_lambda100_5f_hhbbww"}, #put the name of your input file here (without .root), the output file will have the same name
    "pwp8_pp_hh_lambda100_5f_hhbbaa":{'chunks':200, 'output':"FCChh_EvtGen_pwp8_pp_hh_lambda100_5f_hhbbaa"}, #put the name of your input file here (without .root), the output file will have the same name
    "pwp8_pp_hh_lambda100_5f_hhbbzz_4l":{'chunks':200, 'output':"FCChh_EvtGen_pwp8_pp_hh_lambda100_5f_hhbbzz_4l"}, #put the name of your input file here (without .root), the output file will have the same name
}

#for local testing:
# processList= {
#     # "pwp8_pp_hh_lambda100_5f_hhbbww":{'output':"FCChh_EvtGen_pwp8_pp_hh_lambda100_5f_hhbbww"}, #put the name of your input file here (without .root), the output file will have the same name
#     # "pwp8_pp_hh_lambda100_5f_hhbbaa":{'output':"FCChh_EvtGen_pwp8_pp_hh_lambda100_5f_hhbbaa"}, #put the name of your input file here (without .root), the output file will have the same name
#     "pwp8_pp_hh_lambda100_5f_hhbbzz_4l":{'output':"FCChh_EvtGen_pwp8_pp_hh_lambda100_5f_hhbbzz_4l"}, #put the name of your input file here (without .root), the output file will have the same name
# }

#Mandatory: input directory when not running over centrally produced edm4hep events. 
inputDir    = "/eos/experiment/fcc/hh/generation/DelphesEvents/fcc_v05_scenarioI/" #your directory with the input file
# inputDir    = "/eos/user/b/bistapf/FCChh_EvtGen/" #your directory with the input file

#Optional: output directory, default is local dir
outputDir   = "/eos/user/b/bistapf/FCChh_EvtGen/FCCAnalysis_ntuples_noIso/"

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
              ########################################### JETS ########################################### 
              # #all jets
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

              .Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
              .Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
              .Define('RP_MC_index', "ReconstructedParticle2MC::getRP2MC_index(MCRecoAssociations0,MCRecoAssociations1,ReconstructedParticles)") 



              ########################################### MET ########################################### 
              .Define("MET", "FCCAnalyses::ReconstructedParticle::get_pt(MissingET)")
              .Define("MET_x", "FCCAnalyses::ReconstructedParticle::get_px(MissingET)")
              .Define("MET_y", "FCCAnalyses::ReconstructedParticle::get_py(MissingET)")
              .Define("MET_phi", "FCCAnalyses::ReconstructedParticle::get_phi(MissingET)")

              ########################################### EVENT WIDE KINEMATIC VARIABLES########################################### 

              #H(bb) system - using the medium WP b-jets only for now!! -> if the events has < 2 bjets these variables do not get filled!
              .Define("bb_pairs_unmerged", "AnalysisFCChh::getPairs(b_tagged_jets_medium)") #currently gets only leading pT pair, as a RecoParticlePair
              #get angles between the two bs:
              .Define("dPhi_bb", "AnalysisFCChh::get_angularDist_pair(bb_pairs_unmerged, TString(\"dPhi\")) ")
              .Define("dEta_bb", "AnalysisFCChh::get_angularDist_pair(bb_pairs_unmerged, TString(\"dEta\")) ")
              .Define("dR_bb", "AnalysisFCChh::get_angularDist_pair(bb_pairs_unmerged, TString(\"dR\")) ")

              #then merge the bb pair into one object and get its kinematic properties
              .Define("bb_pairs", "AnalysisFCChh::merge_pairs(bb_pairs_unmerged)") #merge into one object to access inv masses etc
              .Define("m_bb", "FCCAnalyses::ReconstructedParticle::get_mass(bb_pairs)")
              .Define("px_Hbb_cand",  "FCCAnalyses::ReconstructedParticle::get_px(bb_pairs)")
              .Define("py_Hbb_cand",  "FCCAnalyses::ReconstructedParticle::get_py(bb_pairs)")
              .Define("pz_Hbb_cand",  "FCCAnalyses::ReconstructedParticle::get_pz(bb_pairs)")
              .Define("E_Hbb_cand",  "FCCAnalyses::ReconstructedParticle::get_e(bb_pairs)")
              .Define("pT_Hbb_cand",  "FCCAnalyses::ReconstructedParticle::get_pt(bb_pairs)")
              .Define("eta_Hbb_cand",  "FCCAnalyses::ReconstructedParticle::get_eta(bb_pairs)")

              #H(yy) if it exists, if there are no 2 selected photons, doesnt get filled 
              .Define("yy_pairs_unmerged", "AnalysisFCChh::getPairs(selected_photons)")
              .Define("yy_pairs", "AnalysisFCChh::merge_pairs(yy_pairs_unmerged)")
              .Define("m_yy", "FCCAnalyses::ReconstructedParticle::get_mass(yy_pairs)")

              #H(tau_h, tau_h) if it exists, if there are no 2 tau-jets, doesnt get filled -> using medium WP only !!
              .Define("tauhtauh_pairs_unmerged", "AnalysisFCChh::getPairs(tau_tagged_jets_medium)")
              .Define("tauhtauh_pairs", "AnalysisFCChh::merge_pairs(tauhtauh_pairs_unmerged)")
              .Define("m_tauhtauh", "FCCAnalyses::ReconstructedParticle::get_mass(tauhtauh_pairs)")

              #H(WW->emu+MET) if it exists,  if there is no emu pair, doesnt get filled 
              .Define("OS_emu_pairs", "AnalysisFCChh::getDFOSPairs(selected_electrons, selected_muons)") #returns all possible pairs sorted by pT of the elecs and muons
              .Define("n_OS_emu_pairs", "AnalysisFCChh::get_n_pairs(OS_emu_pairs)")

              ##select the leading pT DFOS pair only
              .Define("OS_emu_pair_lead", "AnalysisFCChh::get_first_pair(OS_emu_pairs)")
              .Define("H_2l_cand", "AnalysisFCChh::merge_pairs(OS_emu_pair_lead)")
              .Define("m_ll", "FCCAnalyses::ReconstructedParticle::get_mass(H_2l_cand)")
              .Define("dPhi_ll_MET", "AnalysisFCChh::get_angularDist_MET(H_2l_cand, MissingET, TString(\"dPhi\")) ")

              #second H(bb) system for 4b signals - if event has < 4 b-jets does not get filled - using medium WP
              .Define("sub_bb_pairs_unmerged", "AnalysisFCChh::getPair_sublead(b_tagged_jets_medium)") #just using the b-jets in order of pT
              .Define("sub_b_pairs", "AnalysisFCChh::merge_pairs(sub_bb_pairs_unmerged)") #merge into one object to access inv masses etc
              .Define("m_bb_sub", "FCCAnalyses::ReconstructedParticle::get_mass(sub_b_pairs)")


              ########################################### MC PARTICLES ########################################### 

              #all MC particles
              .Define("mc_particles", "Particle")
              .Alias("mc_parents", "Particle#0")
              .Alias("mc_daughters", "Particle#1")

              #Photons
              .Define("MC_photons", ROOT.MCParticle.sel_pdgID(22, 0),["Particle"])
              .Define("stable_MC_photons", ROOT.MCParticle.sel_genStatus(1),["MC_photons"])
              .Define("n_MC_photons",  "FCCAnalyses::MCParticle::get_n(stable_MC_photons)")
              .Define("pT_MC_photons",  "FCCAnalyses::MCParticle::get_pt(stable_MC_photons)")
              .Define("eta_MC_photons",  "FCCAnalyses::MCParticle::get_eta(stable_MC_photons)")

              #photons with pT > 1 GeV
              .Define("MC_photons_selected", "FCCAnalyses::MCParticle::sel_pt(1.)(MC_photons)") 
              .Define("n_MC_photons_sel",  "FCCAnalyses::MCParticle::get_n(MC_photons_selected)")
              .Define("pT_MC_photons_sel",  "FCCAnalyses::MCParticle::get_pt(MC_photons_selected)")
              .Define("eta_MC_photons_sel",  "FCCAnalyses::MCParticle::get_eta(MC_photons_selected)")


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

                     #Check how many matched leptons in the no-iso collections
                     .Define("truthmatched_reco_leps_from_higgs_noiso", "AnalysisFCChh::find_true_signal_leps_reco_matches(truth_leps_from_higgs, electrons_noiso, muons_noiso)")
                     .Define("n_truthmatched_leps_from_HWW_noiso", "ReconstructedParticle::get_n(truthmatched_reco_leps_from_higgs_noiso)")
                     .Define("pT_truthmatched_leps_from_HWW_noiso",  "FCCAnalyses::ReconstructedParticle::get_pt(truthmatched_reco_leps_from_higgs_noiso)")
                     .Define("eta_truthmatched_leps_from_HWW_noiso",  "FCCAnalyses::ReconstructedParticle::get_eta(truthmatched_reco_leps_from_higgs_noiso)") 
                     .Define("E_truthmatched_leps_from_HWW_noiso",  "FCCAnalyses::ReconstructedParticle::get_e(truthmatched_reco_leps_from_higgs_noiso)") 
                     .Define("phi_truthmatched_leps_from_HWW_noiso",  "FCCAnalyses::ReconstructedParticle::get_phi(truthmatched_reco_leps_from_higgs_noiso)") 

                     #try with larger dR cone to see if it changes things:
                     .Define("truthmatched_reco_leps_from_higgs_noiso_dr02", "AnalysisFCChh::find_true_signal_leps_reco_matches(truth_leps_from_higgs, electrons_noiso, muons_noiso, 0.2)")
                     .Define("n_truthmatched_leps_from_HWW_noiso_dr02", "ReconstructedParticle::get_n(truthmatched_reco_leps_from_higgs_noiso_dr02)")
                     .Define("pT_truthmatched_leps_from_HWW_noiso_dr02",  "FCCAnalyses::ReconstructedParticle::get_pt(truthmatched_reco_leps_from_higgs_noiso_dr02)")
                     .Define("eta_truthmatched_leps_from_HWW_noiso_dr02",  "FCCAnalyses::ReconstructedParticle::get_eta(truthmatched_reco_leps_from_higgs_noiso_dr02)") 
                     .Define("E_truthmatched_leps_from_HWW_noiso_dr02",  "FCCAnalyses::ReconstructedParticle::get_e(truthmatched_reco_leps_from_higgs_noiso_dr02)") 
                     .Define("phi_truthmatched_leps_from_HWW_noiso_dr02",  "FCCAnalyses::ReconstructedParticle::get_phi(truthmatched_reco_leps_from_higgs_noiso_dr02)") 

                     #Check how many matched leptons in the collections after iso
                     .Define("truthmatched_reco_leps_from_higgs", "AnalysisFCChh::find_true_signal_leps_reco_matches(truth_leps_from_higgs, electrons, muons)")
                     .Define("n_truthmatched_leps_from_HWW", "ReconstructedParticle::get_n(truthmatched_reco_leps_from_higgs)") 
                     .Define("pT_truthmatched_leps_from_HWW",  "FCCAnalyses::ReconstructedParticle::get_pt(truthmatched_reco_leps_from_higgs)")
                     .Define("eta_truthmatched_leps_from_HWW",  "FCCAnalyses::ReconstructedParticle::get_eta(truthmatched_reco_leps_from_higgs)") 
                     .Define("E_truthmatched_leps_from_HWW",  "FCCAnalyses::ReconstructedParticle::get_e(truthmatched_reco_leps_from_higgs)") 
                     .Define("phi_truthmatched_leps_from_HWW",  "FCCAnalyses::ReconstructedParticle::get_phi(truthmatched_reco_leps_from_higgs)") 

                     # .Filter("n_truth_leps_from_HWW == 2", "WW_dilep_filter")  #dont use yet, can check if BRs are correct that way! 
                     )

       #additional (truth based) information to filter for bbyy events for the efficiency checks: 
        if "hhbbaa" in out_name :
              df2 = (df2
                     .Define("truth_ys_from_higgs", "AnalysisFCChh::getPhotonsFromH(mc_particles, mc_parents)")
                     .Define("n_truth_ys_from_higgs", "MCParticle::get_n(truth_ys_from_higgs)") 
                     .Define("pT_truth_ys_from_higgs", "MCParticle::get_pt(truth_ys_from_higgs)")
                     .Define("eta_truth_ys_from_higgs", "MCParticle::get_eta(truth_ys_from_higgs)")
                     .Define("E_truth_ys_from_higgs", "MCParticle::get_e(truth_ys_from_higgs)")
                     .Define("phi_truth_ys_from_higgs", "MCParticle::get_phi(truth_ys_from_higgs)")

                     #Check how many matched photons in the no-iso collection
                     .Define("truthmatched_reco_ys_from_higgs_noiso", "AnalysisFCChh::find_reco_matches(truth_ys_from_higgs, photons_noiso)")
                     .Define("n_truthmatched_ys_from_higgs_noiso", "ReconstructedParticle::get_n(truthmatched_reco_ys_from_higgs_noiso)")
                     .Define("pT_truthmatched_ys_from_higgs_noiso",  "FCCAnalyses::ReconstructedParticle::get_pt(truthmatched_reco_ys_from_higgs_noiso)")
                     .Define("eta_truthmatched_ys_from_higgs_noiso",  "FCCAnalyses::ReconstructedParticle::get_eta(truthmatched_reco_ys_from_higgs_noiso)") 
                     .Define("E_truthmatched_ys_from_higgs_noiso",  "FCCAnalyses::ReconstructedParticle::get_e(truthmatched_reco_ys_from_higgs_noiso)") 
                     .Define("phi_truthmatched_ys_from_higgs_noiso",  "FCCAnalyses::ReconstructedParticle::get_phi(truthmatched_reco_ys_from_higgs_noiso)") 


                     #Check how many matched leptons in the collections after iso
                     .Define("truthmatched_reco_ys_from_higgs", "AnalysisFCChh::find_reco_matches(truth_ys_from_higgs, photons)")
                     .Define("n_truthmatched_ys_from_higgs", "ReconstructedParticle::get_n(truthmatched_reco_ys_from_higgs)") 
                     .Define("pT_truthmatched_ys_from_higgs",  "FCCAnalyses::ReconstructedParticle::get_pt(truthmatched_reco_ys_from_higgs)")
                     .Define("eta_truthmatched_ys_from_higgs",  "FCCAnalyses::ReconstructedParticle::get_eta(truthmatched_reco_ys_from_higgs)") 
                     .Define("E_truthmatched_ys_from_higgs",  "FCCAnalyses::ReconstructedParticle::get_e(truthmatched_reco_ys_from_higgs)") 
                     .Define("phi_truthmatched_ys_from_higgs",  "FCCAnalyses::ReconstructedParticle::get_phi(truthmatched_reco_ys_from_higgs)") 
                     
                     )

        #additional (truth based) information to filter bbZZ(4l) events for the efficiency checks: 
        if "hhbbzz_4l" in out_name :
              df2 = (df2
                     .Define("truth_leps_from_higgs", "AnalysisFCChh::getLepsFromZ(mc_particles, mc_parents)") 
                     .Define("n_truth_leps_from_HZZ", "MCParticle::get_n(truth_leps_from_higgs)") 
                     .Define("pdgID_truth_leps_from_HZZ", "MCParticle::get_pdg(truth_leps_from_higgs)")
                     .Define("pT_truth_leps_from_HZZ", "MCParticle::get_pt(truth_leps_from_higgs)")
                     .Define("eta_truth_leps_from_HZZ", "MCParticle::get_eta(truth_leps_from_higgs)")
                     .Define("E_truth_leps_from_HZZ", "MCParticle::get_e(truth_leps_from_higgs)")
                     .Define("phi_truth_leps_from_HZZ", "MCParticle::get_phi(truth_leps_from_higgs)")

                     #Check how many matched leptons in the no-iso collections
                     .Define("truthmatched_reco_leps_from_higgs_noiso", "AnalysisFCChh::find_true_signal_leps_reco_matches(truth_leps_from_higgs, electrons_noiso, muons_noiso)")
                     .Define("n_truthmatched_leps_from_HZZ_noiso", "ReconstructedParticle::get_n(truthmatched_reco_leps_from_higgs_noiso)")
                     .Define("pT_truthmatched_leps_from_HZZ_noiso",  "FCCAnalyses::ReconstructedParticle::get_pt(truthmatched_reco_leps_from_higgs_noiso)")
                     .Define("eta_truthmatched_leps_from_HZZ_noiso",  "FCCAnalyses::ReconstructedParticle::get_eta(truthmatched_reco_leps_from_higgs_noiso)") 
                     .Define("E_truthmatched_leps_from_HZZ_noiso",  "FCCAnalyses::ReconstructedParticle::get_e(truthmatched_reco_leps_from_higgs_noiso)") 
                     .Define("phi_truthmatched_leps_from_HZZ_noiso",  "FCCAnalyses::ReconstructedParticle::get_phi(truthmatched_reco_leps_from_higgs_noiso)") 

                     #Check how many matched leptons in the collections after iso
                     .Define("truthmatched_reco_leps_from_higgs", "AnalysisFCChh::find_true_signal_leps_reco_matches(truth_leps_from_higgs, electrons, muons)")
                     .Define("n_truthmatched_leps_from_HZZ", "ReconstructedParticle::get_n(truthmatched_reco_leps_from_higgs)") 
                     .Define("pT_truthmatched_leps_from_HZZ",  "FCCAnalyses::ReconstructedParticle::get_pt(truthmatched_reco_leps_from_higgs)")
                     .Define("eta_truthmatched_leps_from_HZZ",  "FCCAnalyses::ReconstructedParticle::get_eta(truthmatched_reco_leps_from_higgs)") 
                     .Define("E_truthmatched_leps_from_HZZ",  "FCCAnalyses::ReconstructedParticle::get_e(truthmatched_reco_leps_from_higgs)")
                     .Define("phi_truthmatched_leps_from_HZZ",  "FCCAnalyses::ReconstructedParticle::get_phi(truthmatched_reco_leps_from_higgs)")
                     ) 

        return df2

    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list.

    #REMEMBER TO ADD ALL THE OUTPUT BRANCHES TO THIS LIST 

    def output(out_name):
        branchList = [
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
                      # ETMiss:
                      "MET","MET_x", "MET_y", "MET_phi",
                      # Hbb decay:
                      "m_bb", "px_Hbb_cand", "py_Hbb_cand", "pz_Hbb_cand", "E_Hbb_cand", "pT_Hbb_cand", "eta_Hbb_cand", "dPhi_bb", "dEta_bb", "dR_bb",
                      "m_bb_sub", #mass of subleading pair 
                      #Hyy decay:
                      "m_yy",
                      #H(tau_h, tau_h) decay:
                      "m_tauhtauh",
                      #H(WW->emu+MET) decay:
                      "n_OS_emu_pairs", "m_ll", "dPhi_ll_MET",
                      # MC particles:
                      'n_MC_photons', 'pT_MC_photons', 'eta_MC_photons',
                      'n_MC_photons_sel', 'pT_MC_photons_sel', 'eta_MC_photons_sel',
            
        ]

        if "hhbbww" in out_name:
              #truth leptons
              branchList.append("n_truth_leps_from_HWW")
              branchList.append("pdgID_truth_leps_from_HWW")
              branchList.append("pT_truth_leps_from_HWW")
              branchList.append("eta_truth_leps_from_HWW")
              branchList.append("E_truth_leps_from_HWW")
              branchList.append("phi_truth_leps_from_HWW")
              #reco leptons matched to truth in cone 0.1, before isolation
              branchList.append("n_truthmatched_leps_from_HWW_noiso")
              branchList.append("pT_truthmatched_leps_from_HWW_noiso")
              branchList.append("eta_truthmatched_leps_from_HWW_noiso")
              branchList.append("E_truthmatched_leps_from_HWW_noiso")
              branchList.append("phi_truthmatched_leps_from_HWW_noiso")
              #reco leptons matched to truth in cone 0.2, before isolation
              branchList.append("n_truthmatched_leps_from_HWW_noiso_dr02")
              branchList.append("pT_truthmatched_leps_from_HWW_noiso_dr02")
              branchList.append("eta_truthmatched_leps_from_HWW_noiso_dr02")
              branchList.append("E_truthmatched_leps_from_HWW_noiso_dr02")
              branchList.append("phi_truthmatched_leps_from_HWW_noiso_dr02")
              #reco leptons matched to truth in cone 0.1, after isolation
              branchList.append("n_truthmatched_leps_from_HWW")
              branchList.append("pT_truthmatched_leps_from_HWW")
              branchList.append("eta_truthmatched_leps_from_HWW")
              branchList.append("E_truthmatched_leps_from_HWW")
              branchList.append("phi_truthmatched_leps_from_HWW")

        if "hhbbaa" in out_name:
              #truth photons from higgs
              branchList.append("n_truth_ys_from_higgs")
              branchList.append("pT_truth_ys_from_higgs")
              branchList.append("eta_truth_ys_from_higgs")
              branchList.append("E_truth_ys_from_higgs")
              branchList.append("phi_truth_ys_from_higgs")
              #reco photons matched to truth in cone 0.1, before isolation
              branchList.append("n_truthmatched_ys_from_higgs_noiso")
              branchList.append("pT_truthmatched_ys_from_higgs_noiso")
              branchList.append("eta_truthmatched_ys_from_higgs_noiso")
              branchList.append("E_truthmatched_ys_from_higgs_noiso")
              branchList.append("phi_truthmatched_ys_from_higgs_noiso")
              #reco photons matched to truth in cone 0.1, after isolation
              branchList.append("n_truthmatched_ys_from_higgs")
              branchList.append("pT_truthmatched_ys_from_higgs")
              branchList.append("eta_truthmatched_ys_from_higgs")
              branchList.append("E_truthmatched_ys_from_higgs")
              branchList.append("phi_truthmatched_ys_from_higgs")

        if "hhbbzz_4l" in out_name:
              #truth leptons
              branchList.append("n_truth_leps_from_HZZ")
              branchList.append("pdgID_truth_leps_from_HZZ")
              branchList.append("pT_truth_leps_from_HZZ")
              branchList.append("eta_truth_leps_from_HZZ")
              branchList.append("E_truth_leps_from_HZZ")
              branchList.append("phi_truth_leps_from_HZZ")
              #reco leptons matched to truth in cone 0.1, before isolation
              branchList.append("n_truthmatched_leps_from_HZZ_noiso")
              branchList.append("pT_truthmatched_leps_from_HZZ_noiso")
              branchList.append("eta_truthmatched_leps_from_HZZ_noiso")
              branchList.append("E_truthmatched_leps_from_HZZ_noiso")
              #reco leptons matched to truth in cone 0.1, after isolation
              branchList.append("n_truthmatched_leps_from_HZZ")
              branchList.append("pT_truthmatched_leps_from_HZZ")
              branchList.append("eta_truthmatched_leps_from_HZZ")
              branchList.append("E_truthmatched_leps_from_HZZ")


        return branchList


# local test: fccanalysis run analysis_noiso.py --nevents 100 - also switch runBatch to False

