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

	hist.SetLineWidth(2)
	hist.SetLineColor(colour_code)
	hist.GetYaxis().SetTitle("Events")
	hist.GetXaxis().SetTitle(xaxis_label)
	hist.Draw("HIST")

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

def plot_list_of_hists(list_of_hists, histbasename, out_dir_base, xaxis_label, file_format="png"):
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
		hist.Draw("HIST SAME")
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
		cutstring_bin = "E_truthmatched_ys_from_higgs_noiso[0] > {:.2f} && E_truthmatched_ys_from_higgs_noiso[0] <= {:.2f}".format(E_edges[i_E_edge], E_edges[i_E_edge+1])
		rdf_bin = rdf_resolution.Filter(cutstring_bin)

		#store a histogram of the resolution 
		tmp_hist = rdf_bin.Histo1D(model, 'y_resolution').GetValue()   
		histfilename = "{}_E_{}_to_{}".format(filebasename, E_edges[i_E_edge], E_edges[i_E_edge+1])
		tmp_hist.SetTitle("{}, RMS = {:.4f}".format(hist_name, tmp_hist.GetRMS()) )     
		plot_single_hist(tmp_hist, histfilename, out_dir_base, "#DeltaE/E", colour_code=38, file_format="png")

		hist_res_vs_E.SetBinContent(i_E_edge+1, tmp_hist.GetRMS())

	plot_single_hist(hist_res_vs_E, filebasename, out_dir_base, "E_{true} in GeV", colour_code=38, file_format="png")
	# plot_2D(rdf_resolution, 'pT_truthmatched_ys_from_higgs_noiso', 'y_resolution', out_dir_base)	

	
	return hist_res_vs_E   

def check_photon_resolutions_and_eff(input_filepath, out_dir_base):

	if not os.path.exists(out_dir_base):
		os.mkdir(out_dir_base)

	rdf = get_rdf(input_filepath)

	#total efficiencies for overview:
	rdf_yy_truth = rdf.Filter("n_truth_ys_from_higgs == 2") 
	n_yy_truth_total = rdf_yy_truth.Count().GetValue()
	rdf_yy_recomatched = rdf_yy_truth.Filter("n_truthmatched_ys_from_higgs_noiso == 2")
	rdf_yy_recomatched_wIso = rdf_yy_truth.Filter("n_truthmatched_ys_from_higgs == 2")
	n_evts_yy_recomatched = rdf_yy_recomatched.Count().GetValue()
	n_evts_yy_recomatched_wIso = rdf_yy_recomatched_wIso.Count().GetValue()
	print("Efficiency for 2 matched photons before iso: {:.2f}%".format(n_evts_yy_recomatched/n_yy_truth_total*100.))
	print("Efficiency for 2 matched photons after iso: {:.2f}%".format(n_evts_yy_recomatched_wIso/n_evts_yy_recomatched*100.))

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

	plot_list_of_hists(list_of_hists, "y_E_resolution", out_dir_base, "#Delta E/E", file_format="png")




if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Plot distributions for validation of new signal files")
	parser.add_argument('--input', '-i', metavar="INPUTFILE", dest="inPath", required=True, help="Path to the input directory")
	parser.add_argument('--outdir', '-o', metavar="OUTPUTDIR", dest="outDir", required=True, help="Output directory.")
	args = parser.parse_args()

	check_photon_resolutions_and_eff(args.inPath, args.outDir)
	# check_photon_eff(args.inPath, args.outDir)
	# check_myy_gen(args.inPath, args.outDir)


# python bbyy_eff_res_check.py -i /eos/user/b/bistapf/FCChh_EvtGen/FCCAnalysis_ntuples_noIso/pwp8_pp_hh_lambda100_5f_hhbbaa/chunk0.root -o ./bbyy_checks/

#for checking the myy
# python bbyy_eff_res_check.py -i /eos/user/b/bistapf/FCChh_EvtGen/FCCAnalysis_ntuples_noIso/FCChh_EvtGen_pwp8_pp_hh_lambda100_5f_hhbbaa.root -o ./bbyy_checks/