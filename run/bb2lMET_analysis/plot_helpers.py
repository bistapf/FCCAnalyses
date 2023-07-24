import ROOT
import os
from collections import namedtuple
from array import array
import json

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)

def load_norm_json(json_path):
	if not os.path.isfile(json_path):
		raise Exception("Error in load_norm_json(): Json file not found at", json_path)
	file = open(json_path)
	data = json.load(file)
	file.close()
	return data

def get_nevts_sow(inputfilepath):
	infile = ROOT.TFile(inputfilepath, "READ")
	both_found = True
	nevts = 0
	sow = 0

	if infile.eventsProcessed.GetVal():
		nevts = infile.eventsProcessed.GetVal()
	else:
		both_found = False
		print("Error in get_nevts_sow - could not find eventsProcessed parameter in input file "+inputfilepath)

	if infile.SumOfWeights.GetVal():
		sow = sow = infile.SumOfWeights.GetVal()
	else:
		both_found = False
		print("Error in get_nevts_sow - could not find SumOfWeights parameter in input file "+inputfilepath)

	if not both_found:
		raise Exception("ERROR could not read normalisation info. See above. Exiting.")

	return nevts, sow
	

#compare two histograms
def plot_hist_compare(hist_name, plot_specs, process1, process2, out_dir, norm_info="", yaxis_label="Events", 
						do_ratio=True, file_format="png", do_logy=False, tree_name="events", weight_name="", do_norm_unit=False ):

	rdf1 = ROOT.RDataFrame(tree_name, process1.filepath)
	rdf2 = ROOT.RDataFrame(tree_name, process2.filepath)


	# hist_model = ROOT.RDF.TH1DModel(hist_name, hist_name, plot_specs.nbins, plot_specs.xmin, plot_specs.xmax)
	#going to need a TH1Model to fill:
	has_variable_binning = False
	if not isinstance(plot_specs.nbins, int):
		has_variable_binning = True
		hist_binEdges = array("d", plot_specs.nbins)
		hist_nBins = len(plot_specs.nbins)-1
		#init the histogram with variable bin widths:
		hist_model = ROOT.RDF.TH1DModel(hist_name, hist_name, hist_nBins, hist_binEdges)


	else:
		hist_model = ROOT.RDF.TH1DModel(hist_name, hist_name, plot_specs.nbins, plot_specs.xmin, plot_specs.xmax)

	

	#get the histograms:
	if weight_name:
		hist1 = rdf1.Histo1D(hist_model, plot_specs.name, weight_name).GetValue()  
		hist2 = rdf2.Histo1D(hist_model, plot_specs.name, weight_name).GetValue()  
	else:
		hist1 = rdf1.Histo1D(hist_model, plot_specs.name).GetValue()  
		hist2 = rdf2.Histo1D(hist_model, plot_specs.name).GetValue()  


	hist1.SetTitle(process1.label)
	hist1.SetLineWidth(2)
	hist1.SetLineColor(process1.colour)
	hist1.GetYaxis().SetTitle(yaxis_label)
	hist1.GetXaxis().SetTitle(plot_specs.label)
	hist1.Sumw2()

	
	hist2.SetTitle(process2.label)
	hist2.SetLineWidth(2)
	hist2.SetLineColor(process2.colour)
	hist2.GetYaxis().SetTitle(yaxis_label)
	hist2.GetXaxis().SetTitle(plot_specs.label)
	hist2.Sumw2()

	if norm_info:
		sow1 = rdf1.Histo1D("weight", "weight").Integral() #TO CHECK THAT THIS IS CORRECT
		# print(sow1)
		sow2 = rdf2.Histo1D("weight", "weight").Integral()
		# print(sow2)
		hist_name+="_normed"
		hist1.Scale(norm_info.lumi*norm_info.kfactor*norm_info.xsection/sow1)
		hist2.Scale(norm_info.lumi*norm_info.kfactor*norm_info.xsection/sow2)

	elif do_norm_unit:
		hist1.Scale(1./hist1.Integral())
		hist2.Scale(1./hist2.Integral())
		hist_name+="_unitNormed"

	#set output file name
	if do_ratio:
		hist_ratio = hist1.Clone()
		hist_ratio.Divide( hist2 )
		hist1.GetXaxis().SetLabelSize(0)
		hist1.GetXaxis().SetTitle("")
		hist2.GetXaxis().SetLabelSize(0)
		hist2.GetXaxis().SetTitle("")
		hist_name+="_ratio"
		
	if do_logy:
		hist_name+="_logY"


	histfile_name = "{}.{}".format(hist_name, file_format)
	histfile_path = os.path.join(out_dir, histfile_name)

	#setup canvas
	canvas = ROOT.TCanvas("canvas", "canvas", 800, 800) 
	canvas.SetLogy(do_logy)
	canvas.cd()

	canvas.SetLeftMargin(0.16)

	if do_ratio:
		pad_up = ROOT.TPad("pad_up", "pad_up", 0., 0., 1., 1.)
		pad_up.SetFillStyle(0)
		pad_up.SetBottomMargin(0.32)
		pad_up.SetTopMargin(0.03)
		pad_up.SetLeftMargin(0.13)
		pad_up.SetRightMargin(0.05)
		pad_up.SetLogy(do_logy)
		pad_up.Draw()

		pad_low = ROOT.TPad("pad_low", "pad_low", 0., 0., 1., 1.);
		pad_low.SetFillStyle(0)
		pad_low.SetBottomMargin(0.12)
		pad_low.SetTopMargin(0.72)
		pad_low.SetLeftMargin(0.13)
		pad_low.SetRightMargin(0.05)
		pad_low.SetGrid()
		pad_low.Draw()

		pad_up.cd()

	#draw histograms and legend
	hist1.Draw("HIST SAME")
	hist2.Draw("HIST SAME")

	leg = ROOT.TLegend(0.77, 0.77, 0.95, 0.95)
	leg.SetFillStyle( 0 )
	leg.SetBorderSize( 0 )
	leg.SetMargin( 0.1)
	leg.SetTextFont( 43 )
	leg.SetTextSize( 20 )
	leg.SetColumnSeparation(-0.05)
	if norm_info:
		leg.SetHeader("{} fb^{{-1}}".format(norm_info.lumi))
	leg.AddEntry(hist1, hist1.GetTitle(), "l")
	leg.AddEntry(hist2, hist2.GetTitle(), "l")
	leg.Draw()

	if do_ratio:
		pad_low.cd()
		hist_ratio.GetYaxis().SetTitle("Ratio")
		hist_ratio.GetYaxis().SetTitleOffset(1.95)
		hist_ratio.GetYaxis().SetNdivisions(6)

		pad_low.cd()
		pad_low.Update()
		hist_ratio.Draw("E0P")
		pad_low.RedrawAxis()

		canvas.RedrawAxis()
		canvas.Modified()
		canvas.Update()	


	canvas.SaveAs(histfile_path)

