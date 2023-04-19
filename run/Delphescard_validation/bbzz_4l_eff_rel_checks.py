#check efficiencies and resolutions in bbZZ(4l) events with new delphes card

from collections import namedtuple
import ROOT
import argparse
import os 
import matplotlib.pyplot as plt
from array import array
import helpers 
import resolutionPlotter

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)

# Helper to compute m4l
ROOT.gInterpreter.Declare("""
float ComputeInvariantMass(const ROOT::RVecF & pt, const ROOT::RVecF & eta, const ROOT::RVecF & phi, const ROOT::RVecF & e)
{
    ROOT::Math::PtEtaPhiEVector p1(pt[0], eta[0], phi[0], e[0]);
    ROOT::Math::PtEtaPhiEVector p2(pt[1], eta[1], phi[1], e[1]);
    ROOT::Math::PtEtaPhiEVector p3(pt[2], eta[2], phi[2], e[2]);
    ROOT::Math::PtEtaPhiEVector p4(pt[3], eta[3], phi[3], e[3]);
    return (p1 + p2 + p3 + p4).M();
}
""")

#to check on truth level the m4l as validation of the bbZZ(4l) production
def validate_file(input_filepath, out_dir_base):
	
	if not os.path.exists(out_dir_base):
		os.mkdir(out_dir_base)

	rdf = helpers.get_rdf(input_filepath)
	n_evts_total = rdf.Count().GetValue()
	rdf_true_4l = rdf.Filter("n_truth_leps_from_HZZ == 4")
	n_evts_true_4l = rdf_true_4l.Count().GetValue()

	print("{} total events, and {} events with true HZZ(4l) found = {} %".format(n_evts_total, n_evts_true_4l, n_evts_true_4l/n_evts_total*100))

	#check flavours:
	nevts_true_4e = rdf_true_4l.Filter("abs(pdgID_truth_leps_from_HZZ[0]) == 11 && abs(pdgID_truth_leps_from_HZZ[1]) == 11 && abs(pdgID_truth_leps_from_HZZ[2]) == 11 && abs(pdgID_truth_leps_from_HZZ[3]) == 11 ").Count().GetValue()
	nevts_true_4m = rdf_true_4l.Filter("abs(pdgID_truth_leps_from_HZZ[0]) == 13 && abs(pdgID_truth_leps_from_HZZ[1]) == 13 && abs(pdgID_truth_leps_from_HZZ[2]) == 13 && abs(pdgID_truth_leps_from_HZZ[3]) == 13 ").Count().GetValue()
	print(nevts_true_4e, nevts_true_4m)


	rdf_true_4l = rdf_true_4l.Define("m4l_gen", "ComputeInvariantMass(pT_truth_leps_from_HZZ, eta_truth_leps_from_HZZ, phi_truth_leps_from_HZZ, E_truth_leps_from_HZZ)")

	m4l_hist = rdf_true_4l.Histo1D("m4l_gen")

	canvas = ROOT.TCanvas("canvas", "canvas", 800, 800) 
	canvas.cd()
	m4l_hist.Draw("HIST SAME")
	canvas.SaveAs(out_dir_base+"/m_4l_gen_hist.png")
   

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Plot distributions for validation of new signal files")
	parser.add_argument('--input', '-i', metavar="INPUTFILE", dest="inPath", required=True, help="Path to the input directory")
	parser.add_argument('--outdir', '-o', metavar="OUTPUTDIR", dest="outDir", required=True, help="Output directory.")
	parser.add_argument('--lep', '-l', metavar="lepton", dest="lep", required=True, help="electron or muon")
	parser.add_argument('--op', '-op', metavar="task you want to do", dest="op", required=True, help="task you want to do")
	args = parser.parse_args()

	#test the class method:
	res_plotter = resolutionPlotter.ResolutionPlotter(args.inPath, args.outDir, args.lep)
	res_plotter.filter_input_rdf("n_truth_leps_from_HZZ == 4 && n_truthmatched_leps_from_HZZ_noiso == 4") #use only a subset of events

	#pick the lepton flavour
	if args.lep == "electron" or args.lep == "Electron":
		flavour_filter = "abs(pdgID_truth_leps_from_HZZ[0]) == 11 && abs(pdgID_truth_leps_from_HZZ[1]) == 11 && abs(pdgID_truth_leps_from_HZZ[2]) == 11 && abs(pdgID_truth_leps_from_HZZ[3]) == 11 "
	elif args.lep == "muon"  or args.lep == "Muon":
		flavour_filter = "abs(pdgID_truth_leps_from_HZZ[0]) == 13 && abs(pdgID_truth_leps_from_HZZ[1]) == 13 && abs(pdgID_truth_leps_from_HZZ[2]) == 13 && abs(pdgID_truth_leps_from_HZZ[3]) == 13 "
	else:
		raiseException("Lepton flavour not recognized. Should be electron or muon, not", args.lep)
	
	res_plotter.filter_input_rdf(flavour_filter) #use only a subset of events

	#Energy resolutions vs E in bins of eta:
	if args.op == "resolution_dE_vs_E":
		print("Plotting relative energy resolution vs E in bins of eta.")
		res_plotter.set_binning("eta_truth_leps_from_HZZ", [0., 2.5, 4., 6], "|#eta_{truth}|", "E_truth_leps_from_HZZ", [0., 50., 100., 200.], "E_{truth} in GeV")
		res_plotter.set_use_abs_eta(True)
		res_plotter.plot_resolution_histograms("E_res_eta_bins_vs_E", "E_truthmatched_leps_from_HZZ_noiso", "E_truth_leps_from_HZZ", "#sigmaE/E",  4)
	elif args.op == "resolution_dE_vs_eta":
		print("Plotting relative energy resolution vs eta in bins of E")
		res_plotter.set_binning("E_truth_leps_from_HZZ", [0., 50., 100., 200.], "E_{truth} in GeV", "eta_truth_leps_from_HZZ", [-6., -4., -2.5, -2.0, -1.5, -1.0, -0.5, 0., 0.5, 1.0, 1.5, 2.0, 2.5, 4., 6], "#eta_{truth}")
		res_plotter.set_use_abs_eta(False)
		res_plotter.plot_resolution_histograms("E_res_E_bins_vs_eta", "E_truthmatched_leps_from_HZZ_noiso", "E_truth_leps_from_HZZ", "#sigmaE/E",  4)
	elif args.op == "resolution_dP_vs_pT":
		print("Plotting relative momentum resolution vs pT in bins of eta")
		res_plotter.set_binning("eta_truth_leps_from_HZZ", [0., 2.5, 4., 6], "|#eta_{truth}|", "pT_truth_leps_from_HZZ", [0., 50., 100., 200.], "pT_{truth} in GeV")
		res_plotter.set_use_abs_eta(True)
		res_plotter.plot_resolution_histograms("P_res_eta_bins_vs_pT", "P_truthmatched_leps_from_HZZ_noiso", "P_truth_leps_from_HZZ", "#sigmaP/P",  4)
	elif args.op == "resolution_dP_vs_eta":
		print("Plotting relative momentum resolution vs eta in bins of pT")
		res_plotter.set_binning("pT_truth_leps_from_HZZ", [0., 50., 100., 200.], "pT_{truth} in GeV", "eta_truth_leps_from_HZZ", [-6., -4., -2.5, -2.0, -1.5, -1.0, -0.5, 0., 0.5, 1.0, 1.5, 2.0, 2.5, 4., 6], "#eta_{truth}")
		res_plotter.set_use_abs_eta(False)
		res_plotter.plot_resolution_histograms("P_res_pT_bins_vs_eta", "P_truthmatched_leps_from_HZZ_noiso", "P_truth_leps_from_HZZ", "#sigmaP/P",  4)


	# validate_file(args.inPath, args.outDir)

