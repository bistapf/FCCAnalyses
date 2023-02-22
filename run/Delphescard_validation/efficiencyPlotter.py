import ROOT
import os 
from array import array

import helpers

class EfficiencyPlotter:

	def __init__(self, input_path, output_dir, object_name):
		print("Initializing EfficiencyPlotter for", object_name, "with input", input_path, "and output", output_dir)

		self.object_name = object_name

		if not os.path.exists(output_dir):
			os.mkdir(output_dir)

		self.output_dir = output_dir

		self.rdf = self.get_rdf(input_path)

		if not self.rdf:
			raiseException("Error in initializing EfficiencyPlotter - no rdf created.")

		#set the pdg id

		if self.object_name == "electron" or self.object_name == "Electron":
			self.pdg_id = 11 
		elif self.object_name == "muon" or self.object_name == "Muon":
			self.pdg_id = 13
		else:
			self.pdg_id = None

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

		print("Evts in rdf before filter:", self.rdf.Count().GetValue())

		filtered_rdf = self.rdf.Filter(cutstring)
		print("Filtering rdf with:", cutstring)

		self.rdf = filtered_rdf

		print("Evts in rdf after filter:", self.rdf.Count().GetValue())

	def set_binning(self, primary_var_name, primary_var_bin_edges, primary_var_label, secondary_var_name, secondary_var_bin_edges, secondary_var_label):

		self.var1 = primary_var_name
		self.var1_edges = primary_var_bin_edges
		self.var1_label = primary_var_label
		self.var2 = secondary_var_name
		self.var2_edges = secondary_var_bin_edges
		self.var2_label = secondary_var_label

	def set_use_abs_eta(self, use_abs):
		self.use_abs_eta = use_abs

	def build_cutstring_bin(self, var_name, var_edges, object_index):

		if "eta" in var_name and self.use_abs_eta:
			cutstring = "abs({}[{}]) > {:.2f} && abs({}[{}]) <= {:.2f}".format(var_name, object_index, var_edges[0], var_name, object_index, var_edges[1])
		else:
			cutstring = "{}[{}] > {:.2f} && {}[{}] <= {:.2f}".format(var_name, object_index, var_edges[0], var_name, object_index, var_edges[1])

		return cutstring

	def filter_by_pdgID(self, pdg_var_name, number_of_objects):
		#select also the lepton flavour, if requested
		print("Filtering for with PDG id: ", self.object_name)
		if self.pdg_id:
			cut_string_flav = ""
			for obj_i in range(number_of_objects):
				cut_string_flav += "abs({}[{}]) == {}".format(pdg_var_name, obj_i, self.pdg_id)
			filtered_rdf = self.rdf.Filter(cut_string_flav)
			self.rdf = filtered_rdf
		else:
			raiseException("Error in filter_by_pdgID - PDG ID not given")


	def merge_cutstrings(self, cutstring1, cutstring2):
		return "{} && {}".format(cutstring1, cutstring2)

	#make sure the rdf is filtered for the correct amount of truth objects before running this! i.e. run eff_plotter.filter_input_rdf("truth_var_name == number_of_objects") before calling this
	# in case of running electrons/muons also filter by pdgID first: filter_by_pdgID("pdgID_truth_leps_from_HWW", 1)
	def plot_efficiencies(self, hist_base_name, reco_var_name, eff_label, number_of_objects):

		if not self.var1 or not self.var1_edges or not self.var2 or not self.var2_edges:
			raiseException("Error in plotting efficiencies - no binning info provided, please call set_binning(primary_var_name, primary_var_bin_edges, secondary_var_name, secondary_var_bin_edges) before running this.") 

		list_of_hists_vs_var2 = []
		hist_base_name = "{}_{}".format(self.object_name, hist_base_name)

		#loop over bins of primary var
		for var1_edge in range(len(self.var1_edges)-1):
			#plotting efficiency vs secondary_var in bins of primary var
			hist_binEdges = array("d", self.var2_edges)
			hist_nBins = len(self.var2_edges)-1
			hist_vs_var2_name = "{}_var1_bin_{}".format(hist_base_name, var1_edge)
			hist_vs_var2 = ROOT.TH1D(hist_vs_var2_name, hist_vs_var2_name, hist_nBins, hist_binEdges)
			hist_vs_var2_title = "{:.2f} < {} < {:.2f} ".format(self.var1_edges[var1_edge], self.var1_label, self.var1_edges[var1_edge+1])
			hist_vs_var2.SetTitle(hist_vs_var2_title)

			#now loop over var2 and get eff in each bin:
			for var2_edge in range(len(self.var2_edges)-1):	
				cutstring_bin = ""
				for object_i in range(number_of_objects):
					cutstring_var1 = self.build_cutstring_bin(self.var1, (self.var1_edges[var1_edge], self.var1_edges[var1_edge+1]), object_i)
					cutstring_var2 = self.build_cutstring_bin(self.var2, (self.var2_edges[var2_edge], self.var2_edges[var2_edge+1]), object_i)
					cutstring_bin_obj = self.merge_cutstrings(cutstring_var1, cutstring_var2)
					if cutstring_bin:
						cutstring_bin += " && "
					cutstring_bin += cutstring_bin_obj
				
				print("Calculating efficiency for bin:", cutstring_bin)

				
				rdf_bin = self.rdf.Filter(cutstring_bin)
				n_evts_bin_total = rdf_bin.Count().GetValue()

				#check how often the reco object(s) also there
				cutstring_recomatch = "{} == {}".format(reco_var_name, number_of_objects)
				n_evts_bin_recomatched = rdf_bin.Filter(cutstring_recomatch).Count().GetValue()

				#calculate eff and fill into hist
				if n_evts_bin_total:
					eff_bin = n_evts_bin_recomatched/n_evts_bin_total*100.
				else:
					eff_bin = 0.

				print("Eff in bin is:", eff_bin)	
				hist_vs_var2.SetBinContent(var2_edge+1, eff_bin)

			helpers.plot_single_hist(hist_vs_var2, hist_vs_var2_name, self.output_dir, self.var2_label, eff_label, do_gauss_fit=False, colour_code=38, file_format="png")
			list_of_hists_vs_var2.append(hist_vs_var2)

		helpers.plot_list_of_hists(list_of_hists_vs_var2, hist_base_name, self.output_dir, self.var2_label, eff_label, file_format="png", draw_error=False, fixed_y_range=(0., 100.))
				