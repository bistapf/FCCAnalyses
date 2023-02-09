import ROOT
import os 

class ResolutionPlotter:
	"""Generic class to make plots of various resolutions, in bins of other variables"""

	def __init__(self, input_path, output_dir, object_name):
		print("Initializing ResolutionPlotter for", object_name, "with input", input_path, "and output", output_dir)

		self.object_name = object_name

		self.rdf = self.get_rdf(input_path)

		if not self.rdf:
			raiseException("Error in initializing ResolutionPlotter - no rdf created.")

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


	# def get_resolution_in_bin(input_rdf, )