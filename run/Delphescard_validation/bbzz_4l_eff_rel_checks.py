#check efficiencies and resolutions in bbZZ(4l) events with new delphes card

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
	args = parser.parse_args()

	validate_file(args.inPath, args.outDir)

# checking tester file:
# python bbzz_4l_eff_rel_checks.py -i /eos/user/b/bistapf/FCChh_EvtGen/FCCAnalysis_ntuples_noIso/FCChh_EvtGen_pwp8_pp_hh_5f_hhbbZZ_4l_e_mu_excl.root -o ./bbzz_4l_checks/
