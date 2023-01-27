#check efficiencies and resolutions in bbyy events with new delphes card

from collections import namedtuple
import ROOT
import argparse
import os 
import matplotlib.pyplot as plt
from array import array

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)

# Helper to compute myyy
ROOT.gInterpreter.Declare("""
float ComputeInvariantMass(const ROOT::RVecF & pt, const ROOT::RVecF & eta, const ROOT::RVecF & phi, const ROOT::RVecF & e)
{
    ROOT::Math::PtEtaPhiEVector p1(pt[0], eta[0], phi[0], e[0]);
    ROOT::Math::PtEtaPhiEVector p2(pt[1], eta[1], phi[1], e[1]);
    return (p1 + p2).M();
}
""")


def get_rdf(input_filepath):


	rdf = ROOT.RDataFrame("events", input_filepath)

	if not rdf:
		print("Empty file for:", input_filepath, " Exiting.")
		return

	return rdf


def check_myy_gen(input_filepath, out_dir_base):
	
	if not os.path.exists(out_dir_base):
		os.mkdir(out_dir_base)

	rdf = get_rdf(input_filepath)
	rdf_true_yy = rdf.Filter("n_truth_ys_from_higgs == 2")

	rdf_true_yy = rdf_true_yy.Define("myy_gen", "ComputeInvariantMass(pT_truth_ys_from_higgs, eta_truth_ys_from_higgs, phi_truth_ys_from_higgs, E_truth_ys_from_higgs)")

	myy_hist = rdf_true_yy.Histo1D("myy_gen")

	canvas = ROOT.TCanvas("canvas", "canvas", 800, 800) 
	canvas.cd()
	myy_hist.Draw("HIST SAME")
	canvas.SaveAs("m_yy_gen_hist.png")



if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Plot distributions for validation of new signal files")
	parser.add_argument('--input', '-i', metavar="INPUTFILE", dest="inPath", required=True, help="Path to the input directory")
	parser.add_argument('--outdir', '-o', metavar="OUTPUTDIR", dest="outDir", required=True, help="Output directory.")
	args = parser.parse_args()

	check_myy_gen(args.inPath, args.outDir)


# python bbyy_eff_res_check.py -i /eos/user/b/bistapf/FCChh_EvtGen/FCCAnalysis_ntuples_noIso/pwp8_pp_hh_lambda100_5f_hhbbaa/chunk0.root -o ./bbyy_checks/
# python bbyy_eff_res_check.py -i /eos/user/b/bistapf/FCChh_EvtGen/FCCAnalysis_ntuples_noIso/FCChh_EvtGen_pwp8_pp_hh_lambda100_5f_hhbbaa.root -o ./bbyy_checks/