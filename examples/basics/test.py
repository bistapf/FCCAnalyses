import ROOT
import os
import argparse

#setup of the libraries, following the example:
print ("Load cxx analyzers ... ",)
ROOT.gSystem.Load("libedm4hep")
ROOT.gSystem.Load("libpodio")
ROOT.gSystem.Load("libFCCAnalyses")
ROOT.gErrorIgnoreLevel = ROOT.kFatal
_edm  = ROOT.edm4hep.ReconstructedParticleData()
_pod  = ROOT.podio.ObjectID()
_fcc  = ROOT.dummyLoader

print ('edm4hep  ',_edm)
print ('podio    ',_pod)
print ('fccana   ',_fcc)

#helper functions for truth filter:

#check if particle is lepton, neutrino or Z
ROOT.gInterpreter.Declare("""
bool isLep(edm4hep::MCParticleData truth_part) {
	auto pdg_id = truth_part.PDG;
	//std::cout << "pdg id of truth part is" << pdg_id << std::endl;
    if (abs(pdg_id) == 11 || abs(pdg_id) == 13 || abs(pdg_id) == 15){
        return true;
    }
    else{
    	return false;
    }
}
""")

ROOT.gInterpreter.Declare("""
bool isNeutrino(edm4hep::MCParticleData truth_part) {
	auto pdg_id = truth_part.PDG;
	//std::cout << "pdg id of truth part is" << pdg_id << std::endl;
    if (abs(pdg_id) == 12 || abs(pdg_id) == 14 || abs(pdg_id) == 16){
        return true;
    }
    else{
    	return false;
    }
}
""")

ROOT.gInterpreter.Declare("""
bool isZ(edm4hep::MCParticleData truth_part) {
	auto pdg_id = truth_part.PDG;
	//std::cout << "pdg id of truth part is" << pdg_id << std::endl;
    if (abs(pdg_id) == 23){
        return true;
    }
    else{
    	return false;
    }
}
""")

ROOT.gInterpreter.Declare("""
bool isTau(edm4hep::MCParticleData truth_part) {
	auto pdg_id = truth_part.PDG;
	//std::cout << "pdg id of truth part is" << pdg_id << std::endl;
    if (abs(pdg_id) == 15){
        return true;
    }
    else{
    	return false;
    }
}
""")



#helper fct to check the Z decay
ROOT.gInterpreter.Declare("""
	int checkZDecay(edm4hep::MCParticleData truth_Z, ROOT::VecOps::RVec<podio::ObjectID> daughter_ids, ROOT::VecOps::RVec<edm4hep::MCParticleData> truth_particles){

		auto first_child_index = truth_Z.daughters_begin;
		auto last_child_index = truth_Z.daughters_end;

		if(last_child_index - first_child_index != 2){
			std::cout << "Error in checkZDecay! Found more or fewer than exactly 2 daughters of a Z boson - this is not expected by code. Need to implement a solution still!"<< std::endl;
			return 0;
		}

		//now get the indices in the daughters vector
		auto child_1_MC_index = daughter_ids.at(first_child_index).index;
		auto child_2_MC_index = daughter_ids.at(last_child_index-1).index;

		// std::cout << "Daughters run from: " << child_1_MC_index << " to " << child_2_MC_index << std::endl;

		//then go back to the original vector of MCParticles
		auto child_1 = truth_particles.at(child_1_MC_index);
		auto child_2 = truth_particles.at(child_2_MC_index);

		if( isLep(child_1) &&  isLep(child_2) ){
			return 1;
		}
		else if ( isNeutrino(child_1) &&  isNeutrino(child_2) ){
			return 2;
		}
		else{
			std::cout << "Found different decay of Z boson than 2 leptons (e or mu), neutrinos or taus! Please check." << std::endl;
			return 0;
		}

	}

""")

