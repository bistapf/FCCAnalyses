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

#version of this function that loops over vector of 4 leptons matched to truth, and adds the resulting resolution histograms for more statistics
#feed with rdf where 4 leptons are already required!!
#eta edges should be a tuple of minimum, maximum
def check_lep_energy_res_per_eta_bin_4l(input_rdf, eta_edges, E_edges, filebasename, out_dir_base, iso):

	model = ROOT.RDF.TH1DModel("resolution_model_hist", "resolution_model_hist", 40, -0.05, 0.05)

	#histogram vs E
	hist_binEdges = array("d", E_edges)
	hist_nBins = len(E_edges)-1
	hist_res_vs_E_all = ROOT.TH1D(filebasename, filebasename, hist_nBins, hist_binEdges)

	hist_title = "{} < |#eta| < {}".format(eta_edges[0], eta_edges[1])

	for i_E_edge in range(len(E_edges)-1):

		res_hist_bin_4l = ROOT.TH1D("res_hist_bin_4l", "res_hist_bin_4l", 40, -0.05, 0.05)

		for lepton_i in range(4):
			cut_string_eta = "abs(eta_truth_leps_from_HZZ[{}]) > {:.2f} && abs(eta_truth_leps_from_HZZ[{}]) <= {:.2f}".format(lepton_i, eta_edges[0], lepton_i, eta_edges[1])
			print(cut_string_eta) 
			rdf_bin = input_rdf.Filter(cut_string_eta)

			cutstring_bin = "E_truth_leps_from_HZZ[{}] > {:.2f} && E_truth_leps_from_HZZ[{}] <= {:.2f}".format(lepton_i, E_edges[i_E_edge], lepton_i, E_edges[i_E_edge+1])
			print(cutstring_bin)
			rdf_bin = rdf_bin.Filter(cutstring_bin)

			hist_i_name = "{}_{}".format(filebasename, lepton_i)

			lep_res_name = 'lep_resolution_{}'.format(lepton_i)

			if iso is True:
				lep_res_def_string = '(E_truthmatched_leps_from_HZZ_noiso[{}] - E_truth_leps_from_HZZ[0])/E_truth_leps_from_HZZ[{}]'.format(lepton_i, lepton_i)
			
			else:
				lep_res_def_string ='(E_truthmatched_leps_from_HZZ_noiso[{}] - E_truth_leps_from_HZZ[0])/E_truth_leps_from_HZZ[{}]'.format(lepton_i, lepton_i)

			print(lep_res_name, lep_res_def_string)
			rdf_resolution = rdf_bin.Define(lep_res_name, lep_res_def_string)

			#store a histogram of the resolution 
			tmp_hist = rdf_resolution.Histo1D(model, lep_res_name).GetValue()   
			print("#Entries in the histogram for lepton {}: {}".format(lepton_i, tmp_hist.GetEntries() ))
			res_hist_bin_4l.Add(tmp_hist)


		print("#Entries in the histogram for all 4 leptons: {}".format(res_hist_bin_4l.GetEntries() ))
		histfilename = "{}_E_{}_to_{}_4l".format(filebasename, E_edges[i_E_edge], E_edges[i_E_edge+1])  
		gaus_pars = helpers.plot_single_hist(res_hist_bin_4l, histfilename, out_dir_base, "#sigma(E)/E", do_gauss_fit=True, colour_code=38, file_format="png")
	
		if gaus_pars:
			hist_res_vs_E_all.SetBinContent(i_E_edge+1, gaus_pars[2])
			hist_res_vs_E_all.SetBinError(i_E_edge+1, gaus_pars[3])

	helpers.plot_single_hist(hist_res_vs_E_all, filebasename, out_dir_base, "E_{true} in GeV", do_gauss_fit=False, colour_code=38, file_format="png")

	return hist_res_vs_E_all   