#script to compare the same distribution with and without event weights
def plot_weight_compare(hist_name, plot_specs, process, out_dir, norm_info="", yaxis_label="Events", 
						do_ratio=True, file_format="png", do_logy=False, tree_name="events", weight_name="weight"):
	
	print(process.filepath)
	nevts, sow = get_nevts_sow(process.filepath)
	print("nevts", nevts)
	print("sow", sow)

	rdf = ROOT.RDataFrame(tree_name, process.filepath)


	# hist_model = ROOT.RDF.TH1DModel(hist_name, hist_name, plot_specs.nbins, plot_specs.xmin, plot_specs.xmax)
	#going to need a TH1Model to fill:
	has_variable_binning = False
	if not isinstance(plot_specs.nbins, int):
		has_variable_binning = True
		hist_binEdges = array("d", plot_specs.nbins)
		hist_nBins = len(plot_specs.nbins)-1
		#init the histogram with variable bin widths:
		hist_model = ROOT.RDF.TH1DModel(hist_name, hist_name, hist_nBins, hist_binEdges)


	else:
		hist_model = ROOT.RDF.TH1DModel(hist_name, hist_name, plot_specs.nbins, plot_specs.xmin, plot_specs.xmax)

	

	#get the histograms:
	hist_no_weight = rdf.Histo1D(hist_model, plot_specs.name).GetValue()  
	hist_weighted = rdf.Histo1D(hist_model, plot_specs.name, weight_name).GetValue()  


	hist_no_weight.SetTitle("Unweighted")
	hist_no_weight.SetLineWidth(2)
	hist_no_weight.SetLineColor(36)
	hist_no_weight.GetYaxis().SetTitle(yaxis_label)
	hist_no_weight.GetXaxis().SetTitle(plot_specs.label)
	hist_no_weight.Sumw2()

	
	hist_weighted.SetTitle("Weighted")
	hist_weighted.SetLineWidth(2)
	hist_weighted.SetLineColor(46)
	hist_weighted.GetYaxis().SetTitle(yaxis_label)
	hist_weighted.GetXaxis().SetTitle(plot_specs.label)
	hist_weighted.Sumw2()

	if norm_info:
		hist_no_weight.Scale(norm_info.lumi*norm_info.kfactor*norm_info.xsection/nevts)
		hist_weighted.Scale(norm_info.lumi*norm_info.kfactor*norm_info.xsection/sow)

	#set output file name
	if do_ratio:
		hist_ratio = hist_no_weight.Clone()
		hist_ratio.Divide( hist_weighted )
		hist_no_weight.GetXaxis().SetLabelSize(0)
		hist_no_weight.GetXaxis().SetTitle("")
		hist_weighted.GetXaxis().SetLabelSize(0)
		hist_weighted.GetXaxis().SetTitle("")
		hist_name+="_ratio"
		
	if do_logy:
		hist_name+="_logY"


	histfile_name = "{}.{}".format(hist_name, file_format)
	histfile_path = os.path.join(out_dir, histfile_name)

	#setup canvas
	canvas = ROOT.TCanvas("canvas", "canvas", 800, 800) 
	canvas.SetLogy(do_logy)
	canvas.cd()

	canvas.SetLeftMargin(0.16)

	if do_ratio:
		pad_up = ROOT.TPad("pad_up", "pad_up", 0., 0., 1., 1.)
		pad_up.SetFillStyle(0)
		pad_up.SetBottomMargin(0.32)
		pad_up.SetTopMargin(0.03)
		pad_up.SetLeftMargin(0.13)
		pad_up.SetRightMargin(0.05)
		pad_up.SetLogy(do_logy)
		pad_up.Draw()

		pad_low = ROOT.TPad("pad_low", "pad_low", 0., 0., 1., 1.);
		pad_low.SetFillStyle(0)
		pad_low.SetBottomMargin(0.12)
		pad_low.SetTopMargin(0.72)
		pad_low.SetLeftMargin(0.13)
		pad_low.SetRightMargin(0.05)
		pad_low.SetGrid()
		pad_low.Draw()

		pad_up.cd()

	#draw histograms and legend
	hist_no_weight.Draw("HIST SAME")
	hist_weighted.Draw("HIST SAME")

	leg = ROOT.TLegend(0.65, 0.77, 0.95, 0.95)
	leg.SetFillStyle( 0 )
	leg.SetBorderSize( 0 )
	leg.SetMargin( 0.1)
	leg.SetTextFont( 43 )
	leg.SetTextSize( 20 )
	leg.SetColumnSeparation(-0.05)
	if norm_info:
		leg.SetHeader("{} fb^{{-1}}".format(norm_info.lumi))
	leg_text_no_weight = "{}, {:.1f} evts".format(hist_no_weight.GetTitle(), hist_no_weight.Integral())
	leg_text_weighted = "{}, {:.1f} evts".format(hist_weighted.GetTitle(), hist_weighted.Integral())
	leg.AddEntry(hist_no_weight, leg_text_no_weight, "l")
	leg.AddEntry(hist_weighted, leg_text_weighted, "l")
	leg.Draw()

	print("Unweighted", hist_no_weight.Integral())
	print("Weighted", hist_weighted.Integral())

	if do_ratio:
		pad_low.cd()
		hist_ratio.GetYaxis().SetTitle("Ratio")
		hist_ratio.GetYaxis().SetTitleOffset(1.95)
		hist_ratio.GetYaxis().SetNdivisions(6)

		pad_low.cd()
		pad_low.Update()
		hist_ratio.Draw("E0P")
		pad_low.RedrawAxis()

		canvas.RedrawAxis()
		canvas.Modified()
		canvas.Update()	


	canvas.SaveAs(histfile_path)