#truth filter to get llvv signal events:
ROOT.gInterpreter.Declare("""
	bool ZZllvvFilter(ROOT::VecOps::RVec<edm4hep::MCParticleData> truth_particles, ROOT::VecOps::RVec<podio::ObjectID> daughter_ids) {
	//std::cout << "Running llvv filter" << std::endl;
	std::vector<edm4hep::MCParticleData> z_list; 

	// first scan through the truth particles to find Z bosons
    for (auto & truth_part: truth_particles) {
    	if (isZ(truth_part)){
    		z_list.push_back(truth_part);
    	}
    	//Tau veto:
    	if  (isTau(truth_part)){
    		return false;
    	}
    }

    //check how many Zs are in event and build the flag:
    // std::cout << "Number of Zs" << z_list.size() << std::endl;
    if (z_list.size() == 2){
    	int z1_decay = checkZDecay(z_list.at(0), daughter_ids, truth_particles);
    	int z2_decay = checkZDecay(z_list.at(1), daughter_ids, truth_particles);

    	int zz_decay_flag = z1_decay + z2_decay;

    	//flags are Z(ll) =1 and Z(vv) =2, so flag for llvv is =3 (4l=2, 4v=4)
		if (zz_decay_flag == 3){
				return true; 
			}
			else{
				return false;
			}

    }
    else{
    	return false;
    }
}
	
	
""")


#analysis class implementing the "event loop", use for standalone running
class analysis():
	#__________________________________________________________
	def __init__(self, inputlist, outname, ncpu):
		self.outname = outname

		if ".root" not in outname:
			self.outname+=".root"

		ROOT.ROOT.EnableImplicitMT(ncpu)

		self.df = ROOT.RDataFrame("events", inputlist)

	#__________________________________________________________
	def run(self):

		#filter signal events: only want ZZllvv decays out of ZZ(leptonic) samples
		if "pwp8_pp_hh_lambda100_5f_hhbbzz_zleptonic" in self.outname :
			df_intial = (self.df
			.Define("mc_particles", "Particle")
			.Alias("mc_daughters", "Particle#1")
			.Filter("ZZllvvFilter(mc_particles, mc_daughters)")
			)
		else:
			df_intial = self.df

		print("Events in input dataframe:", self.df.Count().GetValue())
		print("Events in filtered ZZllvv dataframe:", df_intial.Count().GetValue())

		#need to add variables here!
		df2 = (df_intial
		#old examples:
		.Define("selected_jets", "ReconstructedParticle::sel_pt(50.)(Jet)") 
		.Define("jet_pT",        "ReconstructedParticle::get_pt(Jet)")
		.Define("seljet_pT",     "ReconstructedParticle::get_pt(selected_jets)")
		#new variables for the analysis of bbZZ events:
		#count the leptons, with pT > 20 GeV:
		# .Define("selected_electrons", "ReconstructedParticle::sel_pt(20.)(Electron)") 
		# .Define("electron_pT",        "ReconstructedParticle::get_pt(Muon)")
		# .Define("N_electrons", "selected_electrons.size()") 

		#get number of b-jets
		# .Define("n_b_jets", "ReconstructedParticle::getJet_ntags(Jet)")

		#copied from FCC-ee example:
		# define an alias for electron index collection #why is this needed?
		.Alias("Electron0", "Electron#0.index")
		# define the electron collection
		.Define("electrons",  "ReconstructedParticle::get(Electron0, ReconstructedParticles)") #dont get it
		.Define("n_electrons",  "ReconstructedParticle::get_n(electrons)")
		.Define("pT_electrons",  "ReconstructedParticle::get_pt(electrons)")
		#select electrons with pT > 20 GeV
		.Define("selected_electrons", "ReconstructedParticle::sel_pt(20.)(electrons)")
		# .Define("n_electrons_sel", "getRP_n(selected_electrons)")
		.Define("n_electrons_sel", "return selected_electrons.size()") #why does this not work?
		.Define("pT_electrons_sel",  "ReconstructedParticle::get_pt(selected_electrons)")

		# define an alias for muon index collection #why is this needed?
		.Alias("Muon0", "Muon#0.index")
		# define the muon collection
		.Define("muons",  "ReconstructedParticle::get(Muon0, ReconstructedParticles)") #dont get it
		.Define("n_muons",  "ReconstructedParticle::get_n(muons)")
		.Define("pT_muons",  "ReconstructedParticle::get_pt(muons)")
		#select electrons with pT > 20 GeV
		.Define("selected_muons", "ReconstructedParticle::sel_pt(20.)(muons)")
		.Define("n_muons_sel", "ReconstructedParticle::get_n(selected_muons)")
		# .Define("n_electrons_sel", "return selected_electrons.size()") #why does this not work?
		.Define("pT_muons_sel",  "ReconstructedParticle::get_pt(selected_muons)")

		#leptons:
		.Define("n_leps",  "ReconstructedParticle::get_n(muons)+ReconstructedParticle::get_n(electrons)")
		.Define("n_leps_sel",  "ReconstructedParticle::get_n(selected_muons)+ReconstructedParticle::get_n(selected_electrons)")


		#get some truth particles: neutrinos etc?
		.Define("MC_pdg", "MCParticle::get_pdg(Particle)")

		#access met
		.Define("MET", "ReconstructedParticle::get_pt(MissingET)")

		#filter out all events with exactly 2 leptons
		# .Filter("n_leps_sel == 2")
		#calculate mll
		.Define("z_ee", "ReconstructedParticle::resonanceBuilder(91)(selected_electrons)")
		.Define("m_ee", "ReconstructedParticle::get_mass(z_ee)")
		.Define("z_mumu", "ReconstructedParticle::resonanceBuilder(91)(selected_muons)")
		.Define("m_mumu", "ReconstructedParticle::get_mass(z_mumu)")
		)

		# select branches for output file
		branchList = ROOT.vector('string')()
		for branchName in [
						"n_electrons",
						"n_electrons_sel",
						"pT_electrons",
						"pT_electrons_sel",
						"n_muons",
						"n_muons_sel",
						"pT_muons",
						"pT_muons_sel",
						"n_leps",
						"n_leps_sel",
						"MC_pdg",
						"MET",
						"m_ee",
						"m_mumu",
						]:
			branchList.push_back(branchName)
		df2.Snapshot("events", self.outname, branchList)

