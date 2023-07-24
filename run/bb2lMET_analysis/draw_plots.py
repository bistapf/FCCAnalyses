import ROOT
import os
from collections import namedtuple
import json
import copy
import math
from array import array
import argparse
import bb2lMET_plots as plot_list

import yaml #TEMP !?

from bb2lMET_processes import bbzz_processes, bbzz_processes_new, bbtautau_processes, bbtautau_processes_new, bbWW_processes, bbWW_processes_new, all_processes, bbWW_processes_kl, bb2l_DFOS_processes
from bb2l_categories import bb2l_cats

from bb2lMET_plots import plot_list_2D

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)



bbZZllvv_labels_dict = {
	"sel2_bJets":"#it{HH(bbZZ)} analysis, Pre-Sel.",
	"sel3_mll":"#it{HH(bbZZ)} analysis, Pre-Sel.",
	"sel9_dphiZMET_12":"#it{HH(bbZZ)} analysis, Kin. Sel.",
	"sel9_dPhiHH":"#it{HH(bbZZ)} analysis, Kin. Sel.",
	"sel9_mlb_150":"#it{HH(bbXX(2l+MET))} SF, Z peak analysis, Kin. Sel.",
}

bbtautau_emu_labels_dict = {
	"sel2_bJets":"#it{HH(bb#tau#tau(e#mu))} analysis, Pre-Sel.",
	"sel9_dphiZMET_12":"#it{HH(bb#tau#tau(e#mu))} analysis, Kin. Sel.",
}

bbtautau_SF_labels_dict = {
	"sel2_bJets":"#it{HH(bb#tau#tau(ee+#mu#mu))} analysis, Pre-Sel.",
	"sel9_dphiZMET_12":"#it{HH(bb#tau#tau(ee+#mu#mu))} analysis, Kin. Sel.",
}

bbWW_emu_labels_dict = {
	"sel2_bJets":"#it{HH(bbWW(e#mu))} analysis, Pre-Sel.",
	"sel9_mlb_150":"#it{HH(bbWW(e#mu))} analysis, Kin. Sel.",
	"sel8_HT2_ratio":"#it{HH(bbWW(e#mu))} analysis, Kin. Sel. (no mlb cut)",
}

bbWW_SF_labels_dict ={
	"sel2_bJets":"#it{HH(bbWW(ee+#mu#mu))} analysis, Pre-Sel.",
	"sel2_bJets_medium":"#it{HH(bbWW(ee+#mu#mu))} analysis, Pre-Sel.",
	"sel9_mlb_150":"#it{HH(bbWW(ee+#mu#mu))} analysis, Kin. Sel.",
	"sel8_HT2_ratio":"#it{HH(bbWW(ee+#mu#mu))} analysis, Kin. Sel. (no mlb cut)",
	
}

def buildFileName(input_dir, sample, cut_level):
	# filenames_list = []
	# for sample in sample_list:
	# filename = sample+"_"+cut_level+".root"
		# filenames_list.append(os.path.join(input_dir, filename))
	if cut_level == "": 
		return os.path.join(input_dir,sample+".root")
	else:
		return os.path.join(input_dir,sample+"_"+cut_level+".root")
	# return filenames_list

def addOverflowToLastBin(hist):
	# print("Adding overflow to last bin for histogram:", hist.GetName())
	overflow_index = hist.GetNbinsX()+1
	if hist.IsBinOverflow(overflow_index):
		# print ("Found overflow bin with index", overflow_index, "merging content with previous bin!")
		overflow = hist.GetBinContent(overflow_index)
		lastbin = hist.GetBinContent(overflow_index-1)
		hist.SetBinContent(overflow_index-1, overflow+lastbin)
		# print ("Added together overflow =", overflow, "and last bin content", lastbin, "in histogram of name", hist.GetName())


#first get the # of events that were processed: needed for denominator and stored only in the original tree, not the filtered ones
def getEvtsProcessedDict(input_dir, processes):
	nevts_dir = {}
	sow_dir = {}

	for proc in processes:
		for sample in processes[proc].sample_list:

			yamlfile=os.path.join("/afs/cern.ch/work/f/fccsw/public/FCCDicts/yaml/FCChh/fcc_v05_scenarioI", sample+'/merge.yaml')
			with open(yamlfile) as ftmp:
				try:
					doc = yaml.load(ftmp, Loader=yaml.FullLoader)
				except yaml.YAMLError as exc:
					print(exc)
				except IOError as exc:
					print ("I/O error({0}): {1}".format(exc.errno, exc.strerror))
					print ("outfile ",outfile)
				finally:
					print ('----> yaml file {} succesfully opened'.format(yamlfile))

			sow = doc["merge"]["sumofweights"]
			nevts = doc["merge"]["nevents"]

			nevts_dir[sample] = nevts
			sow_dir[sample] = sow

			#overwrite to use the yaml for now -> not ideal use the Tparameter next time!!!
			# filepath_presel = os.path.join(input_dir, sample+".root")
			
			# #open the file, load the value:
			# file_in = ROOT.TFile.Open(filepath_presel)
			# nevts_processed = -1.
			# for key in file_in.GetListOfKeys():
			# 	if 'eventsProcessed' == key.GetName():
			# 		nevts_processed = file_in.eventsProcessed.GetVal()
			# 		break

			# if nevts_processed < 0:
			# 	raise Exception("Error in getEvtsProcessedDict! Could not find #evts processed for sample "+sample)

			# nevts_dir[sample] = nevts_processed

	return nevts_dir, sow_dir

def getNormFactor(sample, nevts_dir, proc_dict_path = "/afs/cern.ch/user/b/bistapf/FCCAnalyses/run/HH_bbZZ_analysis/xsec_dir_tester.json", lumi=30e+06):
	norm_factor = -1.

	#number of processed events should have been written to the dictionary already
	nevts_proc = nevts_dir[sample]

	#read x-section etc from the json file:
	if '.json' in proc_dict_path:
		with open(proc_dict_path, 'r') as dict_file:
			proct_dict = json.load(dict_file)
	else:
		raise Exception("Error in getNormFactor: Only support .json files for the cross-section values currently!")

	norm_factor = lumi*proct_dict[sample]["crossSection"]*proct_dict[sample]["kfactor"]*proct_dict[sample]["matchingEfficiency"]/nevts_proc

	# print("built normfactor from:")
	# print("#evts = ", nevts_proc)
	# print("x-sec = ", proct_dict[sample]["crossSection"])
	# print("k-factor = ", proct_dict[sample]["kfactor"])
	# print("match-eff = ", proct_dict[sample]["matchingEfficiency"])
	# print("lumi = ", lumi)
	# print("norm_factor = ", norm_factor)

	if norm_factor < 0:
		raise Exception("Error in getNormFactor: Probably missing a factor in the normalisation ...")

	return norm_factor



