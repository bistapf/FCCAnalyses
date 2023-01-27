# quick script checking efficiencies in the bbWW(lvlv) channel, with the new delphes card

from collections import namedtuple
import ROOT
import argparse
import os 
import matplotlib.pyplot as plt
from array import array

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)


def check_truth_brs(input_filepath, out_dir_base, plot_format=".png"):

	if not os.path.exists(out_dir_base):
		os.mkdir(out_dir_base)

	rdf = ROOT.RDataFrame("events", input_filepath)

	if not rdf:
		print("Empty file for:", input_filepath, " Exiting.")
		return

	#get the number of truth leptons from W(decay): 
	nevts_all = rdf.Count().GetValue()
	print("All evts", nevts_all)
	nevts_full_had = rdf.Filter("n_truth_leps_from_HWW == 0").Count().GetValue()
	nevts_full_had_rel = nevts_full_had/nevts_all*100.
	print("0 leps from W decay {} = {:.2f} %".format(nevts_full_had, nevts_full_had_rel))
	nevts_1lep = rdf.Filter("n_truth_leps_from_HWW == 1").Count().GetValue()
	nevts_1lep_rel = nevts_1lep/nevts_all*100.
	print("1 leps from W decay {} = {:.2f} %".format(nevts_1lep, nevts_1lep_rel))
	nevts_2lep = rdf.Filter("n_truth_leps_from_HWW == 2").Count().GetValue()
	nevts_2lep_rel = nevts_2lep/nevts_all*100.
	print("2 leps from W decay {} = {:.2f} %".format(nevts_2lep, nevts_2lep_rel))
	checker = nevts_full_had_rel+nevts_1lep_rel+nevts_2lep_rel
	print("Checking total", checker)
	print("Checking maximum two:", rdf.Filter("n_truth_leps_from_HWW > 2").Count().GetValue())

def get_rdf(input_filepath):

	rdf = ROOT.RDataFrame("events", input_filepath)
	if not rdf:
		print("Empty file for:", input_filepath, " Exiting.")
		return
	return rdf

def check_res_per_bin_1lep(input_file, out_dir_base, flavour):

	model = ROOT.RDF.TH1DModel("resolution_model_hist", "resolution_model_hist", 40, -0.05, 0.05)

	if not os.path.exists(out_dir_base):
		os.mkdir(out_dir_base)

	input_rdf = get_rdf(input_file)
	input_rdf_flavor = input_rdf.Filter("n_truth_leps_from_HWW == 1").Filter("abs(pdgID_truth_leps_from_HWW[0]) == {}".format(int(flavour)))

	eta_edges = [0., 2.5, 4., 6]
	p_edges = [0., 10., 20., 30., 50., 100., 200.]

	#histogram properties based on the binning
	hist_binEdges = array("d", p_edges)
	hist_nBins = len(p_edges)-1

	list_of_hists =[]
	for i_eta_edge in range(len(eta_edges)-1):
		hist_title = "{} < |#eta| < {}".format(eta_edges[i_eta_edge], eta_edges[i_eta_edge+1])
		cut_string_eta = "abs(eta_truth_leps_from_HWW[0]) > {:.2f} && abs(eta_truth_leps_from_HWW[0]) <= {:.2f}".format(eta_edges[i_eta_edge], eta_edges[i_eta_edge+1])
		rdf_recomatch = input_rdf_flavor.Filter(cut_string_eta+" && n_truthmatched_leps_from_HWW_noiso == 1")
		rdf_resolution = rdf_recomatch.Define('lep_resolution', '(E_truthmatched_leps_from_HWW_noiso[0] - E_truth_leps_from_HWW[0])/E_truth_leps_from_HWW[0]')
		tmp_hist = rdf_resolution.Histo1D(model, 'lep_resolution').GetValue()   
		tmp_hist.SetTitle("{}, RMS = {:.2f}".format(hist_title, tmp_hist.GetRMS()) )            
		list_of_hists.append(tmp_hist)

	canvas = ROOT.TCanvas("canvas", "canvas", 800, 800) 
	canvas.cd()
	histfile_name = "{}_E_resolution.png".format(flavour)
	histfile_path = os.path.join(out_dir_base, histfile_name)

	leg = ROOT.TLegend(0.55, 0.6, 0.9, 0.9)

	for i_hist, hist in enumerate(list_of_hists):
		print("Plotting hist", i_hist)
		hist.SetLineWidth(2)
		hist.SetLineColor(38+i_hist*4)

		hist.GetYaxis().SetTitle("Fraction of events")
		hist.GetXaxis().SetTitle("Delta(E)/E")
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