# checking tester file:
# python bbzz_4l_eff_rel_checks.py -i /eos/user/b/bistapf/FCChh_EvtGen/FCCAnalysis_ntuples_noIso/FCChh_EvtGen_pwp8_pp_hh_5f_hhbbZZ_4l_e_mu_excl.root -o ./bbzz_4l_checks/
# bbzz_4l_eff_rel_checks.py -i /eos/user/b/bistapf/FCChh_EvtGen/FCCAnalysis_ntuples_noIso/pwp8_pp_hh_lambda100_5f_hhbbzz_4l/ -o ./bbzz_4l_checks/ -l electron -op resolution_dE_vs_eta
# python bbzz_4l_eff_rel_checks.py -i /eos/user/b/bistapf/FCChh_EvtGen/FCCAnalysis_ntuples_noIso/pwp8_pp_hh_lambda100_5f_hhbbzz_4l/ -o ./bbzz_4l_checks/ -l electron -op resolution_dP_vs_pT
# python bbzz_4l_eff_rel_checks.py -i /eos/user/b/bistapf/FCChh_EvtGen/FCCAnalysis_ntuples_noIso/pwp8_pp_hh_lambda100_5f_hhbbzz_4l/ -o ./bbzz_4l_checks/ -l electron -op resolution_dP_vs_eta

