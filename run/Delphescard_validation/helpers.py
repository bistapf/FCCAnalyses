#common functions for all the checks

import ROOT
import os

def get_rdf(input_filepath):

	if input_filepath.endswith(".root"):
		rdf = ROOT.RDataFrame("events", input_filepath)
	else:
		rdf = ROOT.RDataFrame("events", input_filepath+"chunk*")

	if not rdf:
		print("Empty file for:", input_filepath, " Exiting.")
		return

	return rdf

def plot_single_hist(hist, filename, out_dir_base, xaxis_label, do_gauss_fit=False, colour_code=38, file_format="png"):

	canvas = ROOT.TCanvas("canvas", "canvas", 800, 800) 
	canvas.cd()
	histfile_name = "{}.{}".format(filename, file_format)
	histfile_path = os.path.join(out_dir_base, histfile_name)

	#fit the histogram with a gaus:
	if do_gauss_fit:
		gauss = ROOT.TF1("gauss","gaus", -1., 1.)
		hist.Fit(gauss)
		fit_result= hist.GetFunction("gauss")

	
	hist.SetLineWidth(2)
	hist.SetLineColor(colour_code)
	hist.GetYaxis().SetTitle("Events")
	hist.GetXaxis().SetTitle(xaxis_label)

	if do_gauss_fit:
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
			hist.SetTitle("#sigma E/E = {:.4f} +/- {:.4f}".format(gaus_width, gaus_width_error))

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

	if do_gauss_fit:
		return gaus_pars

def plot_list_of_hists(list_of_hists, histbasename, out_dir_base, xaxis_label, yaxis_label="Events", file_format="png"):
	canvas = ROOT.TCanvas("canvas", "canvas", 800, 800) 
	canvas.cd()
	canvas.SetLeftMargin(0.15)
	histfile_name = "{}.{}".format(histbasename, file_format)
	histfile_path = os.path.join(out_dir_base, histfile_name)

	hist_stack = ROOT.THStack("hist_stack", "hist_stack")

	leg = ROOT.TLegend(0.55, 0.6, 0.9, 0.9)

	for i_hist, hist in enumerate(list_of_hists):
		print("Plotting hist", i_hist, "with name", hist.GetTitle() )
		hist.SetLineWidth(2)
		hist.SetLineColor(38+i_hist*4)

		hist.GetYaxis().SetTitle(yaxis_label)
		hist.GetXaxis().SetTitle(xaxis_label)
		# hist.Draw("HISTE SAME")
		leg.AddEntry(hist, hist.GetTitle(), "l")
		hist_stack.Add(hist)


	hist_stack.Draw("HISTE NOSTACK")

	hist_stack.GetYaxis().SetTitle(yaxis_label)
	hist_stack.GetXaxis().SetTitle(xaxis_label)
	canvas.RedrawAxis()

	leg.SetFillStyle( 0 )
	leg.SetBorderSize( 0 )
	leg.SetMargin( 0.1)
	leg.SetTextFont( 43 )
	leg.SetTextSize( 20 )
	leg.SetColumnSeparation(-0.05)
	leg.Draw()

	canvas.SaveAs(histfile_path)
