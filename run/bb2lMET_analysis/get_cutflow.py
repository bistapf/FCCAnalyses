import ROOT
import os
from plot_helpers import get_nevts_sow, load_norm_json
from bb2lMET_cutlists import cut_list_bb2lmet_noZ


ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)


if __name__ == "__main__":


	#tester 
	new_card_file = "/eos/user/b/bistapf/FCChh_EvtGen/bb2lMET_ntuples/SFOS/noZ/mgp8_pp_tt012j_5f_sel2_bJets_medium.root"
	process = "mgp8_pp_tt012j_5f"
	# new_card_file = "/eos/user/b/bistapf/FCChh_EvtGen/bb2lMET_ntuples/SFOS/noZ/pwp8_pp_hh_lambda100_5f_hhbbww_sel2_bJets_medium.root"
	# process = "pwp8_pp_hh_lambda100_5f_hhbbww"
	nevts, sow = get_nevts_sow(new_card_file) #can read this from json!?
	tree_name = "events"

	#json file
	json_path = "/eos/experiment/fcc/hh/utils/FCCDicts/FCChh_procDict_v05_scenarioI.json"
	norm_dict = load_norm_json(json_path)
	# print(norm_dict)
	xsec_factor = norm_dict[process]["crossSection"]*norm_dict[process]["kfactor"]*norm_dict[process]["matchingEfficiency"]
	lumi = 30e+06

	print("nevts", nevts)
	print("sow", sow)
	
	rdf = ROOT.RDataFrame(tree_name, new_card_file)
	print("Cut : Unweighted : Weighted")
	for cut_name, cut_string in cut_list_bb2lmet_noZ.items():
		#appply cut
		rdf = rdf.Filter(cut_string)
		#calculate yield unweighted
		yield_unweighted = rdf.Count().GetValue()*xsec_factor*lumi/nevts
		# print("Unweighted yield:", yield_unweighted)

		#calculate yield weighted
		yield_weighted = rdf.Histo1D("m_ll", "weight").Integral()*xsec_factor*lumi/sow
		# yield_weighted = rdf.Histo1D("weight", "weight").Integral()*xsec_factor*lumi/sow
		# print("Weighted yield:", yield_weighted)

		print("{} : {:.2f} : {:.2f}".format(cut_name, yield_unweighted, yield_weighted))


