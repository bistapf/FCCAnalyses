#NOTE: isovar branches temporarily commented out!!


processList = {
     #"pwp8_pp_hh_lambda100_5f_hhbbaa":{'chunks':200, 'output':"FCChh_EvtGen_pwp8_pp_hh_lambda100_5f_hhbbaa"}, #put the name of your input file here (witho\ut .root), the output file will have the same name
     #"pwp8_pp_hh_lambda240_5f_hhbbaa":{'chunks':200, 'output':"FCChh_EvtGen_pwp8_pp_hh_lambda240_5f_hhbbaa"},
     #"pwp8_pp_hh_lambda300_5f_hhbbaa":{'chunks':200, 'output':"FCChh_EvtGen_pwp8_pp_hh_lambda300_5f_hhbbaa"},
     #"pwp8_pp_hh_lambda000_5f_hhbbaa":{'chunks':200, 'output':"FCChh_EvtGen_pwp8_pp_hh_lambda000_5f_hhbbaa"},
     "mgp8_pp_h012j_5f_haa":{'chunks':500, 'output':"FCChh_EvtGen_mgp8_pp_h012j_5f_haa"},
     "mgp8_pp_vbf_h01j_5f_haa":{'chunks':500, 'output':"FCChh_EvtGen_mgp8_pp_vbf_h01j_5f_haa"},
     "mgp8_pp_tth01j_5f_haa":{'chunks':500, 'output':"FCChh_EvtGen_mgp8_pp_tth01j_5f_haa"},
     "mgp8_pp_vh012j_5f_haa":{'chunks':500, 'output':"FCChh_EvtGen_mgp8_pp_vh012j_5f_haa"},
     #"mgp8_pp_jjaa_5f":{'chunks':500, 'output':"FCChh_EvtGen_mgp8_pp_jjaa_5f"},
     #"mgp8_pp_tt012j_5f": {'chunks':200, 'output':"FCChh_EvtGen_mgp8_pp_tt012j_5f"}

}


#for batch submission
#processList = {
#     "pwp8_pp_hh_lambda100_5f_hhbbaa":{'chunks':500, 'output':"FCChh_EvtGen_pwp8_pp_hh_lambda100_5f_hhbbaa"}, #put the name of your input file here (without .root), the output file will have the same name
#     "pwp8_pp_hh_lambda240_5f_hhbbaa":{'chunks':500, 'output':"FCChh_EvtGen_pwp8_pp_hh_lambda240_5f_hhbbaa"},
#     "pwp8_pp_hh_lambda300_5f_hhbbaa":{'chunks':500, 'output':"FCChh_EvtGen_pwp8_pp_hh_lambda300_5f_hhbbaa"},
#     "pwp8_pp_hh_lambda000_5f_hhbbaa":{'chunks':500, 'output':"FCChh_EvtGen_pwp8_pp_hh_lambda000_5f_hhbbaa"},
     #"mgp8_pp_h012j_5f_haa":{#'chunks':500, 'output':"FCChh_EvtGen_mgp8_pp_h012j_5f_haa"},
#     "mgp8_pp_vbf_h01j_5f":{'chunks':500, 'output':"FCChh_EvtGen_mgp8_pp_vbf_h01j_5f"},
#     "mgp8_pp_tth01j_5f_haa/events_000000143":{#'chunks':500, 
#'output':"FCChh_EvtGen_mgp8_pp_tth01j_5f_haa"},
#     "mgp8_pp_vh012j_5f":{'chunks':500, 'output':"FCChh_EvtGen_mgp8_pp_vh012j_5f"},
#     "mgp8_pp_jjaa_5f":{'chunks':500, 'output':"FCChh_EvtGen_mgp8_pp_jjaa_5f"},
#     "mgp8_pp_tt012j_5f": {'chunks':500, 'output':"FCChh_EvtGen_mgp8_pp_tt012j_5f"}

    #}