def check_eff_per_bin_1lep(input_rdf, out_dir_base, flavour):
	eta_edges = [0., 2.5, 4., 6]
	pT_edges = [0., 10., 20., 30., 50., 100., 200.]

	#histogram properties based on the binning
	hist_binEdges = array("d", pT_edges)
	hist_nBins = len(pT_edges)-1

	list_of_hists =[]


	for i_eta_edge in range(len(eta_edges)-1):
		#write to file:
		file_name = "{}_efficiencies_vs_pT_eta_bin_{}.txt".format(flavour, i_eta_edge)
		file_path = os.path.join(out_dir_base, file_name)

		#fill a histogram
		hist_name = "hist_eff_vs_pT_eta_bin"+str(i_eta_edge)
		hist_eff_vs_pT = ROOT.TH1D(hist_name, hist_name, hist_nBins, hist_binEdges)
		hist_title = "{} < |#eta| < {}".format(eta_edges[i_eta_edge], eta_edges[i_eta_edge+1])

		with open(file_path, 'w') as outfile:
			eff_vs_pT = []
			cut_string_eta = "abs(eta_truth_leps_from_HWW[0]) > {:.2f} && abs(eta_truth_leps_from_HWW[0]) <= {:.2f}".format(eta_edges[i_eta_edge], eta_edges[i_eta_edge+1])
			for i_pT_edge in range(len(pT_edges)-1):
				cut_string_bin = cut_string_eta+" && pT_truth_leps_from_HWW[0] > {:.2f} && pT_truth_leps_from_HWW[0] <= {:.2f}".format(pT_edges[i_pT_edge], pT_edges[i_pT_edge+1])
				n_evts_bin_total = input_rdf.Filter(cut_string_bin).Count().GetValue()
				# n_evts_bin_total = rdf_evts_bin.Count().GetValue()
				n_evts_bin_recomatched = input_rdf.Filter(cut_string_bin+" && n_truthmatched_leps_from_HWW_noiso_dr02 == 1").Count().GetValue()
				# n_evts_bin_recomatched = input_rdf.Filter(cut_string_bin+" && n_truthmatched_leps_from_HWW_noiso == 1").Count().GetValue()
				if n_evts_bin_total:
					eff_bin = n_evts_bin_recomatched/n_evts_bin_total*100.
				else:
					eff_bin = 0.
				eff_vs_pT.append(eff_bin)
				print(eff_bin)
				outfile.write("{} to {} GeV : {:.2f} \n".format(pT_edges[i_pT_edge], pT_edges[i_pT_edge+1], eff_bin))

				#fill the hist
				hist_eff_vs_pT.SetBinContent(i_pT_edge+1, eff_bin)

		hist_eff_vs_pT.SetTitle(hist_title)
		list_of_hists.append(hist_eff_vs_pT)


		# #plot
		# plt_name = "{}_efficiencies_vs_pT_eta_bin_{}.png".format(flavour, i_eta_edge)
		# plt.plot(pT_edges, eff_vs_pT)
		# plt.show()
		# plt.savefig(plt_name)

	histfile_name = "{}_efficiencies_vs_pT.png".format(flavour)
	histfile_path = os.path.join(out_dir_base, histfile_name)
	canvas = ROOT.TCanvas("canvas", "canvas", 800, 800) 
	canvas.cd()

	leg = ROOT.TLegend(0.7, 0.2, 0.9, 0.4)

	for i_hist, hist in enumerate(list_of_hists):
		print("Plotting hist", i_hist)
		hist.SetLineWidth(2)
		hist.SetLineColor(38+i_hist*4)

		hist.SetMinimum(0.)
		hist.SetMaximum(100.)
		hist.GetYaxis().SetTitle("{} efficiency in %".format(flavour))
		hist.GetXaxis().SetTitle("p_{T} truth in GeV")
		hist.Draw("HIST SAME")

		leg.AddEntry(hist, hist.GetTitle(), "l")

	leg.SetFillStyle( 0 )
	leg.SetBorderSize( 0 )
	leg.SetTextFont( 43 )
	leg.SetTextSize( 22 )
	leg.SetColumnSeparation(-0.05)
	leg.Draw()

	canvas.SaveAs(histfile_path)


	return 0

