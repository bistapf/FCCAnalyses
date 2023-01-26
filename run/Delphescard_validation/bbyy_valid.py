from collections import namedtuple
import ROOT
import argparse
import os 

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptTitle(0)

def makePlots(dict_of_vars, sel_cutstring, input_filepath, out_dir_base, out_format = ".png", do_log_y=False):

	if not os.path.exists(out_dir_base):
		os.mkdir(out_dir_base)

	rdf = ROOT.RDataFrame("events", input_filepath)

	if sel_cutstring:
		rdf = rdf.Filter(sel_cutstring) #apply the selection

	if not rdf:
		print("Empty file for:", input_filepath, " Exiting.")
		return

	for plot_name, plot in dict_of_vars.items():
		print("Plotting:", plot_name)

		has_variable_binning = False
		if not isinstance(plot.nbins, int):
			has_variable_binning = True
			hist_binEdges = array("d", plot.nbins)
			hist_nBins = len(plot.nbins)-1
			model = ROOT.RDF.TH1DModel(plot_name+"_model_hist", plot_name, hist_nBins, hist_binEdges)
		else:
			model = ROOT.RDF.TH1DModel(plot_name+"_model_hist", plot_name, plot.nbins, plot.xmin, plot.xmax)

		tmp_hist = rdf.Histo1D(model, plot.name)
		if not tmp_hist.GetEntries():
			print("Empty histogram for:", input_filepath, " Exiting.")
			return

		tmp_hist.GetXaxis().SetTitle(plot.label)
		tmp_hist.GetYaxis().SetTitle("Raw MC events")
		tmp_hist.SetFillColor(ROOT.kCyan+2)
		tmp_hist.SetLineColor(ROOT.kCyan+2)

		#write out
		if sel_cutstring == "":
			filename = "bbyy_noSel_"+plot_name+out_format
		else:
			filename = "bbyy_withSel_"+plot_name+out_format
		fileout = os.path.join(out_dir_base, filename)

		canvas = ROOT.TCanvas("canvas", "canvas", 800, 800) 
		tmp_hist.Draw("hist same")
		canvas.SaveAs(fileout)

def plot_ratio(dict_of_vars, sel_cutstring, input_filepath, out_dir_base, out_format = ".png", do_log_x=False):


	if not os.path.exists(out_dir_base):
		os.mkdir(out_dir_base)

	rdf = ROOT.RDataFrame("events", input_filepath)

	if sel_cutstring:
		rdf = rdf.Filter(sel_cutstring) #apply the selection

	if not rdf:
		print("Empty file for:", input_filepath, " Exiting.")
		return

	for plot_name, plot in dict_of_vars.items():
		print("Plotting:", plot_name)

		has_variable_binning = False
		if not isinstance(plot.nbins, int):
			has_variable_binning = True
			hist_binEdges = array("d", plot.nbins)
			hist_nBins = len(plot.nbins)-1
			model = ROOT.RDF.TH1DModel(plot_name+"_model_hist", plot_name, hist_nBins, hist_binEdges)
		else:
			model = ROOT.RDF.TH1DModel(plot_name+"_model_hist", plot_name, plot.nbins, plot.xmin, plot.xmax)

		tmp_hist1 = rdf.Histo1D(model, plot.var1)
		tmp_hist2 = rdf.Histo1D(model, plot.var2)

		if not tmp_hist1.GetEntries():
			print("Empty histogram for:", input_filepath, "in", var1, "Exiting.")
			return

		if not tmp_hist2.GetEntries():
			print("Empty histogram for:", input_filepath, "in", var2, "Exiting.")
			return

		ratio = tmp_hist1.Clone()
		ratio.Divide(tmp_hist2.GetValue())

		ratio.GetXaxis().SetTitle(plot.label)
		ratio.GetYaxis().SetTitle(plot.name)
		ratio.SetLineColor(ROOT.kCyan+2)
		ratio.SetLineWidth(2)

			

		#write out
		if sel_cutstring == "":
			filename = "bbyy_noSel_"+plot_name+out_format
		else:
			filename = "bbyy_withSel_"+plot_name+out_format
		fileout = os.path.join(out_dir_base, filename)

		canvas = ROOT.TCanvas("canvas", "canvas", 800, 800) 
		canvas.SetLogx(do_log_x)
		ratio.Draw("hist same")
		canvas.SaveAs(fileout)




