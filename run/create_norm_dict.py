#script to create/update the .json file with the dictionary used for normalisation 
import os
import json
import glob
import argparse
from FCCAnalysisRun import get_entries_sow

fcchh_hh_dict = {
	#signals with kappa lambda = 1
	"pwp8_pp_hh_lambda100_5f_hhbbzz_zleptonic": {"numberOfEvents": 50000, "sumOfWeights": 50000.0, "crossSection": 0.00345168, "kfactor": 1.08, "matchingEfficiency": 1.0},
	"pwp8_pp_hh_lambda100_5f_hhbbww": {"numberOfEvents": 50000, "sumOfWeights": 50000.0, "crossSection": 0.28332, "kfactor": 1.08, "matchingEfficiency": 1.0},
	"pwp8_pp_hh_lambda100_5f_hhbbtata": {"numberOfEvents": 4997958, "sumOfWeights": 4997958.0, "crossSection": 0.08214306096, "kfactor": 1.08, "matchingEfficiency": 1.0},
	"pwp8_pp_hh_lambda100_5f_hhbbaa": {"numberOfEvents": 4980000, "sumOfWeights": 4980000.0, "crossSection": 0.0029844128399999998, "kfactor": 1.075363, "matchingEfficiency": 1.0},
	#top backgrounds 
	"mgp8_pp_tt012j_5f": {"numberOfEvents": 79190000, "sumOfWeights": 79190000.0, "crossSection": 43110.0, "kfactor": 1.74, "matchingEfficiency": 1.0},	
	"mgp8_pp_t123j_5f": {"numberOfEvents": 3081020, "sumOfWeights": 3081020.0, "crossSection": 7524.0, "kfactor": 2.16, "matchingEfficiency": 1.0},
	#ttV(V) backgrounds
	"mgp8_pp_ttz_5f": {"numberOfEvents": 1000000, "sumOfWeights": 1000000.0, "crossSection": 38.05, "kfactor": 1.68, "matchingEfficiency": 1.0},
	"mgp8_pp_ttzz_5f": {"numberOfEvents": 990000, "sumOfWeights": 990000.0, "crossSection": 0.1206, "kfactor": 1.3, "matchingEfficiency": 1.0},
	"mgp8_pp_ttw_5f": {"numberOfEvents": 1600000, "sumOfWeights": 1600000.0, "crossSection": 6.545, "kfactor": 2.5, "matchingEfficiency": 1.0},
	"mgp8_pp_ttww_4f": {"numberOfEvents": 1600000, "sumOfWeights": 1600000.0, "crossSection": 0.7827, "kfactor": 1.4, "matchingEfficiency": 1.0},
	"mgp8_pp_ttwz_5f": {"numberOfEvents": 1567024, "sumOfWeights": 1567024.0, "crossSection": 0.07427, "kfactor": 2.3, "matchingEfficiency": 1.0},
	#single Higgs bkgs
	"mgp8_pp_h012j_5f": {"numberOfEvents": 6600000, "sumOfWeights": 6600000.0, "crossSection": 587.5, "kfactor": 3.76, "matchingEfficiency": 1.0},
	"mgp8_pp_vh012j_5f": {"numberOfEvents": 1600000, "sumOfWeights": 1600000.0, "crossSection": 37.43, "kfactor": 1.32, "matchingEfficiency": 1.0},
	"mgp8_pp_vbf_h01j_5f": {"numberOfEvents": 6600000, "sumOfWeights": 6600000.0, "crossSection": 84.17, "kfactor": 4.3, "matchingEfficiency": 1.0},
	"mgp8_pp_tth01j_5f": {"numberOfEvents": 970000, "sumOfWeights": 970000.0, "crossSection": 44.84, "kfactor": 1.22, "matchingEfficiency": 1.0},
	#V+jets bkgs
	"mgp8_pp_vj_5f_HT_10000_27000": {"numberOfEvents": 1980000, "sumOfWeights": 1980000.0, "crossSection": 0.008647, "kfactor": 2.0, "matchingEfficiency": 1.0},
	"mgp8_pp_vj_5f_HT_1000_2000": {"numberOfEvents": 1980000, "sumOfWeights": 1980000.0, "crossSection": 191.6, "kfactor": 2.0, "matchingEfficiency": 1.0},
	"mgp8_pp_vj_5f_HT_2000_5000": {"numberOfEvents": 1980000, "sumOfWeights": 1980000.0, "crossSection": 14.47, "kfactor": 2.0, "matchingEfficiency": 1.0},
	"mgp8_pp_vj_5f_HT_27000_100000": {"numberOfEvents": 1970000, "sumOfWeights": 1970000.0, "crossSection": 7.24e-06, "kfactor": 2.0, "matchingEfficiency": 1.0},
	"mgp8_pp_vj_5f_HT_5000_10000": {"numberOfEvents": 2000000, "sumOfWeights": 2000000.0, "crossSection": 0.2814, "kfactor": 2.0, "matchingEfficiency": 1.0},
	"mgp8_pp_vj_5f_HT_500_1000": {"numberOfEvents": 2000000, "sumOfWeights": 2000000.0, "crossSection": 2034.0, "kfactor": 2.0, "matchingEfficiency": 1.0},
	#jjaa background
	"mgp8_pp_jjaa01j_5f": {"numberOfEvents": 50000, "sumOfWeights": 50000.0, "crossSection": 55.72, "kfactor": 1.0, "matchingEfficiency": 0.236},
	#to be added!
	# "mgp8_pp_bbtata_QED": {"numberOfEvents": 4910000, "sumOfWeights": 4910000.0, "crossSection": 0.5519, "kfactor": 1.0, "matchingEfficiency": 1.0},
	# "mgp8_pp_bbtata_QCDQED": {"numberOfEvents": 4950000, "sumOfWeights": 4950000.0, "crossSection": 75.61, "kfactor": 1.0, "matchingEfficiency": 1.0},
	# "mgp8_pp_bbjj_QCD_5f": {"numberOfEvents": 4680000, "sumOfWeights": 4680000.0, "crossSection": 7613653.4636, "kfactor": 1.0, "matchingEfficiency": 1.0},
	
	# "mgp8_pp_vj_4f_M_5000_inf": {"numberOfEvents": 4870000, "sumOfWeights": 4870000.0, "crossSection": 0.4679, "kfactor": 2.0, "matchingEfficiency": 1.0},
	
	# "mgp8_pp_tthh_lambda100_5f": {"numberOfEvents": 910000, "sumOfWeights": 910000.0, "crossSection": 0.0595724055, "kfactor": 1.378155, "matchingEfficiency": 1.0},

}

