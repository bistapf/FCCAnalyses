from collections import namedtuple
import ROOT
import argparse
import os 
import numpy as np

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptTitle(0)

def getHfromRDF(hist):
    h = None
    t = hist.GetValue()
    h = t.Clone()
    return h

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
			hist_binEdges = np.array(ref_var.nbins, dtype=float)
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
			filename = "bbtautau_noSel_"+plot_name+out_format
		else:
			filename = "bbtautau_withSel_"+plot_name+out_format
		fileout = os.path.join(out_dir_base, filename)

		canvas = ROOT.TCanvas("canvas", "canvas", 800, 800) 
		tmp_hist.Draw("hist same")
		canvas.SaveAs(fileout)

def makeEffPlots(dict_of_vars, ref_var, sel_cutstring, input_filepath, out_dir_base, out_format = ".png", do_log_y=False):

        if not os.path.exists(out_dir_base):
                os.mkdir(out_dir_base)

        rdf = ROOT.RDataFrame("events", input_filepath)

        if sel_cutstring:
                rdf = rdf.Filter(sel_cutstring) #apply the selection

        if not rdf:
                print("Empty file for:", input_filepath, " Exiting.")
                return

        #denominator hist
        print("Plotting at denominator:", ref_var.name)
        has_variable_binning = False
        
        if not isinstance(ref_var.nbins, int):
           has_variable_binning = True
           hist_binEdges = np.array(ref_var.nbins, dtype=float)
           hist_nBins = len(ref_var.nbins)-1
           model = ROOT.RDF.TH1DModel(ref_var.name+"_model_hist", ref_var.name, hist_nBins, hist_binEdges)
        else:
           model = ROOT.RDF.TH1DModel(ref_var.name+"_model_hist", ref_var.name, ref_var.nbins, ref_var.xmin, ref_var.xmax)
        
        tmp_hist_den = rdf.Histo1D(model, ref_var.name)
       
        if not tmp_hist_den.GetEntries():
           print("Empty histogram for:", input_filepath, " Exiting.")
           return
        else:
           print("Number entries denumerator: ", tmp_hist_den.GetEntries())
        tmp_den = getHfromRDF(tmp_hist_den)
        #tmp_hist.GetXaxis().SetTitle(plot.label)
        #tmp_hist.GetYaxis().SetTitle("Raw MC events")
        #tmp_hist.SetFillColor(ROOT.kCyan+2)
        #tmp_hist.SetLineColor(ROOT.kCyan+2)

        for plot_name, plot in dict_of_vars.items():
                print("Plotting:", plot_name)

                has_variable_binning = False
                if not isinstance(plot.nbins, int):
                        has_variable_binning = True
                        hist_binEdges = np.array(ref_var.nbins, dtype=float)
                        hist_nBins = len(plot.nbins)-1
                        model = ROOT.RDF.TH1DModel(plot_name+"_model_hist", plot_name, hist_nBins, hist_binEdges)
                else:
                        model = ROOT.RDF.TH1DModel(plot_name+"_model_hist", plot_name, plot.nbins, plot.xmin, plot.xmax)

                tmp_hist_num = rdf.Histo1D(model, plot.name)               
 
                if not tmp_hist_num.GetEntries():
                        print("Empty histogram for:", input_filepath, " Exiting.")
                        return
                else:
                        print("Number entries numerator: ", tmp_hist_num.GetEntries())

                tmp_num = getHfromRDF(tmp_hist_num)
               
                if ROOT.TEfficiency.CheckConsistency(tmp_num, tmp_den):
                   Eff = ROOT.TEfficiency(tmp_num, tmp_den)
                   Eff.SetTitle(";"+plot.label+";Efficiency")
                   Eff.SetTitle(plot_name)
                   ptext = ROOT.TPaveText(.7,.85,.85,.9,option='NDC')
                   if "loose" in plot_name:
                      ptext.AddText("loose tag")
                   elif "medium" in plot_name:
                      ptext.AddText("medium tag") 	
                   elif "tight" in plot_name:
                      ptext.AddText("tight tag")	
                   else:
                      ptext.AddText(plot_name)	                   
		   #write out
                   if sel_cutstring == "":
                      filename = "bbtautau_noSel_Eff"+plot_name+out_format
                   else:
                      filename = "bbtautau_withSel_Eff"+plot_name+out_format
                   fileout = os.path.join(out_dir_base, filename)

                   canvas = ROOT.TCanvas("canvas", "canvas", 900, 700) 
                   canvas.SetGrid()
                   Eff.Draw("AP")
                   canvas.Update()
                   graph = Eff.GetPaintedGraph()
                   graph.SetMinimum(0.6)
                   graph.SetMaximum(1) 
                   canvas.Update() 
                   #canvas.SetLogx()
                   ptext.Draw()
                   canvas.SaveAs(fileout)
                else:
                   print("The histograms are not consistent!")


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Plot distributions for validation of new signal files")
	parser.add_argument('--input', '-i', metavar="INPUTDIR", dest="inDir", required=True, help="Path to the input directory")
	parser.add_argument('--outdir', '-o', metavar="OUTPUTDIR", dest="outDir", required=True, help="Output directory.")
	args = parser.parse_args()

	##setup for bbtautau:
	infilepath = os.path.join(args.inDir, "FCChh_EvtGen_pwp8_pp_hh_lambda100_5f_hhbbtata.root")

	#use a custim namedntuple to transfer the plotting info
	PlotSpecs = namedtuple('PlotSpecs', ['name', 'xmin', 'xmax', 'label', 'nbins'])


	#plot some vars without any selection:
	bbtautau_plot_vars_nosel = {
		"n_b_jets_loose":PlotSpecs(name="n_b_jets_loose", xmin=0, xmax=5, label="n_b_jets_loose", nbins=5),
		"n_b_jets_medium":PlotSpecs(name="n_b_jets_medium", xmin=0, xmax=5, label="n_b_jets_medium", nbins=5),
		"n_b_jets_tight":PlotSpecs(name="n_b_jets_tight", xmin=0, xmax=5, label="n_b_jets_tight", nbins=5),
		"n_tau_jets_loose":PlotSpecs(name="n_tau_jets_loose", xmin=0, xmax=5, label="n_tau_jets_loose", nbins=5),
		"n_tau_jets_medium":PlotSpecs(name="n_tau_jets_medium", xmin=0, xmax=5, label="n_tau_jets_medium", nbins=5),
		"n_tau_jets_tight":PlotSpecs(name="n_tau_jets_tight", xmin=0, xmax=5, label="n_tau_jets_tight", nbins=5),
  		"n_jets_genmatched_b": PlotSpecs(name="n_jets_genmatched_b", xmin=0, xmax=5, label="n_jets_genmatched_b", nbins=5),
                "n_bjets_loose_genmatched_b": PlotSpecs(name="n_bjets_loose_genmatched_b", xmin=0, xmax=5, label="n_bjets_loose_genmatched_b", nbins=5),
                "n_bjets_medium_genmatched_b": PlotSpecs(name="n_bjets_medium_genmatched_b", xmin=0, xmax=5, label="n_bjets_medium_genmatched_b", nbins=5),
                "n_bjets_tight_genmatched_b": PlotSpecs(name="n_bjets_tight_genmatched_b", xmin=0, xmax=5, label="n_bjets_tight_genmatched_b", nbins=5),
                "n_jets_genmatched_wtruth_taus": PlotSpecs(name="n_jets_genmatched_wtruth_taus", xmin=0, xmax=5, label="n_jets_genmatched_wtruth_taus", nbins=5),              
		#"n_recomatched_truth_taus_loose": PlotSpecs(name="n_recomatched_truth_taus_loose", xmin=0, xmax=5, label="n_recomatched_truth_taus_loose", nbins=5),
                #"n_recomatched_truth_taus_medium": PlotSpecs(name="n_recomatched_truth_taus_medium", xmin=0, xmax=5, label="n_recomatched_truth_taus_medium", nbins=5),
                #"n_recomatched_truth_taus_tight": PlotSpecs(name="n_recomatched_truth_taus_tight", xmin=0, xmax=5, label="n_recomatched_truth_taus_tight", nbins=5),
		"n_truth_hadronic_taus":PlotSpecs(name="n_truth_hadronic_taus", xmin=0., xmax=10, label="n_truth_had_tau_fromHiggs", nbins=10),
                "n_truth_leptonic_taus":PlotSpecs(name="n_truth_leptonic_taus", xmin=0., xmax=10., label="n_truth_lep_tau_fromHiggs", nbins=10),
                "n_truth_taus":PlotSpecs(name="n_truth_taus", xmin=0., xmax=10., label="n_truth_tau_fromHiggs", nbins=10),
                "n_truth_hadronic_taus_sel":PlotSpecs(name="n_truth_hadronic_taus_sel", xmin=0., xmax=10., label="n_truth_had_tau_sel", nbins=10),
                "n_truth_hadronic_taus_all":PlotSpecs(name="n_truth_hadronic_taus_all", xmin=0., xmax=10., label="n_truth_had_tau_all", nbins=10),
                "n_MC_taus":PlotSpecs(name="n_MC_taus", xmin=0., xmax=10., label="n_MC_tau", nbins=10),
		"pT_jets_genmatched_wtruth_taus":PlotSpecs(name="pT_jets_genmatched_wtruth_taus", xmin=0., xmax=500., label="p_{T} jet matched #tau_{h} [GeV]", nbins=75),
                "pT_taus_loose_genmatched_wtruth_taus":PlotSpecs(name="pT_taus_loose_genmatched_wtruth_taus", xmin=0., xmax=500., label="p_{T} tau matched #tau_{h} [GeV]", nbins=75),
		"pT_truth_hadronic_taus":PlotSpecs(name="pT_truth_hadronic_taus", xmin=0., xmax=500., label="p_{T} truth #tau_{h} [GeV]", nbins=75),
		"eta_truth_hadronic_taus":PlotSpecs(name="eta_truth_hadronic_taus", xmin=-5., xmax=5., label="#eta truth #tau_{h} ", nbins=20),
                #"pT_recomatched_truth_taus_medium":PlotSpecs(name="pT_recomatched_truth_taus_medium", xmin=0., xmax=500., label="p_{T} truth #tau_{h} recomatched[GeV]", nbins=75),
                #"eta_recomatched_truth_taus_medium":PlotSpecs(name="eta_recomatched_truth_taus_medium", xmin=-5., xmax=5., label="#eta truth #tau_{h} recomatched", nbins=20),
		"pT_tau_jets_medium":PlotSpecs(name="pT_tau_jets_medium", xmin=0., xmax=500., label="p_{T} sel. #tau_{h} [GeV]", nbins=75), #plots the pT of both selected ys into one hist!
                "eta_tau_jets_medium":PlotSpecs(name="eta_tau_jets_medium", xmin=-5., xmax=5., label="#eta sel. #tau_{h} ", nbins=20), #plots the eta of both selected ys into one hist!
		
	}

	sel_cuts_empty = ""
	makePlots(bbtautau_plot_vars_nosel, sel_cuts_empty, infilepath, args.outDir)

        ##apply selection to be able to plot event wide kinematic variables
	sel_cuts = "n_b_jets_medium == 2 && n_tau_jets_medium == 2"

        #(hadronic) tau tagging efficiencies
	bbtautau_plot_pTeff={
	  "pT_taus_loose_genmatched_wtruth_taus":PlotSpecs(name="pT_taus_loose_genmatched_wtruth_taus", xmin=0., xmax=200., label="p_{T} #tau_{h} [GeV]", nbins=20),
          "pT_taus_medium_genmatched_wtruth_taus":PlotSpecs(name="pT_taus_medium_genmatched_wtruth_taus", xmin=0., xmax=200., label="p_{T} #tau_{h} [GeV]", nbins=20),
          "pT_taus_tight_genmatched_wtruth_taus":PlotSpecs(name="pT_taus_tight_genmatched_wtruth_taus", xmin=0., xmax=200., label="p_{T} #tau_{h} [GeV]", nbins=20),
         }
	bbtautau_plot_etaeff={
          "eta_taus_loose_genmatched_wtruth_taus":PlotSpecs(name="eta_taus_loose_genmatched_wtruth_taus", xmin=-5., xmax=5., label="#eta #tau_{h} ", nbins=20),
          "eta_taus_medium_genmatched_wtruth_taus":PlotSpecs(name="eta_taus_medium_genmatched_wtruth_taus", xmin=-5., xmax=5., label="#eta #tau_{h} ", nbins=20),
          "eta_taus_tight_genmatched_wtruth_taus":PlotSpecs(name="eta_taus_tight_genmatched_wtruth_taus", xmin=-5., xmax=5., label="#eta #tau_{h} ", nbins=20),
         }
	pT_ref = PlotSpecs(name="pT_jets_genmatched_wtruth_taus", xmin=0., xmax=200., label="p_{T} #tau_{h} [GeV]", nbins=20)
	eta_ref = PlotSpecs(name="eta_jets_genmatched_wtruth_taus", xmin=-5, xmax=5., label="#eta  #tau_{h}", nbins=20)

	makeEffPlots(bbtautau_plot_pTeff, pT_ref, sel_cuts_empty, infilepath, args.outDir)
	makeEffPlots(bbtautau_plot_etaeff, eta_ref, sel_cuts_empty, infilepath, args.outDir)
 
        #bjets tagging efficiencies
	binedges=[20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,250,300,350,400,450,500,600,700,800,900,1000,1250,1500]
	bbtautau_plot_pTeff={
	  "pT_bjets_loose_genmatched_b":PlotSpecs(name="pT_bjets_loose_genmatched_b", xmin=0., xmax=1000., label="p_{T} bjets [GeV]", nbins=binedges),
          "pT_bjets_medium_genmatched_b":PlotSpecs(name="pT_bjets_medium_genmatched_b", xmin=0., xmax=1000., label="p_{T} bjets [GeV]", nbins=binedges),
          "pT_bjets_tight_genmatched_b":PlotSpecs(name="pT_bjets_tight_genmatched_b", xmin=0., xmax=1000., label="p_{T} bjets [GeV]", nbins=binedges),
         }
	bbtautau_plot_etaeff={
          "eta_bjets_loose_genmatched_b":PlotSpecs(name="eta_bjets_loose_genmatched_b", xmin=-5., xmax=5., label="#eta bjets ", nbins=20),
          "eta_bjets_medium_genmatched_b":PlotSpecs(name="eta_bjets_medium_genmatched_b", xmin=-5., xmax=5., label="#eta bjets ", nbins=20),
          "eta_bjets_tight_genmatched_b":PlotSpecs(name="eta_bjets_tight_genmatched_b", xmin=-5., xmax=5., label="#eta bjets ", nbins=20),
         }
	pT_ref = PlotSpecs(name="pT_jets_genmatched_b", xmin=0., xmax=1000., label="p_{T} #tau_{h} [GeV]", nbins=binedges)
	eta_ref = PlotSpecs(name="eta_jets_genmatched_b", xmin=-5, xmax=5., label="#eta  #tau_{h}", nbins=20)

	makeEffPlots(bbtautau_plot_pTeff, pT_ref, sel_cuts_empty, infilepath, args.outDir)
	makeEffPlots(bbtautau_plot_etaeff, eta_ref, sel_cuts_empty, infilepath, args.outDir)
 
 
        ####### with selection
	bbtautau_plot_vars = {
		"m_bb":PlotSpecs(name="m_bb", xmin=80., xmax=200., label="m_{bb} [GeV]", nbins=60),
		"m_tauhtauh":PlotSpecs(name="m_tauhtauh", xmin=0., xmax=200., label="m_{#tau_{h}#tau_{h}} [GeV]", nbins=50),
		"pT_tau_jets_medium":PlotSpecs(name="pT_tau_jets_medium", xmin=0., xmax=500., label="p_{T} sel. #tau_{h} [GeV]", nbins=75), #plots the pT of both selected ys into one hist!
		"eta_tau_jets_medium":PlotSpecs(name="eta_tau_jets_medium", xmin=0., xmax=5., label="#eta sel. #tau_{h} ", nbins=20), #plots the eta of both selected ys into one hist!
		"pT_b_jets_medium":PlotSpecs(name="pT_b_jets_medium", xmin=0., xmax=500., label="p_{T} sel. b-jets [GeV]", nbins=75), #plots the pT of both selected bs into one hist!
		"eta_b_jets_medium":PlotSpecs(name="eta_b_jets_medium", xmin=0., xmax=5., label="#eta sel. pb-jets", nbins=20), #plots the eta of both selected bs into one hist!
	}

	makePlots(bbtautau_plot_vars, sel_cuts, infilepath, args.outDir)

#python bbtautau_valid.py -i /eos/user/b/bistapf/FCChh_EvtGen/FCCAnalysis_ntuples/ -o ./bbtautau_plots/
