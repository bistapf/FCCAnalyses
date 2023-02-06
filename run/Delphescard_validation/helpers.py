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