def makePlot(variable, input_dir, processes, cut_level, nevts_dict, out_dir_base, labels_dict, plots_dict, weighted=False, store_root_file=False, out_format = ".png", do_log_y=True, lumi=30e+06, addOverlow=False, fix_ratio_range=(), extra_cut=("",""), signal_cat="" ):
	#get the namedtuple info for the variable we want to plot:
	plot = plots_dict[variable]
	print("Plotting", variable, "at cut-level", cut_level)
	if weighted:
		print("Applying MC events weights")
	cut_name = cut_level


	if extra_cut[0]:
		extra_cut_name = "_"+extra_cut[0]
		extra_cut = extra_cut[1]
		# extra_cut_name = extra_cut.replace(" ", "_").replace(">", "ge").replace("<", "le").replace("=","eq").replace("&&", "and").replace("||", "or").replace(".", "p").replace("[0]", "").replace("abs", "").replace("(", "").replace(")", "")
		cut_name+=extra_cut_name
	else:
		extra_cut_name=""
		extra_cut=""


	#going to need a TH1Model to fill:
	has_variable_binning = False
	if not isinstance(plot.nbins, int):
		has_variable_binning = True
		hist_binEdges = array("d", plot.nbins)
		hist_nBins = len(plot.nbins)-1
		#init the histogram with variable bin widths:
		model = ROOT.RDF.TH1DModel(variable+"_model_hist", variable, hist_nBins, hist_binEdges)
		signal_hist = ROOT.TH1D(variable+"_sig_hist", variable, hist_nBins, hist_binEdges)
		data_hist = ROOT.TH1D("data_obs", "data_obs", hist_nBins, hist_binEdges)

	else:
		model = ROOT.RDF.TH1DModel(variable+"_model_hist", variable, plot.nbins, plot.xmin, plot.xmax)
		signal_hist = ROOT.TH1D(variable+"_sig_hist", variable, plot.nbins, plot.xmin, plot.xmax )
		data_hist = ROOT.TH1D("data_obs", "data_obs", plot.nbins, plot.xmin, plot.xmax )
	
	bkg_hists_list = []
	
	for proc in processes:
		# print(proc)

		if has_variable_binning:
			# print("Setting up hist with variable binning")
			bkg_tmp_hist = ROOT.TH1D(proc+"_"+variable+"_bkg_hist", variable, hist_nBins, hist_binEdges )
		else:
			# print("Setting up hist with normal binning")
			bkg_tmp_hist = ROOT.TH1D(proc+"_"+variable+"_bkg_hist", variable, plot.nbins, plot.xmin, plot.xmax )

		#need to open multiple files for some: 
		for sample in processes[proc].sample_list:
			filepath = buildFileName(input_dir, sample, cut_level)
			# print(sample)

			#check if tree exists first:
			input_file = ROOT.TFile(filepath)
			if not input_file.Get("events"):
				print("Empty file for:", sample, " Skipping.")
				input_file.Close()
				continue
			input_file.Close()
			

			rdf = ROOT.RDataFrame("events", filepath)

			if not rdf:
				print("Empty file for:", sample, " Skipping.")
				continue

			#if running with extra cut string, apply that selection
			if extra_cut:
				rdf = rdf.Filter(extra_cut)

			if weighted:
				tmp_hist = rdf.Histo1D(model, plot.name, "weight")
			else:
				tmp_hist = rdf.Histo1D(model, plot.name)
			# print(tmp_hist.GetEntries())

			#skip if nothing passes selection:
			if not tmp_hist.GetEntries():
				print("Empty histogram for:", sample, " Skipping.")
				continue

			norm_factor = getNormFactor(sample, nevts_dict )
			# print(sample, norm_factor, tmp_hist.GetEntries(), tmp_hist.GetEntries()*norm_factor )
			tmp_hist.Scale(norm_factor)

			if addOverlow:
				addOverflowToLastBin(tmp_hist)

			#set plotting properties:
			tmp_hist.SetTitle(processes[proc].title)

			if "signal" in proc:
				# print("Adding signal hist for", proc, "with integral", tmp_hist.Integral() )
				hist_to_add = copy.deepcopy(tmp_hist.GetValue())
				signal_hist.Add(hist_to_add)
				signal_hist.SetLineColor(processes[proc].colour_key)
				signal_hist.SetLineWidth(3)
				signal_hist.SetTitle(processes[proc].title)

			else:
				hist_to_add = copy.deepcopy(tmp_hist.GetValue())
				bkg_tmp_hist.Add(hist_to_add)
				bkg_tmp_hist.SetLineColor(processes[proc].colour_key)
				bkg_tmp_hist.SetFillColor(processes[proc].colour_key)



		#add each bkg hist to the stack after it is built from all its samples:
		if not "signal" in proc:
			hist_to_stack = copy.deepcopy(bkg_tmp_hist)
			hist_to_stack.SetTitle(processes[proc].title)

			#check how many events are in very high pT regime:
			# if "pT_Hbb_cand" in variable or "pT_HZZ_cand" in variable:
			# 	print("Checking high pT regime of", variable)
			# 	boundary_bin_index = hist_to_stack.FindBin(200.)
			# 	n_bins_last = hist_to_stack.GetNbinsX()
			# 	print("Process is", proc, " and found", hist_to_stack.Integral(boundary_bin_index, n_bins_last+1 ), "normalised bkg events > 200 GeV")
			# 	print("Boundary bin has n_entries =", hist_to_stack.GetBinContent(boundary_bin_index), "bkg events")
			# 	addOverflowToLastBin(hist_to_stack)


			bkg_hists_list.append(hist_to_stack)
			data_hist.Add(hist_to_stack)



	#should have signal hist + bkg stack now:
	# print("Signal hist has integral", signal_hist.Integral())

	#sort the bkgs by size:
	bkg_hists_list = sorted(bkg_hists_list, key=lambda hist: hist.Integral())
	bkg_stack = ROOT.THStack("hist_stack","")
	for bkg_hist in bkg_hists_list:
		bkg_stack.Add(bkg_hist)

	#draw stuff:
	canvas = ROOT.TCanvas("canvas", "canvas", 800, 800) 
	#add ratio:
	pad_up = ROOT.TPad("pad_up", "pad_up", 0., 0., 1., 1.)
	pad_up.SetFillStyle(0)
	pad_up.SetBottomMargin(0.32)
	pad_up.SetTopMargin(0.03)
	pad_up.SetLeftMargin(0.13)
	pad_up.SetRightMargin(0.05)
	pad_up.SetLogy(do_log_y)
	pad_up.Draw()

	pad_low = ROOT.TPad("pad_low", "pad_low", 0., 0., 1., 1.);
	pad_low.SetFillStyle(0)
	pad_low.SetBottomMargin(0.12)
	pad_low.SetTopMargin(0.72)
	pad_low.SetLeftMargin(0.13)
	pad_low.SetRightMargin(0.05)
	pad_low.SetGrid()
	pad_low.Draw()

	#
	pad_up.cd()

	bkg_stack.Draw("hist")
	signal_hist.Draw("hist same")

	#axes:
	bkg_stack.SetMinimum(1.e0)
	bkg_stack.SetMaximum(1.e13)
	bkg_stack.GetYaxis().SetTitle("Events")
	bkg_stack.GetXaxis().SetLabelSize(0)
	signal_hist.GetXaxis().SetTitle(plot.label)

	#labels:
	Text = ROOT.TLatex()

	Text.SetNDC() 

	Text.SetTextAlign(12);
	Text.SetNDC(ROOT.kTRUE) 
	Text.SetTextSize(0.025) 
	Text.DrawLatex(0.17, 0.95, "#it{FCC-hh Simulation (Delphes)}") 
	lumi_tag = "#bf{{ #sqrt{{s}} = {:.0f} TeV, L = {:.0f} ab^{{-1}} }}".format(100., lumi/1e6)
	Text.DrawLatex(0.17, 0.9, lumi_tag)
	ana_tag = "#bf{{ {} }}".format(labels_dict[cut_level])
	Text.DrawLatex(0.17, 0.85, ana_tag)

	#legend
	legsize = 0.05*((len(bkg_hists_list)+1)/2)
	# leg = ROOT.TLegend(0.58,0.86 - legsize,0.86,0.88)
	# leg.Draw()
	leg = ROOT.TLegend(0.6, 0.95 - legsize, 0.95, 0.95)
	for bkg in reversed(bkg_hists_list):
		leg.AddEntry(bkg, bkg.GetTitle(), "f")
	leg.AddEntry(signal_hist, signal_hist.GetTitle(), "l")

	leg.SetFillStyle( 0 )
	leg.SetBorderSize( 0 )
	leg.SetTextFont( 43 )
	leg.SetTextSize( 22 )
	leg.SetNColumns( 2 )
	leg.SetColumnSeparation(-0.05)
	leg.Draw()

	#ratio panel
	hist_ratio = signal_hist.Clone()
	hist_ratio.Divide( bkg_stack.GetStack().Last() )
	hist_ratio.GetYaxis().SetTitle("S/B")
	hist_ratio.GetYaxis().SetTitleOffset(1.95)
	hist_ratio.GetYaxis().SetNdivisions(6)

	#set some fixed ratio: 
	if fix_ratio_range:
		hist_ratio.GetYaxis().SetRangeUser(fix_ratio_range[0], fix_ratio_range[1])


	pad_low.cd()
	pad_low.Update()
	hist_ratio.Draw("E0P")
	pad_low.RedrawAxis()

	canvas.RedrawAxis()
	canvas.Modified()
	canvas.Update()	

	#store into directory of the cutlevel, for easier sorting:
	out_dir = os.path.join(out_dir_base, cut_level)
	if not os.path.exists(out_dir):
		os.makedirs(out_dir)

	if weighted:
		filename = cut_name+"_"+variable+"_weighted"+out_format
	else:
		filename = cut_name+"_"+variable+out_format
		
	fileout = os.path.join(out_dir, filename)


	canvas.SaveAs(fileout)


	#write out a root file for use in WS building if requested:
	if store_root_file:
		filename = signal_cat+"_histograms_"+variable+"_"+cut_name+".root"
		fileoutpath = os.path.join(out_dir_base, "WS_Input")
		if not os.path.exists(fileoutpath):
			os.makedirs(fileoutpath)
		fileoutpath = os.path.join(fileoutpath, filename)
		fileout = ROOT.TFile(fileoutpath, "RECREATE")
		fileout.cd()

		#subdirectories for categories
		# if "_dphi" in extra_cut:
		if extra_cut:
			fileout.mkdir(extra_cut_name.strip("_"))
			fileout.cd(extra_cut_name.strip("_"))

		#signal
		if "bbWW" in signal_cat:
			signal_hist.SetName("ggHH_kl_1_kt_1_hbbhww")
			signal_hist.SetTitle("ggHH_kl_1_kt_1_hbbhww")
		elif "bbtautau" in signal_cat:
			signal_hist.SetName("ggHH_kl_1_kt_1_hbbhtautau")
			signal_hist.SetTitle("ggHH_kl_1_kt_1_hbbhtautau")
		elif "bbZZ" in signal_cat:
			signal_hist.SetName("ggHH_kl_1_kt_1_hbbhzz")
			signal_hist.SetTitle("ggHH_kl_1_kt_1_hbbhzz")
		elif "bb2l" in signal_cat:
			signal_hist.SetName("ggHH_kl_1_kt_1")
			signal_hist.SetTitle("ggHH_kl_1_kt_1")
		else:
			print("WARNING! SignalCat not set - using default name signal for signal process.")
			signal_hist.SetName("signal")
			signal_hist.SetTitle("signal")



		signal_hist.Write()

		print("total signal evts = ", signal_hist.Integral())

		for bkg_hist in bkg_hists_list:
			proc_name = bkg_hist.GetName().split(variable)[0].rstrip("_")
			# print(proc_name)
			bkg_hist.SetName(proc_name)
			bkg_hist.SetTitle(proc_name)
			bkg_hist.SetLineColor(ROOT.kBlack)
			bkg_hist.Write()
			print("total {} evts = {}".format(proc_name, bkg_hist.Integral()) )

		#add an observation

		#this somehow stopped working??
		# obs_hist = bkg_stack.GetStack().Last().Clone("data_obs")
		# obs_hist.SetName("data_obs")
		# obs_hist.SetTitle("data_obs")
		# obs_hist.Write()

		data_hist.Write()

		print("Wrote root file:", fileoutpath)

		fileout.Close()

