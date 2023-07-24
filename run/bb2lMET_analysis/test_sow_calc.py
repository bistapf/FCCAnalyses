import ROOT

def get_rdf(input_filepath):

	print("Getting rdf from:", input_filepath)

	if input_filepath.endswith(".root"):
		rdf = ROOT.RDataFrame("events", input_filepath)
	else:
		print("Adding chunks ..")
		# rdf = ROOT.RDataFrame("events", input_filepath+"/chunk99.root")
		rdf = ROOT.RDataFrame("events", input_filepath+"/chunk*")

	if not rdf:
		print("Empty file for:", input_filepath, " Exiting.")
		return

	# print(rdf.GetColumnNames())

	return rdf

def test_RDF_calc(input_file):

	rdf = get_rdf(input_file)

	sow = rdf.Histo1D("weight", "weight").Integral()
	nevts = rdf.Histo1D("weight").Integral()
	print(rdf.Histo1D("weight").GetMean()*nevts)
	return nevts, sow

def test_evtLoop_calc(input_filepath):
	input_file = ROOT.TFile(input_filepath, "READ")
	tree = input_file.Get("events")

	sow = 0
	nevts = 0 
	for event in tree:  
		weight = float(event.weight[0])
		sow += weight
		nevts +=1 

	return nevts, sow

if __name__ == "__main__":

	input_file = "/eos/user/b/bistapf/FCChh_EvtGen/bb2lMET_ntuples/SFOS/pwp8_pp_hh_lambda100_5f_hhbbww/chunk197.root"

	#NEED TO TEST: events_000013364 EDM4HEP FILE STILL /eos/experiment/fcc/hh/generation/DelphesEvents/fcc_v05_scenarioI//pwp8_pp_hh_lambda100_5f_hhbbww/events_000013364.root

	nevts_RDF, sow_RDF = test_RDF_calc(input_file)
	print(nevts_RDF)
	print(sow_RDF)

	nevts_loop, sow_loop = test_evtLoop_calc(input_file)
	print(nevts_loop)
	print(sow_loop)

