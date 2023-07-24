import ROOT
import os
from collections import namedtuple
from plot_helpers import plot_hist_compare, plot_weight_compare

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)


if __name__ == "__main__":
	old_card_file = "/eos/user/b/bistapf/FCCAnalysesFiles/HH_bb2lMET_analysis/preSel_SFOS_fullStat/bbWW_SF_analysis/pwp8_pp_hh_lambda100_5f_hhbbww_sel2_bJets.root"
	# rdf_old = ROOT.RDataFrame("events", old_card_file)

	out_dir = "./bbWW_SFOS_plots/"

	new_card_file = "/eos/user/b/bistapf/FCChh_EvtGen/bb2lMET_ntuples/SFOS/noZ/pwp8_pp_hh_lambda100_5f_hhbbww_sel2_bJets_medium.root"
	ttbar_file = "/eos/user/b/bistapf/FCChh_EvtGen/bb2lMET_ntuples/SFOS/noZ/mgp8_pp_tt012j_5f_sel2_bJets_medium.root"

	#processes or different files to compare
	ProcessSpecs = namedtuple('ProcessSpecs', ['name', 'label', 'filepath', 'colour'])
	file_comparison ={
		"bbWW_old":ProcessSpecs(name="bbWW_old", label="Old card", filepath=old_card_file, colour=36 ),
		"bbWW_new":ProcessSpecs(name="bbWW_new", label="New card", filepath=new_card_file, colour=46 ),
		"ttbar_new":ProcessSpecs(name="ttbar_new", label="New card", filepath=ttbar_file, colour=46 ),
	}

	NormInfo = namedtuple('NormInfo', ['name','lumi', 'xsection', 'kfactor'])

	#units are fb
	# procDictAdd={"pwp8_pp_hh_lambda100_5f_hhbbww": {"numberOfEvents": 50000, "sumOfWeights": 50000.0, "crossSection": 0.28332, "kfactor": 1.08, "matchingEfficiency": 1.0}}
	norm_bbWW = NormInfo(name="Normalization for the FCC-hh bbWW(incl.) sample", lumi=30e+06, xsection=0.28332, kfactor=1.08)
	norm_ttbar = NormInfo(name="Normalization for the FCC-hh ttbar sample", lumi=30e+06, xsection=43110., kfactor=1.74)

	#use a custom namedntuple to transfer the plotting info
	PlotSpecs = namedtuple('PlotSpecs', ['name', 'xmin', 'xmax', 'label', 'nbins'])

	sel_vars_hists = {
		"m_bb_zoom":PlotSpecs(name="m_bb", xmin=20., xmax=200., label="m_{bb} [GeV]", nbins=30),
		"m_ll":PlotSpecs(name="m_ll", xmin=0., xmax=200., label="m_{ll} [GeV]", nbins=35),
		"dR_bb":PlotSpecs(name="dR_bb", xmin=0.0, xmax=5.5, label="#Delta R_{bb}", nbins=25),
		"dR_ll":PlotSpecs(name="dR_ll", xmin=0.0, xmax=5.5, label="#Delta R_{ll}", nbins=25),
		"dPhi_ll_MET":PlotSpecs(name="dPhi_ll_MET", xmin=-3.5, xmax=3.5, label="#Delta#phi_{ll, E_{T}^{miss} }", nbins=35),
		"HT2_ratio":PlotSpecs(name="HT2_ratio", xmin=0., xmax=1.2, label="H_{T}^{2} ratio  ", nbins=40),
		"mlb_reco":PlotSpecs(name="mlb_reco", xmin=0., xmax=1000., label="m_{lb}^{reco} [GeV]", nbins=50),
		"mlb_reco_zoom":PlotSpecs(name="mlb_reco", xmin=30., xmax=510., label="m_{lb}^{reco} [GeV]", nbins=12),
		"mT2_HH_selBinning":PlotSpecs(name="mT2_HH", xmin=75., xmax=400., label="m_{T2}(bb2l+MET) [GeV]", nbins=[ 75., 90., 105., 120., 135., 150., 200. ]),
	}

	# out_dir_compare = "./Comparison_Plots/"
	# out_dir_weights = "./plots_weights_compare_bbWW_SFOS"
	out_dir_weights = "./plots_weights_compare_ttbar_SFOS"
	for hist_name, hist in sel_vars_hists.items():
		# compare distirbutions in new card with and without event weights
		# plot_weight_compare(hist_name, hist, file_comparison["bbWW_new"], out_dir_weights, norm_info=norm_bbWW, yaxis_label="Events", 
		# 				do_ratio=True, file_format="png", do_logy=False, tree_name="events", weight_name="weight")

		plot_weight_compare(hist_name, hist, file_comparison["ttbar_new"], out_dir_weights, norm_info=norm_ttbar, yaxis_label="Events", 
						do_ratio=True, file_format="png", do_logy=False, tree_name="events", weight_name="weight")


		#first compare normalized to unit area, between the files
		# plot_hist_compare(hist_name, hist, file_comparison["bbWW_new"], file_comparison["bbWW_old"], out_dir, norm_info="", yaxis_label="Fraction of events", 
		# 				  do_ratio=True, file_format="png", do_logy=False, tree_name="events", weight_name="", do_norm_unit=True )
		# plot_hist_compare(hist_name, hist, file_comparison["bbWW_new"], file_comparison["bbWW_old"], out_dir, norm_info="", yaxis_label="Fraction of events", 
		# 				  do_ratio=True, file_format="png", do_logy=True, tree_name="events", weight_name="", do_norm_unit=True )

	exit()


	