if __name__ == "__main__":

	# default_input_tester = "/eos/experiment/fcc/hh/generation/DelphesEvents/fcc_v04/pwp8_pp_hh_lambda100_5f_hhbbzz/events_000077595.root" #fully inclusive Z decays
	default_input_tester = "/eos/experiment/fcc/hh/generation/DelphesEvents/fcc_v04/pwp8_pp_hh_lambda100_5f_hhbbzz_zleptonic/events_000087952.root"
	default_out_dir = "./"

	#parse input arguments:
	parser = argparse.ArgumentParser(description="Stand-alone analysise code for FCC-hh events of type HH(bbZZ)")
	parser.add_argument('--input', '-i', metavar="INPUTFILE", dest="input_file", default=default_input_tester, help="Path to the input file. If not specified, runs over a default tester file.")
	parser.add_argument('--output', '-o', metavar="OUTPUTDIR", dest="out_dir", default=default_out_dir, help="Output directory. If not specified, sets to current directory.")
	args = parser.parse_args()

	#create the output dir, if it doesnt exist yet:
	if not os.path.exists(args.out_dir):
		os.mkdir(args.out_dir)

	#build the name/path of the output file:
	output_file = os.path.join(args.out_dir, args.input_file.split("/")[-2]+"_"+args.input_file.split("/")[-1])

	#now run:
	print("##### Running HH(bbZZ) analysis #####")
	print("Input file: ", args.input_file)
	print("Output file: ", output_file)

	ncpus = 4
	analysis = analysis(args.input_file, output_file, ncpus)
	analysis.run()

	#file with cross-sections from Clement: /afs/cern.ch/work/h/helsens/public/FCCDicts/FCC_procDict_fcc_v04.json