def check_lepton_resolutions(flavour, input_filepath, out_dir_base):

	if not os.path.exists(out_dir_base):
		os.mkdir(out_dir_base)

	rdf = helpers.get_rdf(input_filepath)

	rdf_true_4l = rdf.Filter("n_truth_leps_from_HZZ == 4")

	if flavour=="electron":
		rdf_true_4e = rdf_true_4l.Filter("abs(pdgID_truth_leps_from_HZZ[0]) == 11 && abs(pdgID_truth_leps_from_HZZ[1]) == 11 && abs(pdgID_truth_leps_from_HZZ[2]) == 11 && abs(pdgID_truth_leps_from_HZZ[3]) == 11 ")
		rdf_true_4l_recomatched = rdf_true_4e.Filter("n_truthmatched_leps_from_HZZ_noiso == 4" ) #TODO: ADD ISO OPTION?

	elif flavour=="muon":
		rdf_true_4m = rdf_true_4l.Filter("abs(pdgID_truth_leps_from_HZZ[0]) == 13 && abs(pdgID_truth_leps_from_HZZ[1]) == 13 && abs(pdgID_truth_leps_from_HZZ[2]) == 13 && abs(pdgID_truth_leps_from_HZZ[3]) == 13 ")
		rdf_true_4l_recomatched = rdf_true_4m.Filter("n_truthmatched_leps_from_HZZ_noiso == 4" )

	#first check: energy resolutions vs E in bins of eta
	list_of_hists =[]
	eta_edges = [0., 2.5, 4., 6]
	E_edges = [0., 50., 100., 200.] #TODO: CHECK IF CAN BE FINER

	for i_eta_edge in range(len(eta_edges)-1):
		hist_title = "{} < |#eta| < {}".format(eta_edges[i_eta_edge], eta_edges[i_eta_edge+1])
		hist_filebase = "{}_E_resolution_eta_bin{}".format(flavour, i_eta_edge)
		eta_edges_tuple = [eta_edges[i_eta_edge], eta_edges[i_eta_edge+1]]
		hist_eta_bin = check_lep_energy_res_per_eta_bin_4l(rdf_true_4l_recomatched, eta_edges_tuple, E_edges, hist_filebase, out_dir_base, False)
		hist_eta_bin.SetTitle(hist_title)
		list_of_hists.append(hist_eta_bin)

	helpers.plot_list_of_hists(list_of_hists, "{}_E_resolution".format(flavour), out_dir_base, "E_{truth} in GeV", "{} : #sigma(E)/E".format(flavour), file_format="png")

	#second check: energy resolutions vs eta in bins of E


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Plot distributions for validation of new signal files")
	parser.add_argument('--input', '-i', metavar="INPUTFILE", dest="inPath", required=True, help="Path to the input directory")
	parser.add_argument('--outdir', '-o', metavar="OUTPUTDIR", dest="outDir", required=True, help="Output directory.")
	parser.add_argument('--lep', '-l', metavar="lepton", dest="lep", required=True, help="electron or muon")
	args = parser.parse_args()

	# check_lepton_resolutions(args.lep, args.inPath, args.outDir)

	#test the class method:
	res_plotter = resolutionPlotter.ResolutionPlotter(args.inPath, args.outDir, args.lep)
	res_plotter.filter_input_rdf("n_truth_leps_from_HZZ == 4 && n_truthmatched_leps_from_HZZ_noiso == 4") #use only a subset of events

	#pick the lepton flavour
	if args.lep == "electron" or args.lep == "Electron":
		flavour_filter = "abs(pdgID_truth_leps_from_HZZ[0]) == 11 && abs(pdgID_truth_leps_from_HZZ[1]) == 11 && abs(pdgID_truth_leps_from_HZZ[2]) == 11 && abs(pdgID_truth_leps_from_HZZ[3]) == 11 "
	elif args.lep == "muon"  or args.lep == "Muon":
		flavour_filter = "abs(pdgID_truth_leps_from_HZZ[0]) == 13 && abs(pdgID_truth_leps_from_HZZ[1]) == 13 && abs(pdgID_truth_leps_from_HZZ[2]) == 13 && abs(pdgID_truth_leps_from_HZZ[3]) == 13 "

	res_plotter.filter_input_rdf(flavour_filter) #use only a subset of events

	#start with energy resolutions vs E in bins of eta:
	res_plotter.set_binning("eta_truth_leps_from_HZZ", [0., 2.5, 4., 6], "|#eta_{truth}|", "E_truth_leps_from_HZZ", [0., 50., 100., 200.], "E_{truth} in GeV")
	res_plotter.plot_resolution_histograms("E_res_eta_bins_vs_E", "E_truthmatched_leps_from_HZZ_noiso", "E_truth_leps_from_HZZ", "#sigmaE/E",  4)

	# res_plotter.build_cutstring_bin(["eta_truth_leps_from_HZZ", "E_truth_leps_from_HZZ"], list_bin_edge_pairs, object_index)

	# validate_file(args.inPath, args.outDir)

# checking tester file:
# python bbzz_4l_eff_rel_checks.py -i /eos/user/b/bistapf/FCChh_EvtGen/FCCAnalysis_ntuples_noIso/FCChh_EvtGen_pwp8_pp_hh_5f_hhbbZZ_4l_e_mu_excl.root -o ./bbzz_4l_checks/
# python bbzz_4l_eff_rel_checks.py -i /eos/user/b/bistapf/FCChh_EvtGen/FCCAnalysis_ntuples_noIso/pwp8_pp_hh_lambda100_5f_hhbbzz_4l/ -o ./bbzz_4l_checks/ -l muon
# python bbzz_4l_eff_rel_checks.py -i /eos/user/b/bistapf/FCChh_EvtGen/FCCAnalysis_ntuples_noIso/pwp8_pp_hh_lambda100_5f_hhbbzz_4l/ -o ./bbzz_4l_checks_class/ -l muon