def setup_hist_template(plot, hist_type="model"):
	has_variable_binning = False
	if not isinstance(plot.nbins, int):
		has_variable_binning = True
		hist_binEdges = array("d", plot.nbins)
		hist_nBins = len(plot.nbins)-1

		if hist_type == "model":
			return  ROOT.RDF.TH1DModel("temp_hist", "temp_hist", hist_nBins, hist_binEdges)
		else:
			return ROOT.TH1D("temp_hist", "temp_hist", hist_nBins, hist_binEdges)

	else:

		if hist_type == "model":
			return ROOT.RDF.TH1DModel("temp_hist", "temp_hist", plot.nbins, plot.xmin, plot.xmax)
		else:
			return ROOT.TH1D("temp_hist", "temp_hist", plot.nbins, plot.xmin, plot.xmax)

#single 2d plot for one process only
def plot_2D(input_dir, out_dir, sample, cut_level, var1, var2, out_format = ".png"):

	plot1 = plot_list_2D[var1]
	plot2 = plot_list_2D[var2]

	if not os.path.exists(out_dir):
		os.mkdir(out_dir)

	filepath = buildFileName(input_dir, sample, cut_level)

	rdf = ROOT.RDataFrame("events", filepath)

	# hist_var1 = rdf.Histo1D(var1)

	# hist_var1.Draw()

	hist_2D = rdf.Histo2D(ROOT.RDF.TH2DModel(plot1.name, plot2.name, plot1.nbins, plot1.xmin, plot1.xmax, plot2.nbins, plot2.xmin, plot2.xmax), plot1.name, plot2.name)
	# 40,"xmin":0,"xmax":800

	corr_coeff = hist_2D.GetCorrelationFactor()
	print(corr_coeff)
	#save it:
	canvas_name = var1+"_vs_"+var2
	canvas = ROOT.TCanvas(canvas_name, canvas_name, 800, 800) 
	canvas.SetLeftMargin(0.15)
	canvas.SetRightMargin(0.15)
	canvas.cd()

	hist_2D.GetXaxis().SetTitle(plot1.label)
	hist_2D.GetYaxis().SetTitle(plot2.label)
	hist_2D.Draw("COLZ")

	canvas.SaveAs(out_dir+canvas_name+".png" )


#plot shape comparison:
def plot_shape_compare(plots_dict, list_procs, cut_level, input_dir, out_dir, nevts_dict, out_format = ".png", fillBkg=False, extra_cut=""):

	if not os.path.exists(out_dir):
		os.mkdir(out_dir)

	cut_name = cut_level
	if extra_cut[0]:
		extra_cut_name = "_"+extra_cut[0]
		extra_cut = extra_cut[1]
		# extra_cut_name = extra_cut.replace(" ", "_").replace(">", "ge").replace("<", "le").replace("=","eq").replace("&&", "and").replace("||", "or").replace(".", "p").replace("[0]", "").replace("abs", "").replace("(", "").replace(")", "")
		cut_name+=extra_cut_name
	else:
		extra_cut_name=""
		extra_cut=""


	for plot_key, plot in plots_dict.items():
		print(plot_key, plot)

		# plot = plots[variable]
		print("Plotting shape comparison for ", plot.name, "at cut-level", cut_level, "for processes:", list_procs)
		hist_list =[]
		hist_stack = ROOT.THStack("hist_stack","")

		for proc in list_procs:

			model = setup_hist_template(plot, hist_type="model")
			
			hist_temp = setup_hist_template(plot, hist_type="hist")
			hist_temp.SetName(all_processes[proc].title)
			hist_temp.SetTitle(all_processes[proc].title)

			for sample in all_processes[proc].sample_list:
				filepath = buildFileName(input_dir, sample, cut_level)

				#check if tree exists first:
				input_file = ROOT.TFile(filepath)
				if not input_file.Get("events"):
					continue
				input_file.Close()

				rdf = ROOT.RDataFrame("events", filepath)

				if not rdf:
					continue

				if extra_cut:
					rdf = rdf.Filter(extra_cut)

				tmp = rdf.Histo1D(model, plot.name)
				norm_factor = getNormFactor(sample, nevts_dict )
				tmp.Scale(norm_factor)

				hist_to_add = copy.deepcopy(tmp.GetValue())

				hist_temp.Add(hist_to_add)


			#prettify hists
			hist_temp.GetXaxis().SetTitle(plot.label)
			hist_temp.GetYaxis().SetTitle("Fraction of events")
			hist_temp.SetLineWidth(3)
			hist_temp.SetLineColor(all_processes[proc].colour_key)

			if not "lambda" in sample and fillBkg:
				hist_temp.SetFillColor(all_processes[proc].colour_key)


			hist_list.append(hist_temp)

			hist_temp.Scale(1./hist_temp.Integral())
			hist_stack.Add(hist_temp)



		#setup plot
		canvas = ROOT.TCanvas("canvas", "canvas", 800, 800) 
		canvas.SetLeftMargin(0.13)
		canvas.cd()

		leg = ROOT.TLegend(0.65, 0.75, 0.90, 0.85)
		leg.SetFillStyle( 0 )
		leg.SetBorderSize( 0 )
		
		hist_stack.Draw("NOSTACK HIST")

		hist_stack.GetXaxis().SetTitle(plot.label)
		hist_stack.GetYaxis().SetTitle("Fraction of events")

		for hist in hist_list:
			# hist.DrawNormalized("HIST SAME")

			if not "HH" in hist.GetTitle():
				leg.AddEntry(hist, hist.GetTitle(), "f")
			else:
				leg.AddEntry(hist, hist.GetTitle(), "l")

		leg.Draw()

		filename = "shape_compare_"+plot_key+"_"+cut_name+out_format
		fileout = os.path.join(out_dir, filename)

		canvas.SaveAs(fileout)
		canvas.Close()