#for local testing:
#processList= {
#     "pwp8_pp_hh_lambda100_5f_hhbbaa":{'output':"FCChh_EvtGen_pwp8_pp_hh_lambda100_5f_hhbbaa"}, #put the name of your input file here (without .root), the output file will have the same name
     #"pwp8_pp_hh_lambda240_5f_hhbbaa":{'output':"FCChh_EvtGen_pwp8_pp_hh_lambda240_5f_hhbbaa"},   
     #"pwp8_pp_hh_lambda300_5f_hhbbaa":{'output':"FCChh_EvtGen_pwp8_pp_hh_lambda300_5f_hhbbaa"},
     #"pwp8_pp_hh_lambda000_5f_hhbbaa":{'output':"FCChh_EvtGen_pwp8_pp_hh_lambda000_5f_hhbbaa"}, 
     #"mgp8_pp_h012j_5f":{'output':"FCChh_EvtGen_mgp8_pp_h012j_5f"},
     #"mgp8_pp_vbf_h01j_5f":{'output':"FCChh_EvtGen_mgp8_pp_vbf_h01j_5f"},
     #"mgp8_pp_tth01j_5f":{'output':"FCChh_EvtGen_mgp8_pp_tth01j_5f"},
     #"mgp8_pp_vh012j_5f":{'output':"FCChh_EvtGen_mgp8_pp_vh012j_5f"},
     #"mgp8_pp_jjaa_5f":{'output':"FCChh_EvtGen_mgp8_pp_jjaa_5f"},
     #"mgp8_pp_tt012j_5f": {'output':"FCChh_EvtGen_mgp8_pp_tt012j_5f"}
     
#}

#Mandatory: input directory when not running over centrally produced edm4hep events. 
inputDir    = "/eos/experiment/fcc/hh/generation/DelphesEvents/fcc_v05_scenarioI/" #your directory with the input file

#Optional: output directory, default is local dir
outputDir   =  "/eos/user/p/pmastrap/FCCFW/Analysis/FCCAnalyses/run/Delphescard_validation/FCCAnalysis_ntuples_forAnalysis_Mbtag/"

#Optional: ncpus, default is 4
nCPUS       = 8

