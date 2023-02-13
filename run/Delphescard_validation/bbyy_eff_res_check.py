#check efficiencies and resolutions in bbyy events with new delphes card

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

# Helper to compute myyy
ROOT.gInterpreter.Declare("""
float ComputeInvariantMass(const ROOT::RVecF & pt, const ROOT::RVecF & eta, const ROOT::RVecF & phi, const ROOT::RVecF & e)
{
    ROOT::Math::PtEtaPhiEVector p1(pt[0], eta[0], phi[0], e[0]);
    ROOT::Math::PtEtaPhiEVector p2(pt[1], eta[1], phi[1], e[1]);
    return (p1 + p2).M();
}
""")

def plot_2D(input_rdf, var1, var2, out_dir_base):

	hist_2D = input_rdf.Histo2D(ROOT.RDF.TH2DModel(var1, var2, 25, 0., 500., 40, -0.05, 0.05,), var1, var2)

	# corr_coeff = hist_2D.GetCorrelationFactor()
	# print(corr_coeff)
	#save it:
	canvas_name = var1+"_vs_"+var2
	canvas = ROOT.TCanvas(canvas_name, canvas_name, 800, 800) 
	canvas.SetLeftMargin(0.15)
	canvas.SetRightMargin(0.15)
	canvas.cd()

	# hist_2D.GetXaxis().SetTitle("p_{T}("+h_flavour+", reco.) [GeV]")
	# hist_2D.GetYaxis().SetTitle("p_{T}(h*, truth.) [GeV]")
	hist_2D.Draw("COLZ")

	canvas.SaveAs(out_dir_base+canvas_name+".png" )



def get_rdf(input_filepath):

	if input_filepath.endswith(".root"):
		rdf = ROOT.RDataFrame("events", input_filepath)
	else:
		rdf = ROOT.RDataFrame("events", input_filepath+"chunk*")

	if not rdf:
		print("Empty file for:", input_filepath, " Exiting.")
		return

	return rdf

def plot_single_hist(hist, filename, out_dir_base, xaxis_label, colour_code=38, file_format="png"):

	canvas = ROOT.TCanvas("canvas", "canvas", 800, 800) 
	canvas.cd()
	histfile_name = "{}.{}".format(filename, file_format)
	histfile_path = os.path.join(out_dir_base, histfile_name)

	#fit the histogram with a gaus:
	gauss = ROOT.TF1("gauss","gaus", -1., 1.)
	hist.Fit(gauss)
	fit_result= hist.GetFunction("gauss")

	
	hist.SetLineWidth(2)
	hist.SetLineColor(colour_code)
	hist.GetYaxis().SetTitle("Events")
	hist.GetXaxis().SetTitle(xaxis_label)

	gaus_pars = []
	if fit_result: #avoid crashes from fitting empty histograms
		fit_result.SetLineColor(ROOT.kBlack)
		fit_result.SetLineWidth(2)
		fit_result.Draw()

		#get the parameter values:
		gaus_mean = fit_result.GetParameter(1)
		gaus_mean_error = fit_result.GetParError(1)
		gaus_width = fit_result.GetParameter(2)
		gaus_width_error = fit_result.GetParError(2)
		gaus_pars = [gaus_mean, gaus_mean_error, gaus_width, gaus_width_error]

	hist.Draw("HIST SAME")

	leg = ROOT.TLegend(0.55, 0.6, 0.9, 0.9)
	leg.SetFillStyle( 0 )
	leg.SetBorderSize( 0 )
	leg.SetMargin( 0.1)
	leg.SetTextFont( 43 )
	leg.SetTextSize( 20 )
	leg.SetColumnSeparation(-0.05)
	leg.AddEntry(hist, hist.GetTitle(), "l")
	leg.Draw()

	canvas.SaveAs(histfile_path)

	return gaus_pars

def plot_list_of_hists_normalized(list_of_hists, histbasename, out_dir_base, xaxis_label, file_format="png"):
	canvas = ROOT.TCanvas("canvas", "canvas", 800, 800) 
	canvas.cd()
	histfile_name = "{}.{}".format(histbasename, file_format)
	histfile_path = os.path.join(out_dir_base, histfile_name)

	leg = ROOT.TLegend(0.55, 0.6, 0.9, 0.9)

	for i_hist, hist in enumerate(list_of_hists):
		print("Plotting hist", i_hist, "with name", hist.GetTitle() )
		hist.SetLineWidth(2)
		hist.SetLineColor(38+i_hist*4)

		hist.GetYaxis().SetTitle("Fraction of events")
		hist.GetXaxis().SetTitle(xaxis_label)
		# hist.Draw("HIST SAME")

		hist.Scale(1./hist.Integral()) #fraction of events
		hist.SetMaximum(0.3)
		hist.Draw("HIST SAME")
		# hist.DrawNormalized("HIST SAME")

		leg.AddEntry(hist, hist.GetTitle(), "l")


	canvas.RedrawAxis()

	leg.SetFillStyle( 0 )
	leg.SetBorderSize( 0 )
	leg.SetMargin( 0.1)
	leg.SetTextFont( 43 )
	leg.SetTextSize( 20 )
	leg.SetColumnSeparation(-0.05)
	leg.Draw()

	canvas.SaveAs(histfile_path)

