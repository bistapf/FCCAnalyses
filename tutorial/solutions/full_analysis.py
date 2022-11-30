processList = {
    "fastsim_tutorial_output":{}, #put the name of your input file here (without .root), the output file will have the same name
    "bkg_evts":{}, #put the name of your input file here (without .root), the output file will have the same name
}

#Mandatory: input directory when not running over centrally produced edm4hep events. 
inputDir    = "." #your directory with the input file

#Optional: output directory, default is local dir
outputDir   = "./outputs/"

#Optional: ncpus, default is 4
nCPUS       = 2

#Optional running on HTCondor, default is False
runBatch    = False

#Mandatory: RDFanalysis class where the use defines the operations on the TTree
class RDFanalysis():

    #__________________________________________________________
    #Mandatory: analysers funtion to define the analysers to process, please make sure you return the last dataframe, in this example it is df2
    def analysers(df):
        import ROOT

        df2 = (df
              ########################################### JETS ########################################### 
              #example showing how to access common kinematic variables 
              .Define("n_jets",  "FCCAnalyses::ReconstructedParticle::get_n(Jet)")
              .Define("px_jets",  "FCCAnalyses::ReconstructedParticle::get_px(Jet)")
              .Define("py_jets",  "FCCAnalyses::ReconstructedParticle::get_py(Jet)")
              .Define("pz_jets",  "FCCAnalyses::ReconstructedParticle::get_pz(Jet)")
              .Define("E_jets",  "FCCAnalyses::ReconstructedParticle::get_e(Jet)")
              .Define("pT_jets",  "FCCAnalyses::ReconstructedParticle::get_pt(Jet)")
              .Define("eta_jets",  "FCCAnalyses::ReconstructedParticle::get_eta(Jet)")

              #example how to select only objects above a certain pT
              .Define("selected_jets", "FCCAnalyses::ReconstructedParticle::sel_pt(20.)(Jet)") #in GeV
              .Define("n_jets_sel",  "FCCAnalyses::ReconstructedParticle::get_n(selected_jets)")

              #example how to access b-tagging information
              .Alias("Jet3","Jet#3.index") 
              .Define("b_tagged_jets", "AnalysisFCChh::get_tagged_jets(Jet, Jet3, ParticleIDs, ParticleIDs_0, 0)") #bit 0 = b-tagging info, see: https://github.com/delphes/delphes/blob/master/cards/FCC/FCChh.tcl#L1136
              .Define("n_b_jets", "FCCAnalyses::ReconstructedParticle::get_n(b_tagged_jets)")

              #example how to access tau-tagging information
              .Define("tau_tagged_jets", "AnalysisFCChh::get_tau_jets(Jet, Jet3, ParticleIDs, ParticleIDs_0, 0)") 
              .Define("n_tau_jets", "FCCAnalyses::ReconstructedParticle::get_n(tau_tagged_jets)")

              ########################################### ELECTRONS ########################################### 
              #example how to retrieve electrons
              .Alias("Electron0", "Electron#0.index")
              .Define("electrons",  "FCCAnalyses::ReconstructedParticle::get(Electron0, ReconstructedParticles)")
              .Define("n_electrons",  "FCCAnalyses::ReconstructedParticle::get_n(electrons)")
              .Define("pT_electrons",  "FCCAnalyses::ReconstructedParticle::get_pt(electrons)")
              .Define("eta_electrons",  "FCCAnalyses::ReconstructedParticle::get_eta(electrons)")

              ########################################### MUONS ########################################### 
              #example how to retrieve muons
              .Alias("Muon0", "Muon#0.index")
              .Define("muons",  "FCCAnalyses::ReconstructedParticle::get(Muon0, ReconstructedParticles)") 
              .Define("n_muons",  "FCCAnalyses::ReconstructedParticle::get_n(muons)")
              .Define("pT_muons",  "FCCAnalyses::ReconstructedParticle::get_pt(muons)")
              .Define("eta_muons",  "FCCAnalyses::ReconstructedParticle::get_eta(muons)")

              ########################################### PHOTONS ########################################### 
              #example how to retrieve photons
              .Alias("Photon0", "Photon#0.index") 
              .Define("photons",  "FCCAnalyses::ReconstructedParticle::get(Photon0, ReconstructedParticles)") 
              .Define("n_photons",  "FCCAnalyses::ReconstructedParticle::get_n(photons)") 
              .Define("pT_photons",  "FCCAnalyses::ReconstructedParticle::get_pt(photons)")
              .Define("eta_photons",  "FCCAnalyses::ReconstructedParticle::get_eta(photons)")

              ########################################### MET ########################################### 
              #example how to retrieve missing transverse energy
              .Define("MET", "FCCAnalyses::ReconstructedParticle::get_pt(MissingET)")

              ########################################### EVENT WIDE KINEMATIC VARIABLES########################################### 
              #example how to get the invariant mass of an object
              .Define("m_jets", "FCCAnalyses::ReconstructedParticle::get_mass(Jet)")

              #you can select the leading pT pair (or subleading) of some object with 
              .Define("bb_pairs_leading", "AnalysisFCChh::getPairs(b_tagged_jets)")
              .Define("bb_pairs_subleading", "AnalysisFCChh::getPair_sublead(b_tagged_jets)")

              #and you can merge a pair with
              .Define("bb_pairs_leading_merged", "AnalysisFCChh::merge_pairs(bb_pairs_leading)")
              #after which you can treat it like a single object 

              .Define("m_bb_leading", "FCCAnalyses::ReconstructedParticle::get_mass(bb_pairs_leading_merged)")

              #invariant di-photon mass
              .Define("yy_pairs_leading", "AnalysisFCChh::getPairs(photons)")
              .Define("yy_pairs_leading_merged", "AnalysisFCChh::merge_pairs(yy_pairs_leading)")
              .Define("m_yy", "FCCAnalyses::ReconstructedParticle::get_mass(yy_pairs_leading_merged)")

              ########################################### MC PARTICLES ########################################### 
              #example how to filter for MC particles with a certain PDG ID and status code
              .Define("MC_photons", ROOT.MCParticle.sel_pdgID(22, 0),["Particle"])
              .Define("stable_MC_photons", ROOT.MCParticle.sel_genStatus(1),["MC_photons"])


               )
        return df2

    #__________________________________________________________
    #Mandatory: output function, please make sure you return the branchlist as a python list.

    #REMEMBER TO ADD ALL THE OUTPUT BRANCHES TO THIS LIST 

    def output():
        branchList = [
            "n_jets", "px_jets", "py_jets", "pz_jets", "E_jets", "pT_jets", "eta_jets",
            "n_jets_sel", "n_b_jets", 
            "n_tau_jets",
            "n_electrons", "pT_electrons", "eta_electrons",
            "n_muons", "pT_muons", "eta_muons",
            "n_photons", "pT_photons", "eta_photons",
            "m_bb_leading", "m_yy", 
            
        ]
        return branchList