#Optional running on HTCondor, default is False
runBatch    = True
#runBatch    = True
#Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis():

    #__________________________________________________________
    #Mandatory: analysers funtion to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df, out_name):
        import ROOT

        df2 = (df
              .Define("weight",  "EventHeader.weight")
              ########################################### JETS ########################################### 
             
              # jets after overlap removal is performed between jets and isolated electrons, muons and photons
              
              #selected jets above a pT threshold of 30 GeV, eta < 4, tight ID 
              .Define("selpt_jets", "FCCAnalyses::ReconstructedParticle::sel_pt(30.)(Jet)")
              .Define("sel_jets_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_jets)")
              .Define("sel_jets", "AnalysisFCChh::SortParticleCollection(sel_jets_unsort)") 
              .Define("njets",  "FCCAnalyses::ReconstructedParticle::get_n(sel_jets)")
              .Define("j1_e",  "FCCAnalyses::ReconstructedParticle::get_e(sel_jets)[0]")
              .Define("j1_pt",  "FCCAnalyses::ReconstructedParticle::get_pt(sel_jets)[0]")
              .Define("j1_eta",  "FCCAnalyses::ReconstructedParticle::get_eta(sel_jets)[0]")
              .Define("j1_phi",  "FCCAnalyses::ReconstructedParticle::get_phi(sel_jets)[0]")
              
              .Define("j2_e",  "FCCAnalyses::ReconstructedParticle::get_e(sel_jets)[1]")
              .Define("j2_pt",  "FCCAnalyses::ReconstructedParticle::get_pt(sel_jets)[1]")
              .Define("j2_eta",  "FCCAnalyses::ReconstructedParticle::get_eta(sel_jets)[1]")
              .Define("j2_phi",  "FCCAnalyses::ReconstructedParticle::get_phi(sel_jets)[1]")

              #b-tagged jets:
              #.Alias("Jet3","Jet#3.index") 
              .Alias("Jet3","_Jet_particleIDs.index")
              #LOOSE WP : bit 1 = medium WP, bit 2 = tight WP
              #b tagged jets
              .Define("bjets", "AnalysisFCChh::get_tagged_jets(Jet, Jet3, ParticleIDs, _ParticleIDs_parameters, 1)")
              #.Define("bjets", "AnalysisFCChh::get_tagged_jets(Jet, Jet3, ParticleIDs, ParticleIDs_0, 0)") #bit 0 = loose WP, see: https://github.com/delphes/delphes/blob/master/cards/FCC/scenarios/FCChh_I.tcl
              .Define("selpt_bjets", "FCCAnalyses::ReconstructedParticle::sel_pt(30.)(bjets)")
              .Define("sel_bjets_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_bjets)")
              .Define("sel_bjets", "AnalysisFCChh::SortParticleCollection(sel_bjets_unsort)")
              .Define("nbjets", "FCCAnalyses::ReconstructedParticle::get_n(sel_bjets)")
              .Define("b1_e",  "FCCAnalyses::ReconstructedParticle::get_e(sel_bjets)[0]")
              .Define("b1_pt",  "FCCAnalyses::ReconstructedParticle::get_pt(sel_bjets)[0]")
              .Define("b1_eta",  "FCCAnalyses::ReconstructedParticle::get_eta(sel_bjets)[0]")
              .Define("b1_phi",  "FCCAnalyses::ReconstructedParticle::get_phi(sel_bjets)[0]")
              .Define("b2_e",  "FCCAnalyses::ReconstructedParticle::get_e(sel_bjets)[1]")
              .Define("b2_pt",  "FCCAnalyses::ReconstructedParticle::get_pt(sel_bjets)[1]")
              .Define("b2_eta",  "FCCAnalyses::ReconstructedParticle::get_eta(sel_bjets)[1]")
              .Define("b2_phi",  "FCCAnalyses::ReconstructedParticle::get_phi(sel_bjets)[1]")
             
              ########################################### ELECTRONS ########################################### 

              #all isolated 
              #.Alias("Electron0", "Electron#0.index")
              .Alias("Electron0", "Electron_objIdx.index")
              .Define("ele",  "FCCAnalyses::ReconstructedParticle::get(Electron0, ReconstructedParticles)")
              .Define("selpt_ele", "FCCAnalyses::ReconstructedParticle::sel_pt(10.)(ele)")
              .Define("sel_ele_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_ele)")
              .Define("sel_ele", "AnalysisFCChh::SortParticleCollection(sel_ele_unsort)")
              .Define("nele",  "FCCAnalyses::ReconstructedParticle::get_n(sel_ele)")
              .Define("e1_e",  "FCCAnalyses::ReconstructedParticle::get_e(sel_ele)[0]")
              .Define("e1_pt",  "FCCAnalyses::ReconstructedParticle::get_pt(sel_ele)[0]")
              .Define("e1_eta",  "FCCAnalyses::ReconstructedParticle::get_eta(sel_ele)[0]")
              .Define("e1_phi",  "FCCAnalyses::ReconstructedParticle::get_phi(sel_ele)[0]")
              .Define("e2_e",  "FCCAnalyses::ReconstructedParticle::get_e(sel_ele)[1]")
              .Define("e2_pt",  "FCCAnalyses::ReconstructedParticle::get_pt(sel_ele)[1]")
              .Define("e2_eta",  "FCCAnalyses::ReconstructedParticle::get_eta(sel_ele)[1]")
              .Define("e2_phi",  "FCCAnalyses::ReconstructedParticle::get_phi(sel_ele)[1]")
             
              ########################################### MUONS ########################################### 
          
              # all isolated
              #.Alias("Muon0", "Muon#0.index")
              .Alias("Muon0", "Muon_objIdx.index")
              .Define("mu",  "FCCAnalyses::ReconstructedParticle::get(Muon0, ReconstructedParticles)")
              .Define("selpt_mu", "FCCAnalyses::ReconstructedParticle::sel_pt(10.)(mu)")
              .Define("sel_mu_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_mu)")
              .Define("sel_mu", "AnalysisFCChh::SortParticleCollection(sel_mu_unsort)") 
              .Define("nmu",  "FCCAnalyses::ReconstructedParticle::get_n(sel_mu)")
              .Define("m1_e",  "FCCAnalyses::ReconstructedParticle::get_e(sel_mu)[0]")
              .Define("m1_pt",  "FCCAnalyses::ReconstructedParticle::get_pt(sel_mu)[0]")
              .Define("m1_eta",  "FCCAnalyses::ReconstructedParticle::get_eta(sel_mu)[0]")
              .Define("m1_phi",  "FCCAnalyses::ReconstructedParticle::get_phi(sel_mu)[0]")
              .Define("m2_e",  "FCCAnalyses::ReconstructedParticle::get_e(sel_mu)[1]")
              .Define("m2_pt",  "FCCAnalyses::ReconstructedParticle::get_pt(sel_mu)[1]")
              .Define("m2_eta",  "FCCAnalyses::ReconstructedParticle::get_eta(sel_mu)[1]")
              .Define("m2_phi",  "FCCAnalyses::ReconstructedParticle::get_phi(sel_mu)[1]")

             
              ########################################### PHOTONS ########################################### 
              #all, after isolation

              #.Alias("Photon0", "Photon#0.index") 
              .Alias("Photon0", "Photon_objIdx.index")
              .Define("gamma",  "FCCAnalyses::ReconstructedParticle::get(Photon0, ReconstructedParticles)")
              .Define("selpt_gamma", "FCCAnalyses::ReconstructedParticle::sel_pt(30.)(gamma)")
              .Define("sel_gamma_unsort", "FCCAnalyses::ReconstructedParticle::sel_eta(4)(selpt_gamma)")
              .Define("sel_gamma", "AnalysisFCChh::SortParticleCollection(sel_gamma_unsort)")
 
              .Define("ngamma",  "FCCAnalyses::ReconstructedParticle::get_n(sel_gamma)") 
              .Define("g1_e",  "FCCAnalyses::ReconstructedParticle::get_e(sel_gamma)[0]")
              .Define("g1_pt",  "FCCAnalyses::ReconstructedParticle::get_pt(sel_gamma)[0]")
              .Define("g1_eta",  "FCCAnalyses::ReconstructedParticle::get_eta(sel_gamma)[0]")
              .Define("g1_phi",  "FCCAnalyses::ReconstructedParticle::get_phi(sel_gamma)[0]")
              .Define("g2_e",  "FCCAnalyses::ReconstructedParticle::get_e(sel_gamma)[1]")
              .Define("g2_pt",  "FCCAnalyses::ReconstructedParticle::get_pt(sel_gamma)[1]")
              .Define("g2_eta",  "FCCAnalyses::ReconstructedParticle::get_eta(sel_gamma)[1]")
              .Define("g2_phi",  "FCCAnalyses::ReconstructedParticle::get_phi(sel_gamma)[1]")

              ########################################### EVENT WIDE KINEMATIC VARIABLES########################################### 

              #H(bb) system - using the loose WP b-jets -> if the events has < 2 bjets these variables do not get filled!
              .Define("bb_pairs_unmerged", "AnalysisFCChh::getPairs(sel_bjets)") #currently gets only leading pT pair, as a RecoParticlePair
              #then merge the bb pair into one object and get its kinematic properties
              .Define("bb_pairs", "AnalysisFCChh::merge_pairs(bb_pairs_unmerged)") #merge into one object to access inv masses etc
              .Define("m_bb", "FCCAnalyses::ReconstructedParticle::get_mass(bb_pairs)")
 
              
              #H(yy) if it exists, if there are no 2 selected photons, doesnt get filled 
              .Define("yy_pairs_unmerged", "AnalysisFCChh::getPairs(sel_gamma)")
              .Define("yy_pairs", "AnalysisFCChh::merge_pairs(yy_pairs_unmerged)")
              .Define("m_yy", "FCCAnalyses::ReconstructedParticle::get_mass(yy_pairs)")

              # Filter at least one candidate
              .Filter("sel_bjets.size()>1")
              .Filter("sel_gamma.size()>1") 
              .Filter("m_bb[0] < 200.") 
              .Filter("m_bb[0] > 80.") 
              .Filter("m_yy[0] < 180.") 
              .Filter("m_yy[0] > 100.")            
        ) 
        return df2

    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list.

    #REMEMBER TO ADD ALL THE OUTPUT BRANCHES TO THIS LIST 

    def output(out_name):
        branchList = [
                      "weight",
                      # Jets:
                      "njets", "j1_e", "j1_pt", "j1_eta", "j1_phi",
                      "j2_e", "j2_pt", "j2_eta", "j2_phi",
                      # B-jets:
                      "nbjets", "b1_e", "b1_pt", "b1_eta","b1_phi",
                      "b2_e", "b2_pt", "b2_eta","b2_phi",
                      # Electrons:
                      "nele", "e1_e", "e1_pt", "e1_eta", "e1_phi",
                      "e2_e", "e2_pt", "e2_eta", "e2_phi",
                      # Muons:
                      "nmu", "m1_e", "m1_pt", "m1_eta", "m1_phi",
                      "m2_e", "m2_pt", "m2_eta", "m2_phi",             
                      # Photons:
                      "ngamma", "g1_e", "g1_pt", "g1_eta", "g1_phi",
                      "g2_e", "g2_pt", "g2_eta", "g2_phi",
                      # Hbb decay:
                      "m_bb", 
                      #Hyy decay:
                      "m_yy"            
        ]
        
        return branchList


# local test: fccanalysis run analysis_noiso.py --nevents 100 - also switch runBatch to False