def plot_list_of_hists(list_of_hists, histbasename, out_dir_base, xaxis_label, yaxis_label="Events", file_format="png"):
	canvas = ROOT.TCanvas("canvas", "canvas", 800, 800) 
	canvas.cd()
	canvas.SetLeftMargin(0.15)
	histfile_name = "{}.{}".format(histbasename, file_format)
	histfile_path = os.path.join(out_dir_base, histfile_name)

	leg = ROOT.TLegend(0.55, 0.6, 0.9, 0.9)

	for i_hist, hist in enumerate(list_of_hists):
		print("Plotting hist", i_hist, "with name", hist.GetTitle() )
		hist.SetLineWidth(2)
		hist.SetLineColor(38+i_hist*4)

		hist.GetYaxis().SetTitle(yaxis_label)
		hist.GetXaxis().SetTitle(xaxis_label)
		hist.Draw("HISTE SAME")
		leg.AddEntry(hist, hist.GetTitle(), "l")


	canvas.RedrawAxis()

	leg.SetFillStyle( 0 )
	leg.SetBorderSize( 0 )
	leg.SetMargin( 0.1)
	leg.SetTextFont( 43 )
	leg.SetTextSize( 20 )
	leg.SetColumnSeparation(-0.05)
	leg.Draw()

	canvas.SaveAs(histfile_path)




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

def check_photon_eff(input_filepath, out_dir_base):

	if not os.path.exists(out_dir_base):
		os.mkdir(out_dir_base)

	rdf = get_rdf(input_filepath)

	rdf_yy_truth = rdf.Filter("n_truth_ys_from_higgs == 2") #finding the H-yy decay doesnt always work, need to filter
	n_yy_truth_total = rdf_yy_truth.Count().GetValue()
	n_evts_yy_recomatched = rdf_yy_truth.Filter("n_truthmatched_ys_from_higgs_noiso == 2").Count().GetValue()
	n_evts_yy_recomatched_wIso = rdf_yy_truth.Filter("n_truthmatched_ys_from_higgs == 2").Count().GetValue()
	print("Efficiency for 2 matched photons before iso: {:.2f}%".format(n_evts_yy_recomatched/n_yy_truth_total*100.))
	print("Efficiency for 1 matched photons after iso: {:.2f}%".format(n_evts_yy_recomatched_wIso/n_evts_yy_recomatched*100.))

def check_photon_res_per_eta_bin(input_rdf, cutstring_base, E_edges, hist_name, filebasename, out_dir_base):

	model = ROOT.RDF.TH1DModel("resolution_model_hist", "resolution_model_hist", 40, -0.05, 0.05)

	#histogram vs E
	hist_binEdges = array("d", E_edges)
	hist_nBins = len(E_edges)-1
	hist_res_vs_E = ROOT.TH1D(filebasename, filebasename, hist_nBins, hist_binEdges)

	rdf_bin = input_rdf.Filter(cutstring_base)
	rdf_resolution = rdf_bin.Define('y_resolution', '(E_truthmatched_ys_from_higgs_noiso[0] - E_truth_ys_from_higgs[0])/E_truth_ys_from_higgs[0]')

	for i_E_edge in range(len(E_edges)-1):
		cutstring_bin = "E_truth_ys_from_higgs[0] > {:.2f} && E_truth_ys_from_higgs[0] <= {:.2f}".format(E_edges[i_E_edge], E_edges[i_E_edge+1])
		rdf_bin = rdf_resolution.Filter(cutstring_bin)

		#store a histogram of the resolution 
		tmp_hist = rdf_bin.Histo1D(model, 'y_resolution').GetValue()   
		histfilename = "{}_E_{}_to_{}".format(filebasename, E_edges[i_E_edge], E_edges[i_E_edge+1])
		tmp_hist.SetTitle("{}, RMS = {:.4f}".format(hist_name, tmp_hist.GetRMS()) )     
		gaus_pars = plot_single_hist(tmp_hist, histfilename, out_dir_base, "#sigma(E)/E", colour_code=38, file_format="png")
		
		# hist_res_vs_E.SetBinContent(i_E_edge+1, tmp_hist.GetRMS())
		if gaus_pars:
			hist_res_vs_E.SetBinContent(i_E_edge+1, gaus_pars[2])
			hist_res_vs_E.SetBinError(i_E_edge+1, gaus_pars[3])

	plot_single_hist(hist_res_vs_E, filebasename, out_dir_base, "E_{true} in GeV", colour_code=38, file_format="png")
	# plot_2D(rdf_resolution, 'pT_truthmatched_ys_from_higgs_noiso', 'y_resolution', out_dir_base)	

	
	return hist_res_vs_E   