#compare vars on same process
def plot_shape_compare_vars(plots_dict, proc, cut_level, input_dir, out_dir, nevts_dict, out_format = ".png", addRatio=True):

	if not os.path.exists(out_dir):
		os.mkdir(out_dir)

	hist_list =[]
	hist_stack = ROOT.THStack("hist_stack","")
	name_string = ""

	colour_index = 30

	for plot_key, plot in plots_dict.items():
		print(plot_key, plot)

		name_string+=(plot.name+"_")

		# plot = plots[variable]
		# print("Plotting shape comparison for ", plot.name, "at cut-level", cut_level, "for processes:", list_procs)


		model = setup_hist_template(plot, hist_type="model")
		
		hist_temp = setup_hist_template(plot, hist_type="hist")
		hist_temp.SetName(all_processes[proc].title)
		# hist_temp.SetTitle(all_processes[proc].title)
		hist_temp.SetTitle(plot_key)

		for sample in all_processes[proc].sample_list:
			filepath = buildFileName(input_dir, sample, cut_level)

			#check if tree exists first:
			input_file = ROOT.TFile(filepath)
			if not input_file.Get("events"):
				continue
			input_file.Close()

			rdf = ROOT.RDataFrame("events", filepath)

			if not rdf:
				continue

			#some vars need to be defined:
			if plot.name == "MET_x_res":
				# print("Defining column")
				rdf = rdf.Define("MET_x_res", "(MET_x[0]-truth_MET_x_H_only[0])/truth_MET_x_H_only[0]")
			if plot.name == "MET_res":
				# print("Defining column")
				rdf = rdf.Define("MET_res", "(MET[0]-truth_MET_H_only[0])/truth_MET_H_only[0]")
			if plot.name == "MET_res_abs":
				# print("Defining column")
				rdf = rdf.Define("MET_res_abs", "MET[0]-truth_MET_H_only[0]")
			if plot.name == "MET_res_abs_smear":
				# print("Defining column")
				rdf = rdf.Define("MET_res_abs_smear", "MET_recalc-truth_MET_H_only[0]")
			if plot.name == "MET_res_smear":
				# print("Defining column")
				rdf = rdf.Define("MET_res_smear", "(MET_recalc-truth_MET_H_only[0])/truth_MET_H_only[0]")
			if plot.name == "m_ll_diff":
				rdf = rdf.Define("m_ll_diff", "m_ll[0] - m_ll_new")
			if plot.name == "m_bb_diff":
				rdf = rdf.Define("m_bb_diff", "m_bb[0] - m_bb_new")
			if plot.name == "px_bb_diff":
				rdf = rdf.Define("px_bb_diff", "px_Hbb_cand[0] - px_bb_new")
			if plot.name == "px_ll_diff":
				rdf = rdf.Define("px_ll_diff", "px_ll[0] - px_ll_new")
			if plot.name == "MET_diff_in_evt":
				rdf = rdf.Define("MET_diff_in_evt", "MET_recalc - MET[0]")
			if plot.name == "MET_x_diff_in_evt":
				rdf = rdf.Define("MET_x_diff_in_evt", "MET_x_smeared - MET_x[0]")
			if plot.name == "MET_y_diff_in_evt":
				rdf = rdf.Define("MET_y_diff_in_evt", "MET_y_smeared - MET_y[0]")
			if plot.name == "MET_ratio_in_evt":
				rdf = rdf.Define("MET_ratio_in_evt", "MET_recalc / MET[0]")
			if plot.name == "MET_x_ratio_in_evt":
				rdf = rdf.Define("MET_x_ratio_in_evt", "MET_x_smeared / MET_x[0]")
			if plot.name == "MET_y_ratio_in_evt":
				rdf = rdf.Define("MET_y_ratio_in_evt", "MET_y_smeared / MET_y[0]")

			tmp = rdf.Histo1D(model, plot.name)
			norm_factor = getNormFactor(sample, nevts_dict )
			tmp.Scale(norm_factor)

			hist_to_add = copy.deepcopy(tmp.GetValue())

			hist_temp.Add(hist_to_add)


			#prettify hists
			hist_temp.GetXaxis().SetTitle(plot.label)
			hist_temp.GetYaxis().SetTitle("Fraction of events")
			hist_temp.SetLineWidth(3)
			hist_temp.SetLineColor(colour_index)
			# hist_temp.SetLineColor(all_processes[proc].colour_key)

			if "truth" in plot_key:
				print("Steting truth hist")
				hist_temp.SetTitle("Truth")
				hist_temp.SetLineColor(ROOT.kBlack)

			elif "reco" in plot_key:
				hist_temp.SetTitle("Reco")
				# hist_temp.SetLineColor(ROOT.kBlack)



		hist_temp.SetTitle(plot_key+", RMS= {:.2f}".format(hist_temp.GetRMS()))
		# print(hist_temp.GetRMS())
		hist_list.append(hist_temp)

		hist_temp.Scale(1./hist_temp.Integral())
		hist_stack.Add(hist_temp)

		colour_index+=5



	#setup plot
	#add ratio panel if requested:
	canvas = ROOT.TCanvas("canvas", "canvas", 800, 800) 

	if addRatio:
		pad_up = ROOT.TPad("pad_up", "pad_up", 0., 0., 1., 1.)
		pad_up.SetFillStyle(0)
		pad_up.SetBottomMargin(0.32)
		pad_up.SetTopMargin(0.03)
		pad_up.SetLeftMargin(0.13)
		pad_up.SetRightMargin(0.05)
		pad_up.Draw()

		pad_low = ROOT.TPad("pad_low", "pad_low", 0., 0., 1., 1.);
		pad_low.SetFillStyle(0)
		pad_low.SetBottomMargin(0.12)
		pad_low.SetTopMargin(0.72)
		pad_low.SetLeftMargin(0.13)
		pad_low.SetRightMargin(0.05)
		pad_low.SetGrid()
		pad_low.Draw()

		#
		pad_up.cd()

	else:
		canvas.SetLeftMargin(0.15)
		canvas.SetBottomMargin(0.15)
		canvas.cd()

	leg = ROOT.TLegend(0.65, 0.75, 0.90, 0.85)
	leg.SetFillStyle( 0 )
	leg.SetBorderSize( 0 )
	
	hist_stack.Draw("NOSTACK HIST")

	hist_stack.GetXaxis().SetTitle(plot.label)
	hist_stack.GetYaxis().SetTitle("Fraction of events")

	if addRatio:
		hist_stack.GetHistogram().GetXaxis().SetTickLength(0)
		hist_stack.GetHistogram().GetXaxis().SetLabelOffset(999)
		hist_stack.GetXaxis().SetTitle("")

	for hist in hist_list:
		# hist.DrawNormalized("HIST SAME")


		leg.AddEntry(hist, hist.GetTitle(), "l")

	leg.Draw()

	if addRatio:
		leg = pad_up.BuildLegend(0.65, 0.75, 0.90, 0.85)
		leg.SetFillStyle( 0 )
		leg.SetBorderSize( 0 )
		leg.SetMargin( 0.1 )
		leg.Draw()

		pad_low.cd()

		#make the ratio
		hist_ratio = hist_stack.GetHists().At(0).Clone()
		hist_ratio.SetName("hist_ratio")
		hist_ratio.SetTitle("hist_ratio")
		# hist_ratio.GetYaxis().SetRangeUser(0.5, 1.5)
		hist_ratio.GetYaxis().SetNdivisions(6)

		hist_ratio.Divide(hist_stack.GetHists().At(1))
		hist_ratio.GetYaxis().SetTitle("Ratio")

		hist_ratio.Draw("E0P")


	filename = "shape_compare_vars_"+name_string+cut_level+out_format
	fileout = os.path.join(out_dir, filename)

	canvas.SaveAs(fileout)
	canvas.Close()

