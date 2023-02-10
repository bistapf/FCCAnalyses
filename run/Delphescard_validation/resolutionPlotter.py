import ROOT
import os 
from array import array

import helpers


class ResolutionPlotter:
	"""Generic class to make plots of various resolutions, in bins of other variables"""

	def __init__(self, input_path, output_dir, object_name):
		print("Initializing ResolutionPlotter for", object_name, "with input", input_path, "and output", output_dir)

		self.object_name = object_name

		if not os.path.exists(output_dir):
			os.mkdir(output_dir)

		self.output_dir = output_dir

		self.rdf = self.get_rdf(input_path)

		if not self.rdf:
			raiseException("Error in initializing ResolutionPlotter - no rdf created.")

		#setup for the resolution histograms:
		self.res_model_nbins = 40
		self.res_model_xmin = -0.05
		self.res_model_xmax = 0.05

	# Open the requested file(s) into the rdf
	def get_rdf(self, input_path):

		if input_path.endswith(".root"):
			rdf = ROOT.RDataFrame("events", input_path)
		else:
			rdf = ROOT.RDataFrame("events", input_path+"chunk*")

		if not rdf:
			print("Empty file for:", input_path, " Exiting.")
			return

		return rdf

	#apply some cut to the rdf before calculating resolutions - overwrites the original
	def filter_input_rdf(self, cutstring):

		filtered_rdf = self.rdf.Filter(cutstring)
		print("Filtering rdf with:", cutstring)

		self.rdf = filtered_rdf

	def set_binning(self, primary_var_name, primary_var_bin_edges, primary_var_label, secondary_var_name, secondary_var_bin_edges, secondary_var_label):

		self.var1 = primary_var_name
		self.var1_edges = primary_var_bin_edges
		self.var1_label = primary_var_label
		self.var2 = secondary_var_name
		self.var2_edges = secondary_var_bin_edges
		self.var2_label = secondary_var_label

	def build_cutstring_bin(self, var_name, var_edges, object_index):

		if "eta" in var_name:
			cutstring = "abs({}[{}]) > {:.2f} && abs({}[{}]) <= {:.2f}".format(var_name, object_index, var_edges[0], var_name, object_index, var_edges[1])
		else:
			cutstring = "{}[{}] > {:.2f} && {}[{}] <= {:.2f}".format(var_name, object_index, var_edges[0], var_name, object_index, var_edges[1])

		return cutstring

	def merge_cutstrings(self, cutstring1, cutstring2):
		return "{} && {}".format(cutstring1, cutstring2)

	def plot_resolution_histograms(self, hist_base_name, reco_var_name, truth_var_name, res_label, number_of_objects):

		if not self.var1 or not self.var1_edges or not self.var2 or not self.var2_edges:
			raiseException("Error in plotting resolution histograms - no binning info provided, please call set_binning(primary_var_name, primary_var_bin_edges, secondary_var_name, secondary_var_bin_edges) before running this.") 

		list_of_hists_vs_var2 = []
		hist_base_name = "{}_{}".format(self.object_name, hist_base_name)

		#loop over the primary var and then make histograms w.r.t secondary var:
		for var1_edge in range(len(self.var1_edges)-1):
			#histogram vs var2
			hist_binEdges = array("d", self.var2_edges)
			hist_nBins = len(self.var2_edges)-1
			hist_vs_var2_name = "{}_var1_bin_{}".format(hist_base_name, var1_edge)
			hist_vs_var2 = ROOT.TH1D(hist_vs_var2_name, hist_vs_var2_name, hist_nBins, hist_binEdges)
			hist_vs_var2_title = "{:.2f} < {} < {:.2f} ".format(self.var1_edges[var1_edge], self.var1_label, self.var1_edges[var1_edge+1])
			hist_vs_var2.SetTitle(hist_vs_var2_title)

			for var2_edge in range(len(self.var2_edges)-1):
				res_hist_bin = ROOT.TH1D("res_hist_bin", "res_hist_bin", 40, -0.05, 0.05)

				# make sure we loop over all the objects per event that we calculate the resolution for, e.g. in bbZZ(4l) we take the res from all 4 leps
				for object_i in range(number_of_objects):

					model = ROOT.RDF.TH1DModel("resolution_model_hist", "resolution_model_hist", self.res_model_nbins, self.res_model_xmin, self.res_model_xmax)

					cutstring_var1 = self.build_cutstring_bin(self.var1, (self.var1_edges[var1_edge], self.var1_edges[var1_edge+1]), object_i)
					cutstring_var2 = self.build_cutstring_bin(self.var2, (self.var2_edges[var2_edge], self.var2_edges[var2_edge+1]), object_i)
					cutstring_bin = self.merge_cutstrings(cutstring_var1, cutstring_var2)
					print("Calculating for bin:", cutstring_bin)
				
					rdf_bin = self.rdf.Filter(cutstring_bin)
					# print("Number of events in bin:", rdf_bin.Count().GetValue())

					#now define the relative resolution ! of (reco-truth)/truth:you dont 
					rel_res_def_string = "({}[{}] - {}[{}])/{}[{}]".format(reco_var_name, object_i, truth_var_name, object_i, truth_var_name, object_i)
					rdf_resolution = rdf_bin.Define("resolution", rel_res_def_string)
					tmp_hist = rdf_resolution.Histo1D(model, "resolution").GetValue()   
					res_hist_bin.Add(tmp_hist)

				histfilename = "{}_{}_x_{}".format(hist_base_name, var1_edge, var2_edge)  
				gaus_pars = helpers.plot_single_hist(res_hist_bin, histfilename, self.output_dir, "#sigma(E)/E", "Events", do_gauss_fit=True, colour_code=38, file_format="png")

				if gaus_pars:
					hist_vs_var2.SetBinContent(var2_edge+1, gaus_pars[2])
					hist_vs_var2.SetBinError(var2_edge+1, gaus_pars[3])

			helpers.plot_single_hist(hist_vs_var2, hist_vs_var2_name, self.output_dir, self.var2_label, res_label, do_gauss_fit=False, colour_code=38, file_format="png")
			list_of_hists_vs_var2.append(hist_vs_var2)

		helpers.plot_list_of_hists(list_of_hists_vs_var2, hist_base_name, self.output_dir, self.var2_label, res_label, file_format="png")


	# def get_resolution_in_bin(self, reco_var_name, truth_var_name,  number_of_objects):

	# 	model = ROOT.RDF.TH1DModel("resolution_model_hist", "resolution_model_hist", self.res_model_nbins, self.res_model_xmin, self.res_model_xmax)