def check_photon_resolutions_and_eff(input_filepath, out_dir_base):

	if not os.path.exists(out_dir_base):
		os.mkdir(out_dir_base)

	rdf = get_rdf(input_filepath)
	# print("Total events in dataframe:", rdf.Count().GetValue() )

	#total efficiencies for overview:
	rdf_yy_truth = rdf.Filter("n_truth_ys_from_higgs == 2") 
	n_yy_truth_total = rdf_yy_truth.Count().GetValue()
	rdf_yy_recomatched = rdf_yy_truth.Filter("n_truthmatched_ys_from_higgs_noiso == 2")
	rdf_yy_recomatched_wIso = rdf_yy_truth.Filter("n_truthmatched_ys_from_higgs == 2")
	n_evts_yy_recomatched = rdf_yy_recomatched.Count().GetValue()
	n_evts_yy_recomatched_wIso = rdf_yy_recomatched_wIso.Count().GetValue()
	print("Efficiency for 2 matched photons before iso: {:.2f}%".format(n_evts_yy_recomatched/n_yy_truth_total*100.))
	print("Efficiency for 2 matched photons after iso: {:.2f}%".format(n_evts_yy_recomatched_wIso/n_evts_yy_recomatched*100.))

	# print("Events with 2 truth photons", n_yy_truth_total )
	# print("Events with 2 reco matched photons", n_evts_yy_recomatched )
	# print("Events with 2 reco matched photons after iso", n_evts_yy_recomatched_wIso )

	#check resolutions

	#first only in bins of eta:
	list_of_hists =[]
	eta_edges = [0., 2.5, 4., 6]
	E_edges = [0., 10., 20., 30., 50., 100., 200.]

	#histogram properties based on the binning
	hist_binEdges = array("d", E_edges)
	hist_nBins = len(E_edges)-1

	for i_eta_edge in range(len(eta_edges)-1):
		hist_title = "{} < |#eta| < {}".format(eta_edges[i_eta_edge], eta_edges[i_eta_edge+1])
		hist_filebase = "E_resolution_eta_bin{}".format(i_eta_edge)
		cut_string_eta = "abs(eta_truth_ys_from_higgs[0]) > {:.2f} && abs(eta_truth_ys_from_higgs[0]) <= {:.2f}".format(eta_edges[i_eta_edge], eta_edges[i_eta_edge+1])
		print(cut_string_eta)
		hist_bin = check_photon_res_per_eta_bin(rdf_yy_recomatched, cut_string_eta, E_edges, hist_title, hist_filebase, out_dir_base)
		# model = ROOT.RDF.TH1DModel("resolution_model_hist", "resolution_model_hist", 40, -0.05, 0.05)

		# rdf_resolution = rdf_yy_recomatched.Define('y_resolution', '(E_truthmatched_ys_from_higgs_noiso[0] - E_truth_ys_from_higgs[0])/E_truth_ys_from_higgs[0]')
		# tmp_hist = rdf_resolution.Histo1D(model, 'y_resolution').GetValue()   
		# tmp_hist.SetTitle("{}, RMS = {:.4f}".format(hist_title, tmp_hist.GetRMS()) )     
		list_of_hists.append(hist_bin)

	plot_list_of_hists(list_of_hists, "y_E_resolution", out_dir_base, "E_{truth} in GeV", "#Delta E/E", file_format="png")