#compare with different cuts
def plot_shape_compare_cuts(plots_dict, proc, cuts_dict, input_dir, out_dir, nevts_dict, out_format = ".png"):

	if not os.path.exists(out_dir):
		os.mkdir(out_dir)



	for plot_key, plot in plots_dict.items():
		# print(plot_key, plot)
		print("Plotting variable:", plot_key)

		hist_list =[]
		hist_stack = ROOT.THStack("hist_stack","")
		name_string = plot_key+"_"
		

		# plot = plots[variable]
		# print("Plotting shape comparison for ", plot.name, "at cut-level", cut_level, "for processes:", list_procs)

		for cut_label, cut in cuts_dict.items():

			name_string+=(cut_label+"_")

			model = setup_hist_template(plot, hist_type="model")
			
			hist_temp = setup_hist_template(plot, hist_type="hist")
			# hist_temp.SetName(cut)
			hist_temp.SetTitle(cut_label)

			for sample in all_processes[proc].sample_list:
				filepath = buildFileName(input_dir, sample, "")

				#check if tree exists first:
				input_file = ROOT.TFile(filepath)
				if not input_file.Get("events"):
					continue
				input_file.Close()

				rdf = ROOT.RDataFrame("events", filepath)

				if not rdf:
					continue

				rdf = rdf.Filter(cut)

				tmp = rdf.Histo1D(model, plot.name)
				norm_factor = getNormFactor(sample, nevts_dict )
				tmp.Scale(norm_factor)

				hist_to_add = copy.deepcopy(tmp.GetValue())

				hist_temp.Add(hist_to_add)


				#prettify hists
				hist_temp.GetXaxis().SetTitle(plot.label)
				hist_temp.GetYaxis().SetTitle("Fraction of events")
				hist_temp.SetLineWidth(3)
				hist_temp.SetLineColor(all_processes[proc].colour_key)

				if not "lambda" in sample:
					hist_temp.SetFillColor(all_processes[proc].colour_key)

				#ugly hack to have different colours without another dict for colours ..
				if "pre" in cut_label:
					hist_temp.SetLineColor(ROOT.kBlack)
				elif "<" in cut_label:
					hist_temp.SetLineColor(ROOT.kCyan+2)
				elif ">" in cut_label:
					hist_temp.SetLineColor(ROOT.kMagenta+2)

				hist_list.append(hist_temp)

				hist_temp.Scale(1./hist_temp.Integral())
				hist_stack.Add(hist_temp)



		#setup plot
		canvas = ROOT.TCanvas("canvas", "canvas", 800, 800) 
		canvas.SetLeftMargin(0.13)
		canvas.cd()

		leg = ROOT.TLegend(0.65, 0.75, 0.90, 0.85)
		leg.SetFillStyle( 0 )
		leg.SetBorderSize( 0 )
		
		hist_stack.Draw("NOSTACK HIST")

		hist_stack.GetXaxis().SetTitle(plot.label)
		hist_stack.GetYaxis().SetTitle("Fraction of events")

		for hist in hist_list:
			# hist.DrawNormalized("HIST SAME")


			leg.AddEntry(hist, hist.GetTitle(), "l")

		leg.Draw()


		filename = "shape_compare_cuts_"+name_string+out_format
		fileout = os.path.join(out_dir, filename)

		canvas.SaveAs(fileout)
		canvas.Close()

#2D input for workspaces

def make_2D_fit_binning(var1, bins1, var2, bins2, processes, cut_level, input_dir, out_dir, nevts_dict, labels_dict, out_format = ".png", do_log_y=True, lumi=30e+06, fix_ratio_range=(), store_root_file=True, signal_cat="", sort_by_ratio=False ):

	var1 = "mlb_reco"
	bins1 = [0., 100., 150., 200., 10000.]
	
	var2 = "mT2_HH"
	bins2 = [0., 100., 125., 150., 10000.]

	

	n_bins = (len(bins1)-1)*(len(bins2)-1)

	signal_hist = ROOT.TH1D(var1+"_"+var2+"_bins_sig", var1+"_"+var2+"_bins_sig", n_bins, 0., n_bins)

	bkg_hists_list = []

	nevts_lines_bkg = {}
	nevts_lines_sig = {}

	#for each process make the 2D histogram


	for proc in processes:

		bin_index = 1
		
		tmp_hist = ROOT.TH1D(proc+"_"+var1+"_"+var2+"_bins_sig", proc+"_"+var1+"_"+var2+"_bins_sig", n_bins, 0., n_bins)
		# tmp_hist.Sumw2()

		for index_1 in range(0, len(bins1)-1):
			for index_2 in range(0, len(bins2)-1):
				
				cut_string = "{}[0] > {:.2f} && {}[0] < {:.2f} && {}[0] > {:.2f} && {}[0] < {:.2f}".format(var1, bins1[index_1], var1, bins1[index_1+1], var2, bins2[index_2], var2, bins2[index_2+1])
				# print(cut_string)
				#now get the signal and S/B

				print(bin_index, cut_string)
			
				nevts_bin_temp = 0

				if "pp_hh" in proc:
					nevts_lines = nevts_lines_sig

				else:
					nevts_lines = nevts_lines_bkg

				for sample in processes[proc].sample_list:
					filepath = buildFileName(input_dir, sample, cut_level)

					#check if tree exists first:
					input_file = ROOT.TFile(filepath)
					if not input_file.Get("events"):
						continue
					input_file.Close()

					rdf = ROOT.RDataFrame("events", filepath)

					if not rdf:
						continue

					rdf = rdf.Filter(cut_string)
					norm_factor = getNormFactor(sample, nevts_dict )
					nevts_bin_temp += rdf.Count().GetValue() * norm_factor

				# print(proc, nevts_bin_temp)
				# dict_entry_name = "{}_bin_{:.0f}".format(proc, bin_index)
				nevts_lines[bin_index] = [proc, cut_string, nevts_bin_temp]

				tmp_hist.AddBinContent(bin_index, nevts_bin_temp)

				bin_index += 1

		tmp_hist.SetTitle(processes[proc].title)

		if "signal" in proc:
			signal_hist.Add(tmp_hist)
			signal_hist.SetLineColor(processes[proc].colour_key)
			signal_hist.SetLineWidth(3)
			signal_hist.SetTitle(processes[proc].title)
		else:
			tmp_hist.SetLineColor(processes[proc].colour_key)
			tmp_hist.SetFillColor(processes[proc].colour_key)
			bkg_hists_list.append(tmp_hist)



	#check s/sqrt(B)
	for bin_index, [sig, cut_string, n_evts_sig] in nevts_lines_sig.items():
		print("BIN:", bin_index, "w. sel.", cut_string)
		# print(sig, n_evts_sig)
		[proc_bkg, cut_string, n_evts_bkg] = nevts_lines_bkg[bin_index]
		# print(proc_bkg, n_evts_bkg)
		print("S/sqrt(B) = {:.2f}".format(n_evts_sig/math.sqrt(n_evts_bkg)))

	print("Signal total=", signal_hist.Integral())

	#sort the bkgs by size:
	bkg_hists_list = sorted(bkg_hists_list, key=lambda hist: hist.Integral())
	bkg_stack = ROOT.THStack("hist_stack","")
	for bkg_hist in bkg_hists_list:
		print(bkg_hist.GetName(), bkg_hist.Integral())
		bkg_stack.Add(bkg_hist)



	#sort the bins by S/B
	if sort_by_ratio:
		dict_bins_in_order = {}
		hist_ratio = signal_hist.Clone()
		hist_ratio.Sumw2()
		hist_ratio.Divide( bkg_stack.GetStack().Last() )

		print("Unsorted")
		for bin_index in range(0, hist_ratio.GetNbinsX()+1):
			print(bin_index, hist_ratio.GetBinContent(bin_index) )
			dict_bins_in_order[bin_index] = hist_ratio.GetBinContent(bin_index)
		#sort the dictionary
		dict_bins_in_order= dict(sorted(dict_bins_in_order.items(), key=lambda item: item[1], reverse=True))

		print("Sorted")
		for bin_index, sb_value in dict_bins_in_order.items():
			print(bin_index, sb_value)

		#now need to fill new hists for each proc

		#signal first
		signal_hist_sorted = ROOT.TH1D(var1+"_"+var2+"_bins_sig", var1+"_"+var2+"_bins_sig", n_bins, 0., n_bins)

		new_bin=1
		for bin_index, sb_value in dict_bins_in_order.items():
			print(new_bin, signal_hist.GetBinContent(bin_index))
			signal_hist_sorted.SetBinContent(new_bin, signal_hist.GetBinContent(bin_index))
			new_bin+=1

		signal_hist_sorted.SetLineColor(signal_hist.GetLineColor())
		signal_hist_sorted.SetLineWidth(3)
		signal_hist_sorted.SetTitle(signal_hist.GetTitle())

		#same for all hists in bkglist
		bkg_hists_list_sorted = []
		for bkg_hist in bkg_hists_list:
			bkg_hist_sorted = ROOT.TH1D(var1+"_"+var2+"_bins_sig", var1+"_"+var2+"_bins_sig", n_bins, 0., n_bins)

			bkg_hist_sorted.SetFillColor(bkg_hist.GetFillColor())
			bkg_hist_sorted.SetLineColor(bkg_hist.GetFillColor())
			bkg_hist_sorted.SetTitle(bkg_hist.GetTitle())
			bkg_hist_sorted.SetName(bkg_hist.GetName())

			new_bin=1
			for bin_index, sb_value in dict_bins_in_order.items():
				bkg_hist_sorted.SetBinContent(new_bin, bkg_hist.GetBinContent(bin_index))
				new_bin+=1

			bkg_hists_list_sorted.append(bkg_hist_sorted)

		#overwrite:
		signal_hist = signal_hist_sorted
		bkg_hists_list = bkg_hists_list_sorted

		bkg_stack = ROOT.THStack("hist_stack","")
		for bkg_hist in bkg_hists_list:
			print(bkg_hist.GetName(), bkg_hist.Integral())
			bkg_stack.Add(bkg_hist)