def check_lepton_eff(input_filepath, out_dir_base):

	#how many of the 1 lepton events have 1 lepton? -> ideally link the truth particle to a reco particle!!

	#first check: 2 lepton events, how many have at least 2 leptons? no truth links 

	if not os.path.exists(out_dir_base):
		os.mkdir(out_dir_base)

	rdf = ROOT.RDataFrame("events", input_filepath)

	if not rdf:
		print("Empty file for:", input_filepath, " Exiting.")
		return

	#check the 1 lepton case:
	print("Checking lepton efficiencies for 1 lepton events")
	rdf_lvqq_truth = rdf.Filter("n_truth_leps_from_HWW == 1") #Note this includes taus!!
	rdf_lvqq_truth_notaus = rdf.Filter("abs(pdgID_truth_leps_from_HWW[0]) == 11 || abs(pdgID_truth_leps_from_HWW[0]) == 13 ")
	n_evts_truth_1l_incl = rdf_lvqq_truth_notaus.Count().GetValue() #NO TAUS!
	n_evts_recomatched_1l_incl = rdf_lvqq_truth_notaus.Filter("n_truthmatched_leps_from_HWW_noiso == 1").Count().GetValue() #recomatch does NOT include taus!!
	print("Efficiency for 1 matched leps before iso: {:.2f}%".format(n_evts_recomatched_1l_incl/n_evts_truth_1l_incl*100.))

	#ELECTRONS
	rdf_1electron_truth = rdf_lvqq_truth.Filter("abs(pdgID_truth_leps_from_HWW[0]) == 11 ")
	n_1electron_truth_total = rdf_1electron_truth.Count().GetValue()
	n_evts_1electron_recomatched = rdf_1electron_truth.Filter("n_truthmatched_leps_from_HWW_noiso == 1").Count().GetValue()
	n_evts_1electron_recomatched_wIso = rdf_1electron_truth.Filter("n_truthmatched_leps_from_HWW == 1").Count().GetValue()
	print("Efficiency for 1 matched electron before iso: {:.2f}%".format(n_evts_1electron_recomatched/n_1electron_truth_total*100.))
	print("Efficiency for 1 matched electron after iso: {:.2f}%".format(n_evts_1electron_recomatched_wIso/n_1electron_truth_total*100.))

	check_eff_per_bin_1lep(rdf_1electron_truth, out_dir_base, "electron")

	#MUONS
	rdf_1muon_truth = rdf_lvqq_truth.Filter("abs(pdgID_truth_leps_from_HWW[0]) == 13 ")
	n_1muon_truth_total = rdf_1muon_truth.Count().GetValue()
	n_evts_1muon_recomatched = rdf_1muon_truth.Filter("n_truthmatched_leps_from_HWW_noiso == 1").Count().GetValue()
	n_evts_1muon_recomatched_wIso = rdf_1muon_truth.Filter("n_truthmatched_leps_from_HWW == 1").Count().GetValue()
	print("Efficiency for 1 matched muon before iso: {:.2f}%".format(n_evts_1muon_recomatched/n_1muon_truth_total*100.))
	print("Efficiency for 1 matched muon after iso: {:.2f}%".format(n_evts_1muon_recomatched_wIso/n_1muon_truth_total*100.))

	check_eff_per_bin_1lep(rdf_1muon_truth, out_dir_base, "muon")


	#check for weird events first
	print("Checking lepton efficiencies for 2 lepton events")
	rdf_lvlv_truth = rdf.Filter("n_truth_leps_from_HWW == 2")
	weird_events = rdf_lvlv_truth.Filter("n_truth_leps_from_HWW < n_truthmatched_leps_from_HWW_noiso").Count().GetValue()
	weird_events_iso = rdf_lvlv_truth.Filter("n_truth_leps_from_HWW < n_truthmatched_leps_from_HWW").Count().GetValue()
	if weird_events or weird_events_iso:
		print("Warning! Found more recomatched leptons than truth leptons! This shouldnt happen.")

	#count how many of those also have 2 reco matched leptons:
	n_evts_truth_2l = rdf_lvlv_truth.Count().GetValue()
	n_evts_recomatched_2l_noiso = rdf_lvlv_truth.Filter("n_truthmatched_leps_from_HWW_noiso == 2").Count().GetValue()
	n_evts_recomatched_2l_iso = rdf_lvlv_truth.Filter("n_truthmatched_leps_from_HWW == 2").Count().GetValue()
	print(n_evts_truth_2l, n_evts_recomatched_2l_noiso, n_evts_recomatched_2l_iso)

	print("Efficiency for 2 matched leps before iso: {:.2f}%".format(n_evts_recomatched_2l_noiso/n_evts_truth_2l*100.))
	print("Efficiency for 2 matched leps after iso: {:.2f}%".format(n_evts_recomatched_2l_iso/n_evts_truth_2l*100.))

	#require that the truth leptons have some pT and in eta range
	rdf_truth_2l_selected = rdf_lvlv_truth.Filter("abs(eta_truth_leps_from_HWW[0]) < 2.5 && abs(eta_truth_leps_from_HWW[1]) < 2.5")
	n_evts_truth_2l_selected = rdf_truth_2l_selected.Count().GetValue()
	n_evts_truth_2l_selected_recomatched_noiso = rdf_truth_2l_selected.Filter("n_truthmatched_leps_from_HWW_noiso == 2").Count().GetValue()
	print("Efficiency for 2 matched leps before iso, and |eta| truth < 2.5: {:.2f}%".format(n_evts_truth_2l_selected_recomatched_noiso/n_evts_truth_2l_selected*100.))




if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Plot distributions for validation of new signal files")
	parser.add_argument('--input', '-i', metavar="INPUTFILE", dest="inPath", required=True, help="Path to the input directory")
	parser.add_argument('--outdir', '-o', metavar="OUTPUTDIR", dest="outDir", required=True, help="Output directory.")
	args = parser.parse_args()

	#check_lepton_eff(args.inPath, args.outDir)
	# check_truth_brs(args.inPath, args.outDir)
	check_res_per_bin_1lep(args.inPath, args.outDir, 13)
	check_res_per_bin_1lep(args.inPath, args.outDir, 11)

# python bbww_lvlv_eff_rel_check.py -i /eos/user/b/bistapf/FCChh_EvtGen/FCCAnalysis_ntuples_noIso/pwp8_pp_hh_lambda100_5f_hhbbww/chunk0.root -o ./bbww_eff_check/