def check_eff_per_eta_bin_1lep(input_filepath, out_dir_base, with_iso=False, with_larger_dR=False):#(input_rdf, out_dir_base, flavour, with_iso=False, with_larger_dR=False):

	#how many of the 1 lepton events have 1 lepton? -> ideally link the truth particle to a reco particle!!

	if not os.path.exists(out_dir_base):
		os.mkdir(out_dir_base)

	#rdf = ROOT.RDataFrame("events", input_filepath)
	input_rdf = helpers.get_rdf(input_filepath)

	if not input_rdf:
		print("Empty file for:", input_filepath, " Exiting.")
		return

	eta_edges = [-6., -4., -2.5, -2.0, -1.5, -1.0, -0.5, 0., 0.5, 1.0, 1.5, 2.0, 2.5, 4., 6]
	pT_edges = [0., 20., 40., 60., 80., 100., 200.]

	#histogram properties based on the binning
	hist_binEdges = array("d", eta_edges)
	hist_nBins = len(eta_edges)-1

	list_of_hists =[]

	if with_iso and with_larger_dR:
		raiseException("Error in check_eff_per_bin_1lep - with_iso and with_larger_dR cannot be true at the same time.")

	recomatch_var = "n_truthmatched_ys_from_higgs_noiso"
	if with_iso:
		recomatch_var = "n_truthmatched_ys_from_higgs" 
	if with_larger_dR:
		recomatch_var = "n_truthmatched_ys_from_higgs"


	for i_pt_edge in range(len(pT_edges)-1):
		#write to file:
		file_name = "photon_efficiencies_vs_eta_pT_bin_{}.txt".format(i_pt_edge)
		file_path = os.path.join(out_dir_base, file_name)

		#fill a histogram
		hist_name = "hist_eff_vs_eta_pT_bin"+str(i_pt_edge)
		hist_eff_vs_eta = ROOT.TH1D(hist_name, hist_name, hist_nBins, hist_binEdges)
		hist_title = "{} < p_{{T}} < {}".format(pT_edges[i_pt_edge], pT_edges[i_pt_edge+1])

		with open(file_path, 'w') as outfile:
			eff_vs_eta = []
			cut_string_pT = "pT_truth_ys_from_higgs[0] > {:.2f} && pT_truth_ys_from_higgs[0] <= {:.2f}".format(pT_edges[i_pt_edge], pT_edges[i_pt_edge+1])
			for i_eta_edge in range(len(eta_edges)-1):
				cut_string_bin = cut_string_pT+" && eta_truth_ys_from_higgs[0] > {:.2f} && eta_truth_ys_from_higgs[0] <= {:.2f}".format(eta_edges[i_eta_edge], eta_edges[i_eta_edge+1])
				n_evts_bin_total = input_rdf.Filter(cut_string_bin).Count().GetValue()
				# n_evts_bin_total = rdf_evts_bin.Count().GetValue()
				n_evts_bin_recomatched = input_rdf.Filter(cut_string_bin+" && {} == 1".format(recomatch_var)).Count().GetValue()
				# n_evts_bin_recomatched = input_rdf.Filter(cut_string_bin+" && n_truthmatched_leps_from_HWW_noiso == 1").Count().GetValue()
				if n_evts_bin_total:
					eff_bin = n_evts_bin_recomatched/n_evts_bin_total*100.
				else:
					eff_bin = 0.
				eff_vs_eta.append(eff_bin)
				print(eff_bin)
				outfile.write("{} to {} GeV : {:.2f} \n".format(eta_edges[i_eta_edge], eta_edges[i_eta_edge+1], eff_bin))

				#fill the hist
				hist_eff_vs_eta.SetBinContent(i_eta_edge+1, eff_bin)

		hist_eff_vs_eta.SetTitle(hist_title)
		list_of_hists.append(hist_eff_vs_eta)

	if with_iso:
		histfile_name = "photon_efficiencies_vs_eta_afterIsolation.png"
	elif with_larger_dR:
		histfile_name = "photon_efficiencies_vs_eta_dR02.png"
	else:
		histfile_name = "photon_efficiencies_vs_eta.png"

	histfile_path = os.path.join(out_dir_base, histfile_name)
	canvas = ROOT.TCanvas("canvas", "canvas", 800, 800) 
	canvas.cd()

	leg = ROOT.TLegend(0.6, 0.2, 0.8, 0.4)

	for i_hist, hist in enumerate(list_of_hists):
		print("Plotting hist", i_hist)
		hist.SetLineWidth(2)
		hist.SetLineColor(30+i_hist*2)

		hist.SetMinimum(0.)
		hist.SetMaximum(105.)
		hist.GetYaxis().SetTitle("photon efficiency in %")
		hist.GetXaxis().SetTitle("#eta truth")
		hist.Draw("HIST SAME")

		leg.AddEntry(hist, hist.GetTitle(), "l")

	leg.SetFillStyle( 0 )
	leg.SetBorderSize( 0 )
	leg.SetTextFont( 43 )
	leg.SetTextSize( 22 )
	leg.SetColumnSeparation(-0.05)
	leg.Draw()

	canvas.SaveAs(histfile_path)


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Plot distributions for validation of new signal files")
	parser.add_argument('--input', '-i', metavar="INPUTFILE", dest="inPath", required=True, help="Path to the input directory")
	parser.add_argument('--outdir', '-o', metavar="OUTPUTDIR", dest="outDir", required=True, help="Output directory.")
	parser.add_argument('--op', '-op', metavar="task you want to do", dest="op", required=True, help="task you want to do")
	args = parser.parse_args()

	res_plotter = resolutionPlotter.ResolutionPlotter(args.inPath, args.outDir, "photon")
	res_plotter.filter_input_rdf("n_truth_ys_from_higgs == 2 && n_truthmatched_ys_from_higgs_noiso == 2") #use only a subset of events

	if args.op == "resolution_dE_vs_E":
		print("Plotting relative energy resolution vs E in bins of eta.")
		res_plotter.set_binning("eta_truth_ys_from_higgs", [0., 2.5, 4., 6], "|#eta_{truth}|", "E_truth_ys_from_higgs", [0., 50., 100., 200.], "E_{truth} in GeV")
		res_plotter.set_use_abs_eta(True)
		res_plotter.plot_resolution_histograms("E_res_eta_bins_vs_E", "E_truthmatched_ys_from_higgs_noiso", "E_truth_ys_from_higgs", "#sigmaE/E",  2)
	elif args.op == "resolution_dE_vs_eta":
		print("Plotting relative energy resolution vs eta in bins of E")
		res_plotter.set_binning("E_truth_ys_from_higgs", [0., 50., 100., 200.], "E_{truth} in GeV", "eta_truth_ys_from_higgs", [-6., -4., -2.5, -2.0, -1.5, -1.0, -0.5, 0., 0.5, 1.0, 1.5, 2.0, 2.5, 4., 6], "#eta_{truth}")
		res_plotter.set_use_abs_eta(False)
		res_plotter.plot_resolution_histograms("E_res_E_bins_vs_eta", "E_truthmatched_ys_from_higgs_noiso", "E_truth_ys_from_higgs", "#sigmaE/E",  2)
	elif args.op == "resolution_dP_vs_pT":
		print("Plotting relative momentum resolution vs pT in bins of eta")
		res_plotter.set_binning("eta_truth_ys_from_higgs", [0., 2.5, 4., 6], "|#eta_{truth}|", "pT_truth_ys_from_higgs", [0., 50., 100., 200.], "pT_{truth} in GeV")
		res_plotter.set_use_abs_eta(True)
		res_plotter.plot_resolution_histograms("P_res_eta_bins_vs_pT", "P_truthmatched_ys_from_higgs_noiso", "P_truth_ys_from_higgs", "#sigmaP/P",  2)
	elif args.op == "resolution_dP_vs_eta":
		print("Plotting relative momentum resolution vs eta in bins of pT")
		res_plotter.set_binning("pT_truth_ys_from_higgs", [0., 50., 100., 200.], "pT_{truth} in GeV", "eta_truth_ys_from_higgs", [-6., -4., -2.5, -2.0, -1.5, -1.0, -0.5, 0., 0.5, 1.0, 1.5, 2.0, 2.5, 4., 6], "#eta_{truth}")
		res_plotter.set_use_abs_eta(False)
		res_plotter.plot_resolution_histograms("P_res_pT_bins_vs_eta", "P_truthmatched_ys_from_higgs_noiso", "P_truth_ys_from_higgs", "#sigmaP/P",  2)

	#old fct/code
	# check_eff_per_eta_bin_1lep(args.inPath, args.outDir, False, False)
	#check_photon_resolutions_and_eff(args.inPath, args.outDir)
	# check_photon_eff(args.inPath, args.outDir)
	# check_myy_gen(args.inPath, args.outDir)


# python bbyy_eff_res_check.py -i /eos/user/b/bistapf/FCChh_EvtGen/FCCAnalysis_ntuples_noIso/pwp8_pp_hh_lambda100_5f_hhbbaa/chunk0.root -o ./bbyy_checks/
# python bbyy_eff_res_check.py -i /eos/user/b/bistapf/FCChh_EvtGen/FCCAnalysis_ntuples_noIso/pwp8_pp_hh_lambda100_5f_hhbbaa/ -o ./bbyy_checks/ #all chunks

#for checking the myy
# python bbyy_eff_res_check.py -i /eos/user/b/bistapf/FCChh_EvtGen/FCCAnalysis_ntuples_noIso/pwp8_pp_hh_lambda100_5f_hhbbaa/ -o ./bbyy_checks/ -op resolution_dE_vs_E