#draw stuff:
	canvas = ROOT.TCanvas("canvas", "canvas", 800, 800) 
	#add ratio:
	pad_up = ROOT.TPad("pad_up", "pad_up", 0., 0., 1., 1.)
	pad_up.SetFillStyle(0)
	pad_up.SetBottomMargin(0.32)
	pad_up.SetTopMargin(0.03)
	pad_up.SetLeftMargin(0.13)
	pad_up.SetRightMargin(0.05)
	pad_up.SetLogy(do_log_y)
	pad_up.Draw()

	pad_low = ROOT.TPad("pad_low", "pad_low", 0., 0., 1., 1.);
	pad_low.SetFillStyle(0)
	pad_low.SetBottomMargin(0.12)
	pad_low.SetTopMargin(0.72)
	pad_low.SetLeftMargin(0.13)
	pad_low.SetRightMargin(0.05)
	pad_low.SetGrid()
	pad_low.Draw()

	#
	pad_up.cd()

	bkg_stack.Draw("hist")
	signal_hist.Draw("hist same")

	#axes:
	bkg_stack.SetMinimum(1.e-1)
	bkg_stack.SetMaximum(1.e12)
	bkg_stack.GetYaxis().SetTitle("Events")
	bkg_stack.GetXaxis().SetLabelSize(0)
	signal_hist.GetXaxis().SetTitle("Bin index")

	#labels:
	Text = ROOT.TLatex()

	Text.SetNDC() 

	Text.SetTextAlign(12);
	Text.SetNDC(ROOT.kTRUE) 
	Text.SetTextSize(0.025) 
	Text.DrawLatex(0.17, 0.95, "#it{FCC-hh Simulation (Delphes)}") 
	lumi_tag = "#bf{{ #sqrt{{s}} = {:.0f} TeV, L = {:.0f} ab^{{-1}} }}".format(100., lumi/1e6)
	Text.DrawLatex(0.17, 0.9, lumi_tag)
	ana_tag = "#bf{{ {} }}".format(labels_dict[cut_level])
	Text.DrawLatex(0.17, 0.85, ana_tag)

	#legend
	legsize = 0.05*((len(bkg_hists_list)+1)/2)
	# leg = ROOT.TLegend(0.58,0.86 - legsize,0.86,0.88)
	# leg.Draw()
	leg = ROOT.TLegend(0.6, 0.95 - legsize, 0.95, 0.95)
	for bkg in reversed(bkg_hists_list):
		leg.AddEntry(bkg, bkg.GetTitle(), "f")
	leg.AddEntry(signal_hist, signal_hist.GetTitle(), "l")

	leg.SetFillStyle( 0 )
	leg.SetBorderSize( 0 )
	leg.SetTextFont( 43 )
	leg.SetTextSize( 22 )
	leg.SetNColumns( 2 )
	leg.SetColumnSeparation(-0.05)
	leg.Draw()

	#ratio panel
	hist_ratio = signal_hist.Clone()
	hist_ratio.Sumw2()
	hist_ratio.Divide( bkg_stack.GetStack().Last() )
	hist_ratio.GetYaxis().SetTitle("S/B")
	hist_ratio.GetYaxis().SetTitleOffset(1.95)
	hist_ratio.GetYaxis().SetNdivisions(6)

	#set some fixed ratio: 
	if fix_ratio_range:
		hist_ratio.GetYaxis().SetRangeUser(fix_ratio_range[0], fix_ratio_range[1])


	pad_low.cd()
	pad_low.Update()
	hist_ratio.Draw("E0P")
	pad_low.RedrawAxis()

	canvas.RedrawAxis()
	canvas.Modified()
	canvas.Update()	

	#store into directory of the cutlevel, for easier sorting:
	out_dir = os.path.join(out_dir, cut_level)
	if not os.path.exists(out_dir):
		os.makedirs(out_dir)

	if sort_by_ratio:
		filename = var1+"_"+var2+"_bins_sorted_by_SoB"+out_format
	else:
		filename = var1+"_"+var2+"_bins"+out_format
	
	fileout = os.path.join(out_dir, filename)

	canvas.SaveAs(fileout)

	#write out a root file for use in WS building if requested:
	if store_root_file:
		if sort_by_ratio:
			filename = signal_cat+"_histograms_"+var1+"_"+var2+"_bins_sorted_by_SoB_"+cut_level+".root"
		else:
			filename = signal_cat+"_histograms_"+var1+"_"+var2+"_bins_"+cut_level+".root"
		fileoutpath = os.path.join(out_dir, "WS_Input")
		if not os.path.exists(fileoutpath):
			os.makedirs(fileoutpath)
		fileoutpath = os.path.join(fileoutpath, filename)
		fileout = ROOT.TFile(fileoutpath, "RECREATE")
		fileout.cd()

		#signal
		if "bbWW" in signal_cat:
			signal_hist.SetName("ggHH_kl_1_kt_1_hbbhww")
			signal_hist.SetTitle("ggHH_kl_1_kt_1_hbbhww")
		elif "bbtautau" in signal_cat:
			signal_hist.SetName("ggHH_kl_1_kt_1_hbbhtautau")
			signal_hist.SetTitle("ggHH_kl_1_kt_1_hbbhtautau")
		elif "bbZZ" in signal_cat:
			signal_hist.SetName("ggHH_kl_1_kt_1_hbbhzz")
			signal_hist.SetTitle("ggHH_kl_1_kt_1_hbbhzz")
		elif "bb2l" in signal_cat:
			signal_hist.SetName("ggHH_kl_1_kt_1")
			signal_hist.SetTitle("ggHH_kl_1_kt_1")
		else:
			print("WARNING! SignalCat not set - using default name signal for signal process.")
			signal_hist.SetName("signal")
			signal_hist.SetTitle("signal")



		signal_hist.Write()

		print("total signal evts = ", signal_hist.Integral())

		for bkg_hist in bkg_hists_list:
			proc_name = bkg_hist.GetName().split(var1)[0].rstrip("_")
			print(proc_name)
			bkg_hist.SetName(proc_name)
			bkg_hist.SetTitle(proc_name)
			bkg_hist.SetLineColor(ROOT.kBlack)
			bkg_hist.Write()
			print("total {} evts = {}".format(bkg_hist.GetName(), bkg_hist.Integral()) )

		#add an observation
		obs_hist = bkg_stack.GetStack().Last().Clone("data_obs")
		obs_hist.SetLineColor(ROOT.kBlue)
		obs_hist.SetLineWidth(2)
		obs_hist.SetName("data_obs")
		obs_hist.SetTitle("data_obs")
		obs_hist.Write()

		# data_hist.Write()

		print("Wrote root file:", fileoutpath)

		fileout.Close()

		