if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Plot distributions for validation of new signal files")
	parser.add_argument('--input', '-i', metavar="INPUTDIR", dest="inDir", required=True, help="Path to the input directory")
	parser.add_argument('--outdir', '-o', metavar="OUTPUTDIR", dest="outDir", required=True, help="Output directory.")
	args = parser.parse_args()

	##setup for bbyy:
	infilepath = os.path.join(args.inDir, "pwp8_pp_hh_5f_hhbbyy_tester_new_card.root")
	# infilepath = os.path.join(args.inDir, "FCChh_EvtGen_pwp8_pp_hh_5f_hhbbyy_tester_new_card.root")

	#use a custim namedntuple to transfer the plotting info
	PlotSpecs = namedtuple('PlotSpecs', ['name', 'xmin', 'xmax', 'label', 'nbins'])


	#plot some vars without any selection:
	bbyy_plot_vars_nosel = {
		"n_b_jets_loose":PlotSpecs(name="n_b_jets_loose", xmin=0., xmax=5., label="n_b_jets_loose", nbins=5),
		"n_b_jets_medium":PlotSpecs(name="n_b_jets_medium", xmin=0., xmax=5., label="n_b_jets_medium", nbins=5),
		"n_b_jets_tight":PlotSpecs(name="n_b_jets_tight", xmin=0., xmax=5., label="n_b_jets_tight", nbins=5),
		"n_photons":PlotSpecs(name="n_photons", xmin=0., xmax=30., label="n_photons", nbins=30),
		"n_photons_iso":PlotSpecs(name="n_photons_iso", xmin=0., xmax=10., label="n_photons_iso", nbins=10),
		"n_photons_sel":PlotSpecs(name="n_photons_sel", xmin=0., xmax=10., label="n_photons_sel", nbins=10),
		"n_MC_photons_sel":PlotSpecs(name="n_MC_photons_sel", xmin=0., xmax=200., label="n_MC_photons_sel", nbins=20),
	}

	sel_cuts_empty = ""
	makePlots(bbyy_plot_vars_nosel, sel_cuts_empty, infilepath, args.outDir)

	#ratios:
	#use a custim namedntuple to transfer the plotting info
	RatioSpecs = namedtuple('PlotSpecs', ['name', 'var1', 'var2', 'xmin', 'xmax', 'label', 'nbins'])

	bbyy_efficiencies = {
		"y_eff_vs_pT":RatioSpecs(name="Photon Efficiency", var1="pT_photons", var2="pT_MC_photons_sel", xmin=0., xmax=200., label="p_{T}^{#gamma} in GeV", nbins=20),
	}

	plot_ratio(bbyy_efficiencies, sel_cuts_empty, infilepath, args.outDir)

	#with log x axis:
	bbyy_efficiencies_logX = {
		"y_eff_vs_pT_logX":RatioSpecs(name="Photon Efficiency", var1="pT_photons", var2="pT_MC_photons_sel", xmin=1.e-2, xmax=1.e5, label="p_{T}^{#gamma} in GeV", nbins=1000),
	}

	plot_ratio(bbyy_efficiencies_logX, sel_cuts_empty, infilepath, args.outDir, do_log_x=True)

	#TEMP: Only presel plots!!
	exit()

	##apply selection to be able to plot event wide kinematic variables

	sel_cuts = "n_b_jets_medium == 2 && n_photons_sel == 2"


	bbyy_plot_vars = {
		"m_bb":PlotSpecs(name="m_bb", xmin=80., xmax=200., label="m_{bb} [GeV]", nbins=60),
		"m_yy":PlotSpecs(name="m_yy", xmin=115., xmax=135., label="m_{yy} [GeV]", nbins=40),
		"pT_photons_sel":PlotSpecs(name="pT_photons_sel", xmin=0., xmax=500., label="p_{T} sel. photons [GeV]", nbins=150), #plots the pT of both selected ys into one hist!
		"eta_photons_sel":PlotSpecs(name="eta_photons_sel", xmin=0., xmax=5., label="#eta sel. photons", nbins=25), #plots the eta of both selected ys into one hist!
		"pT_b_jets_medium":PlotSpecs(name="pT_b_jets_medium", xmin=0., xmax=500., label="p_{T} sel. b-jets [GeV]", nbins=150), #plots the pT of both selected bs into one hist!
		"eta_b_jets_medium":PlotSpecs(name="eta_b_jets_medium", xmin=0., xmax=5., label="#eta sel. pb-jets", nbins=25), #plots the eta of both selected bs into one hist!
	}

	makePlots(bbyy_plot_vars, sel_cuts, infilepath, args.outDir)

#python bbyy_valid.py -i /eos/user/b/bistapf/FCChh_EvtGen/FCCAnalysis_ntuples/ -o ./bbyy_plots/