def get_nevts_sum_of_weights(files_dir):

	nevts = 0
	sow = 0 

	files_list = glob.glob(files_dir + "/chunk*.root")
	for file in files_list:
		# print(file)
		nevts_param, _, sow_param, _ = get_entries_sow(file, get_local=False)
		nevts+= nevts_param
		sow+=sow_param

	return nevts, sow

if __name__ == "__main__":

	parser = argparse.ArgumentParser(prog='UpdateRefsFromLocal', description='Script to create the normalisation dict from FCCAnalyses ntuples')
	parser.add_argument('-i', '--indir', dest="indir", required=True, help="Input directory to run on." )  
	parser.add_argument('-o', '--outname', dest="outname", default="FCChh_procDict_v05_scenarioI", help="Name of the json file." ) 

	args = parser.parse_args()

	fcchh_hh_dict_out = dict(fcchh_hh_dict)

	for process_name, process_info in fcchh_hh_dict.items():
		print(process_name)
		files_dir = os.path.join(args.indir, process_name)
		if not os.path.exists(files_dir):
			print("No files found for process", process_name, " Continuing with next one.")
			fcchh_hh_dict_out.pop(process_name)
			continue 

		nevts, sow = get_nevts_sum_of_weights(files_dir)
	# 	#replace the entries
		fcchh_hh_dict_out[process_name]["numberOfEvents"] = nevts
		fcchh_hh_dict_out[process_name]["sumOfWeights"] = sow

	outfile = os.path.join(args.indir, args.outname+".json")
	print("Creating json at:", outfile)
	with open(outfile, 'w') as convert_file:
		convert_file.write(json.dumps(fcchh_hh_dict_out, indent=0))

# python create_norm_dict.py -i /eos/user/b/bistapf/FCChh_EvtGen/bb2lMET_ntuples/SFOS/