if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Plot distributions for FCC-hh events of type HH(2l+MET)")
	parser.add_argument('--input', '-i', metavar="INPUTDIR", dest="inDir", required=True, help="Path to the input directory")
	parser.add_argument('--outdir', '-o', metavar="OUTPUTDIR", dest="outDir", required=True, help="Output directory, if not specified subdir called Cutflows of working dir.")
	parser.add_argument('--signalCat', metavar="SIGNALCAT", dest="signalCat", required=True, help="Signal category of the analysis: bbZZllvv, or ..?")
	parser.add_argument('--extraCut', metavar="CUTNAME", dest="extraCut", help="Adding an extra cutname")

	
	args = parser.parse_args()

	if args.extraCut:
		extra_cut_name = args.extraCut
		extra_cut_string = bb2l_cats[args.extraCut]
	else:
		extra_cut_name = ""
		extra_cut_string = ""


	##direct compare bbWW signal and ttbar bkg
	if args.signalCat == "compare_bbWW_ttbar":
		plots = plot_list.compare_vars_bbWW_ttbar
		cut_levels = ["sel2_bJets", "sel8_HT2_ratio"]
		procs =["ttbar", "pwp8_pp_hh_lambda100_5f_hhbbww"]
		nevts_dict, sow_dict = getEvtsProcessedDict( args.inDir, all_processes)
		indir = os.path.join(args.inDir, "bbWW_emu_analysis")

		for cut_level in cut_levels:
			plot_shape_compare(plots, procs, cut_level, indir, args.outDir, nevts_dict, out_format = ".png")

		exit()

	##comparing shapes between bbWW and bbtautau
	if args.signalCat == "compare_bbWW_bbtautau":
		plots = plot_list.compare_vars_bbWW_bbtautau
		# cut_levels = ["sel2_bJets"] 
		procs =["pwp8_pp_hh_lambda100_5f_hhbbww","pwp8_pp_hh_lambda100_5f_hhbbtata"]
		nevts_dict, sow_dict = getEvtsProcessedDict( args.inDir, all_processes)



		plot_shape_compare(plots, procs, "", args.inDir, args.outDir, nevts_dict, out_format = ".png")

		exit()

	if args.signalCat == "compare_bbWW_bbtautau_ttbar":
		plots = plot_list.compare_vars_bbWW_bbtautau_ttbar
		# cut_levels = ["sel2_bJets"] 
		procs =["pwp8_pp_hh_lambda100_5f_hhbbww","pwp8_pp_hh_lambda100_5f_hhbbtata", "ttbar"]
		nevts_dict, sow_dict = getEvtsProcessedDict( args.inDir, all_processes)

		plot_shape_compare(plots, procs, "", args.inDir, args.outDir, nevts_dict, out_format = ".png")
		# plot_shape_compare(plots, procs, "sel9_mlb_150", args.inDir+"/bbWW_SF_analysis/", args.outDir, nevts_dict, out_format = ".png")
		plot_shape_compare(plots, procs, "sel9_mlb_150", args.inDir+"/bbWW_emu_analysis/", args.outDir, nevts_dict, out_format = ".png")

		exit()

	if args.signalCat == "compare_bbtautau":
		plots = plot_list.compare_vars_bbWW_bbtautau
		# cut_levels = ["sel2_bJets"] 
		procs ="pwp8_pp_hh_lambda100_5f_hhbbtata"
		nevts_dict, sow_dict = getEvtsProcessedDict( args.inDir, all_processes)

		list_of_cut_compares =[
			{
			"pre-sel.":"n_b_jets >1",
			"lep pT > 20 GeV":"pT_pair_lep1[0] > 20. && pT_pair_lep2[0] > 20.",
			},
			{
			"pre-sel.":"n_b_jets >1",
			"MET < 100 GeV":"MET[0] < 100.",
			"MET > 100 GeV":"MET[0] > 100.",
			},
			{
			"pre-sel.":"n_b_jets > 1",
			"x > 0.5":"x_lep1[0] > 0.5 && x_lep2[0] > 0.5",
			"x < 0.5":"x_lep1[0] < 0.5 && x_lep2[0] < 0.5",
			},
			{
			"pre-sel.":"n_b_jets > 1",
			"m_coll > 200.":"m_collinear[0] > 200.",
			"m_coll < 200.":"m_collinear[0] < 200.",
			}


		]

		for cuts_dict in list_of_cut_compares:
			plot_shape_compare_cuts(plots, procs, cuts_dict, args.inDir, args.outDir, nevts_dict, out_format = ".png")

		# plot_shape_compare(plots, procs, "", args.inDir, args.outDir, nevts_dict, out_format = ".png")

		exit()

	if args.signalCat == "compare_HH_ggH":
		plots = plot_list.compare_vars_HH_ggH
		procs = ["pwp8_pp_hh_lambda100_5f_hhbbww", "ggF_Higgs"]
		nevts_dict, sow_dict = getEvtsProcessedDict( args.inDir, all_processes)
		plot_shape_compare(plots, procs, "", args.inDir, args.outDir, nevts_dict, out_format = ".png")
		plot_shape_compare(plots, procs, "sel9_mlb_150", args.inDir+"/bbWW_emu_analysis/", args.outDir, nevts_dict, out_format = ".png")
		exit()

	if args.signalCat == "compareXValues":
		plots = plot_list.compare_x1
		procs = "pwp8_pp_hh_lambda100_5f_hhbbtata"
		nevts_dict, sow_dict = getEvtsProcessedDict( args.inDir, all_processes)
		plot_shape_compare_vars(plots, procs, "", args.inDir, args.outDir, nevts_dict, out_format = ".png")
		plots = plot_list.compare_x2
		plot_shape_compare_vars(plots, procs, "", args.inDir, args.outDir, nevts_dict, out_format = ".png")
		# plot_shape_compare(plots, procs, "sel9_mlb_150", args.inDir+"/bbWW_emu_analysis/", args.outDir, nevts_dict, out_format = ".png")
		exit()

	if args.signalCat == "compare_met_smearing":
		procs = "pwp8_pp_hh_lambda100_5f_hhbbww"
		nevts_dict, sow_dict = getEvtsProcessedDict( args.inDir.split("SmearedMET")[0], all_processes) #check in oparent dir..

		plots_list_list = [
			
			plot_list.compare_vars_met_smear,
			plot_list.compare_vars_met_res_smeared,
			plot_list.compare_vars_met_x_smear,
			plot_list.compare_vars_met_y_smear,
			plot_list.compare_vars_dPhiZMET_smeared,
			plot_list.compare_vars_HT2ratio_smeared,
			plot_list.compare_vars_mT2_smeared,
			# plot_list.compare_vars_input_check,
			plot_list.compare_vars_met_res_abs_smeared,
			


		]

		for plots in plots_list_list:
			plot_shape_compare_vars(plots, procs, "", args.inDir, args.outDir, nevts_dict, out_format = ".png")

		#plots of single variables
		single_vars_list = [
			plot_list.compare_vars_gaus_for_smear,
			plot_list.compare_vars_met_diff,
			plot_list.compare_vars_met_x_diff,
			plot_list.compare_vars_met_y_diff,
			plot_list.compare_vars_met_ratio,
			plot_list.compare_vars_met_x_ratio,
			plot_list.compare_vars_met_y_ratio,

		]

		for plots in single_vars_list:
			plot_shape_compare_vars(plots, procs, "", args.inDir, args.outDir, nevts_dict, out_format = ".png", addRatio=False)

		#2D plots:
		plot_2D(args.inDir, args.outDir, procs, "", "MET", "MET_recalc", out_format = ".png")


		
		
		
		# plot_shape_compare_vars(plots, procs, "", args.inDir, args.outDir, nevts_dict, out_format = ".png")
		# #ADDING MET X STILL
		# plots = plot_list.compare_vars_met_x_smear
		# plot_shape_compare_vars(plots, procs, "", args.inDir, args.outDir, nevts_dict, out_format = ".png")
		# #kin sel variables:
		# plots = plot_list.compare_vars_dPhiZMET_smeared
		# plot_shape_compare_vars(plots, procs, "", args.inDir, args.outDir, nevts_dict, out_format = ".png")
		# plots = plot_list.compare_vars_HT2ratio_smeared
		# plot_shape_compare_vars(plots, procs, "", args.inDir, args.outDir, nevts_dict, out_format = ".png")
		# plots = plot_list.compare_vars_mT2_smeared
		# plot_shape_compare_vars(plots, procs, "", args.inDir, args.outDir, nevts_dict, out_format = ".png")
		# plot_shape_compare(plots, procs, "sel9_mlb_150", args.inDir+"/bbWW_emu_analysis/", args.outDir, nevts_dict, out_format = ".png")
		exit()


	cut_levels = [] #kinsel only
	# cut_levels = ["sel2_bJets_medium"] 

	plots = plot_list.common_sel_vars

	if args.signalCat == "bbZZllvv":
		# processes = bb2l_DFOS_processes #use alle signals for bbZZllvv aimed analysis, significant bbtautau contribution here
		processes = bbzz_processes_new
		files_dir = os.path.join(args.inDir, "bbZZllvv_analysis")
		labels_dict = bbZZllvv_labels_dict
		cut_levels.append("sel9_dphiZMET_12") #kinematic selection for bbZZllvv

	elif args.signalCat == "bbZZllvv_old":
		# processes = bb2l_DFOS_processes #use alle signals for bbZZllvv aimed analysis, significant bbtautau contribution here
		processes = bbzz_processes_new
		files_dir = os.path.join(args.inDir, "bbZZllvv_oldSel_analysis")
		labels_dict = bbZZllvv_labels_dict
		cut_levels = []
		cut_levels.append("sel3_mll") #old preselection for bbZZllvv
		cut_levels.append("sel9_dPhiHH") #old kinematic selection for bbZZllvv

		#OVERWRITING PLOTS
		plots = plot_list.bbZZllvv_old_plots

	elif args.signalCat == "bbtautau_emu":
		processes = bbtautau_processes_new
		files_dir = os.path.join(args.inDir, "bbtautau_emu_analysis")
		labels_dict = bbtautau_emu_labels_dict
		cut_levels.append("sel9_dphiZMET_12") #kinematic selection for bbtautau

	elif args.signalCat == "bbtautau_old":
		processes = bbtautau_processes_new
		files_dir = os.path.join(args.inDir, "bbtautau_oldSel_analysis")

		if "SF" in args.inDir:
			labels_dict = bbtautau_SF_labels_dict
		else:
			labels_dict = bbtautau_emu_labels_dict
		# cut_levels.append("sel10_HT2_ratio") #old kinematic selection for bbtautau
		plots = plot_list.bbtautau_old_plots

	elif args.signalCat == "bbWW_emu":
		processes = bbWW_processes_new
		
		if "SF" in args.inDir:
			labels_dict = bbWW_SF_labels_dict
			files_dir = os.path.join(args.inDir, "bbWW_SF_analysis")
			
		else:
			labels_dict = bbWW_emu_labels_dict
			files_dir = os.path.join(args.inDir, "bbWW_emu_analysis")
		# cut_levels.append("sel9_mlb_150") #kinematic selection for bbWW

		# cut_levels = ["sel8_HT2_ratio"] #TEMP OVERWRITE

	elif args.signalCat == "bb2l_DFOS":
		processes = bb2l_DFOS_processes
		# if args.kappaLambda: #TO DO: need kapp lambda signals for bbtautau
		# 	processes = bbWW_processes_kl
		files_dir = os.path.join(args.inDir, "noZ") #using the selection from bbWW(emu), not optimum for bbtautau but as a start
		# cut_level = "sel9_mlb_150"
		labels_dict = bbWW_emu_labels_dict
		cut_levels.append("sel9_mlb_150") #kinematic selection for bbWW
		cut_levels.append("sel8_HT2_ratio")

	elif args.signalCat == "bb2l_SFOS_noZ":
		processes = bb2l_DFOS_processes
		# if args.kappaLambda: #TO DO: need kapp lambda signals for bbtautau
		# 	processes = bbWW_processes_kl
		files_dir = os.path.join(args.inDir, "bbWW_SF_analysis") #using the selection from bbWW(emu), not optimum for bbtautau but as a start
		# cut_level = "sel9_mlb_150"
		labels_dict = bbWW_emu_labels_dict
		cut_levels.append("sel9_mlb_150") #kinematic selection for bbWW
		# cut_levels.append("sel8_HT2_ratio")  

	#bbZZ aimed channel but with all signals
	elif args.signalCat == "bb2l_SFOS_Zpeak":
		processes = bb2l_DFOS_processes #use alle signals for bbZZllvv aimed analysis, significant bbtautau contribution here
		files_dir = os.path.join(args.inDir, "bbZZllvv_analysis")
		labels_dict = bbZZllvv_labels_dict
		cut_levels.append("sel9_dphiZMET_12") #kinematic selection for bbZZllvv

	#for BDT analysis: comparing kinematic vars in the different m_ll regimes
	elif args.signalCat == "BDT_compare_mll_regions":

		#overwrite which plots to make
		plots = plot_list.bbZZ_vs_bbWW_BDT_compare_vars
		

		#first make the plots for bbZZ = on-shell mll 
		processes = bbzz_processes_new #only use bbZZ signal for now  
		nevts_dict, sow_dict = getEvtsProcessedDict( args.inDir, processes)
		files_dir = os.path.join(args.inDir, "bbZZllvv_analysis")
		labels_dict = bbZZllvv_labels_dict
		# cut_levels.append("sel2_bJets") #only pre-selection applied
		extra_cut_name = "bbZZ_region_76_mll_106" 
		extra_cut_string = "m_ll[0] > 76 && m_ll[0] < 106"
		cut_level = "sel2_bJets"
		# for plot in plots: 
		# 	makePlot(plot, files_dir, processes, cut_level, nevts_dict, args.outDir, labels_dict, plots, extra_cut=(extra_cut_name, extra_cut_string))

		#shape comparison of ttbar vs all other bkgs
		procs = ["ttbar", "other_bkgs", "pwp8_pp_hh_lambda100_5f_hhbbzz_zleptonic"]
		# nevts_dict = getEvtsProcessedDict( args.inDir, all_processes)
		# plot_shape_compare(plots, procs, cut_level, files_dir, args.outDir, nevts_dict, out_format = ".png", extra_cut=(extra_cut_name, extra_cut_string))

		#shape comparison of the different bkgs, splitting of single H 
		procs = ["ttbar", "Single_Higgs", "rest"]
		plot_shape_compare(plots, procs, cut_level, files_dir, args.outDir, nevts_dict, out_format = "_bkgs_only.png", extra_cut=(extra_cut_name, extra_cut_string))

		#now the same but for the bbWW signal/mll region:
		processes = bbWW_processes_new #only use bbZZ signal for now  
		nevts_dict, sow_dict = getEvtsProcessedDict( args.inDir, processes)
		files_dir = os.path.join(args.inDir, "bbWW_SF_analysis")
		labels_dict = bbWW_SF_labels_dict
		# cut_levels.append("sel2_bJets") #only pre-selection applied
		extra_cut_name = "bbWW_region_10_mll_80" 
		extra_cut_string = "m_ll[0] > 10 && m_ll[0] < 80"
		cut_level = "sel2_bJets"
		for plot in plots: 
			makePlot(plot, files_dir, processes, cut_level, nevts_dict, args.outDir, labels_dict, plots, extra_cut=(extra_cut_name, extra_cut_string))

		#shape comparison of ttbar vs all other bkgs
		procs = ["ttbar", "other_bkgs", "pwp8_pp_hh_lambda100_5f_hhbbww"]
		# nevts_dict = getEvtsProcessedDict( args.inDir, all_processes)
		plot_shape_compare(plots, procs, cut_level, files_dir, args.outDir, nevts_dict, out_format = ".png", extra_cut=(extra_cut_name, extra_cut_string))

		#shape comparison of the different bkgs, splitting of single H 
		procs = ["ttbar", "Single_Higgs", "rest"]
		plot_shape_compare(plots, procs, cut_level, files_dir, args.outDir, nevts_dict, out_format = "_bkgs_only.png", extra_cut=(extra_cut_name, extra_cut_string))

		exit()


	#first make a dictionary for how many evts were processed per sample:
	nevts_dict, sow_dict = getEvtsProcessedDict( args.inDir, processes)

	#make WS inputs
	# makePlot("m_pseudo_HH_selBinning", default_in_dir, processes, "sel10_mlb_150", nevts_dict, out_dir, store_root_file=True, addOverlow=True)
	# # makePlot("m_pseudo_HH_selBinning", default_in_dir, processes, "sel9_mlb_100", nevts_dict, out_dir, store_root_file=True, addOverlow=True)
	# # # # makePlot("m_pseudo_HH_smeared_selBinning", default_in_dir, processes, "sel8_HT2_ratio", nevts_dict, out_dir, store_root_file=True)
	# exit()

	# shape comparisons
	# shape_compare_proc = ["ttbar", "signal"]
	# plot_shape_compare("MET", shape_compare_proc, "sel2_bJets", default_in_dir, out_dir, nevts_dict)
	# exit()

	for cut_level in cut_levels:
		for plot in plots:
			# plot_shape_compare(plot, shape_compare_proc, cut_level, default_in_dir, out_dir, nevts_dict)
			
			# makePlot(plot, files_dir, processes, cut_level, nevts_dict, args.outDir, labels_dict, plots, extra_cut=(extra_cut_name, extra_cut_string))
			makePlot(plot, files_dir, processes, cut_level, sow_dict, args.outDir, labels_dict, plots, weighted=True, extra_cut=(extra_cut_name, extra_cut_string))
			# makePlot(plot, default_in_dir, processes, cut_level, nevts_dict, out_dir, fix_ratio_range=(0., 0.005))
			# makePlot(plot, default_in_dir, processes, cut_level, nevts_dict, out_dir)


# commands:

# python draw_plots.py -i /eos/user/b/bistapf/FCChh_EvtGen/bb2lMET_ntuples/SFOS/ -o ./Plots_bb2lMET_DFOS/ --signalCat bb2l_DFOS