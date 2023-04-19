#plotting the isolation variable

from collections import namedtuple
import ROOT
import argparse
import os 
import matplotlib.pyplot as plt
from array import array
import helpers

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)

def plot_isoVar_delphes(input_path, out_dir, isoVarName, xmin=None, xmax=None, n_bins=None, do_logy=False):

	plot_name = isoVarName

	rdf = helpers.get_rdf(input_path)
	# print(rdf.Count().GetValue())

	#filter to actually have the truth->reco matched lepton if asking for that one
	if "truthmatched" in isoVarName:
		rdf = rdf.Filter("n_truth_leps_from_HWW == 1")
		rdf = rdf.Filter("n_truthmatched_leps_from_HWW_noiso == 1")
		plot_name+="_filtered_1l_evts"

	if n_bins:
		model = ROOT.RDF.TH1DModel("isoVar_hist", "isoVar_hist", n_bins, xmin, xmax)
		isoVar_hist = rdf.Histo1D(model, isoVarName).GetValue()  
		plot_name+="_range_{}_{}_nbins_{}".format(xmin, xmax, n_bins)

	else:
		isoVar_hist = rdf.Histo1D(isoVarName).GetValue()   

	# if xmax:
	# 	isoVar_hist.SetAxisRange(xmin, xmax)
	# 	plot_name+="_range_{}_{}".format(xmin, xmax)
		
	helpers.plot_single_hist(isoVar_hist, plot_name, out_dir, "Isolation Variable", "Events", do_gauss_fit=False, colour_code=38, file_format="png", do_logy=do_logy)

#difference between original and recalculated isoVar
def plot_isoVar_compare(input_path, out_dir, isoVarName):

	plot_name = "diff_orig_recalc_{}".format(isoVarName)
	recalc_isovar_name = "recalc_{}".format(isoVarName)
	diff_to_plot = "{} - {}".format(isoVarName, recalc_isovar_name)

	rdf = helpers.get_rdf(input_path)
	rdf = rdf.Define("isoVar_diff", diff_to_plot)

	isoVar_diff_hist = rdf.Histo1D("isoVar_diff").GetValue()   
		
	helpers.plot_single_hist(isoVar_diff_hist, plot_name, out_dir, "Delphes isoVar - recalculated isoVar", "Events", do_gauss_fit=False, colour_code=38, file_format="png", do_logy=False)

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Plot distributions for validation of new signal files")
	parser.add_argument('--input', '-i', metavar="INPUTFILE", dest="inPath", required=True, help="Path to the input directory")
	parser.add_argument('--outdir', '-o', metavar="OUTPUTDIR", dest="outDir", required=True, help="Output directory.")
	parser.add_argument('--isoVarName', '-n', metavar="ISOVARNAME", dest="isoVarName", required=True, help="Name of the isolation variable to plot.")

	args = parser.parse_args()

	#check the difference
	plot_isoVar_compare(args.inPath, args.outDir, args.isoVarName)

	#plot whole range with log axis
	plot_isoVar_delphes(args.inPath, args.outDir, args.isoVarName, do_logy=True)

	#then plot smaller range without log
	xmin = 0.
	xmax = 20.
	n_bins = 200
	plot_isoVar_delphes(args.inPath, args.outDir, args.isoVarName, xmin, xmax, n_bins)

	#and also only below 1
	xmin = 0.
	xmax = 1.
	n_bins = 50
	plot_isoVar_delphes(args.inPath, args.outDir, args.isoVarName, xmin, xmax, n_bins)

	#checks on Zmumu:
	# python plot_isoVar.py -i /eos/user/b/bistapf/FCChh_EvtGen/FCCAnalysis_ntuples_noIso/testing_isoVar/FCChh_testing_isoVar_Zmumu.root -o /eos/user/b/bistapf/FCCAnalyses_Plots/DelphesCardValidation/Zmumu_iso_check/ -n isoVar_muons_noiso
	# python plot_isoVar.py -i /eos/user/b/bistapf/FCChh_EvtGen/FCCAnalysis_ntuples_noIso/testing_isoVar/FCChh_testing_isoVar_Zmumu.root -o /eos/user/b/bistapf/FCCAnalyses_Plots/DelphesCardValidation/Zmumu_iso_check/ -n isoVar_photons_noiso
	# python plot_isoVar.py -i /eos/user/b/bistapf/FCChh_EvtGen/FCCAnalysis_ntuples_noIso/testing_isoVar/FCChh_testing_isoVar_Zmumu.root -o /eos/user/b/bistapf/FCCAnalyses_Plots/DelphesCardValidation/Zmumu_iso_check/ -n isoVar_electrons_noiso

	#running on bbww signal events:
	# python plot_isoVar.py -i /eos/user/b/bistapf/FCChh_EvtGen/FCCAnalysis_ntuples_noIso/testing_isoVar/pwp8_pp_hh_lambda100_5f_hhbbww -o /eos/user/b/bistapf/FCCAnalyses_Plots/DelphesCardValidation/ -n isoVar_truthmatched_ele_from_higgs
	# python plot_isoVar.py -i /eos/user/b/bistapf/FCChh_EvtGen/FCCAnalysis_ntuples_noIso/testing_isoVar/pwp8_pp_hh_lambda100_5f_hhbbww -o /eos/user/b/bistapf/FCCAnalyses_Plots/DelphesCardValidation/ -n isoVar_truthmatched_mu_from_higgs
	# python plot_isoVar.py -i /eos/user/b/bistapf/FCChh_EvtGen/FCCAnalysis_ntuples_noIso/testing_isoVar/pwp8_pp_hh_lambda100_5f_hhbbww -o /eos/user/b/bistapf/FCCAnalyses_Plots/DelphesCardValidation/ -n isoVar_electrons_noiso
	# python plot_isoVar.py -i /eos/user/b/bistapf/FCChh_EvtGen/FCCAnalysis_ntuples_noIso/testing_isoVar/pwp8_pp_hh_lambda100_5f_hhbbww -o /eos/user/b/bistapf/FCCAnalyses_Plots/DelphesCardValidation/ -n isoVar_muons_noiso
	# python plot_isoVar.py -i /eos/user/b/bistapf/FCChh_EvtGen/FCCAnalysis_ntuples_noIso/testing_isoVar/pwp8_pp_hh_lambda100_5f_hhbbww -o /eos/user/b/bistapf/FCCAnalyses_Plots/DelphesCardValidation/ -n isoVar_photons_noiso