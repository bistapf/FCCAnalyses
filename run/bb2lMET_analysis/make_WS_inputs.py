import ROOT
import os
import argparse
import bb2lMET_plots as plot_list
import bb2l_categories as categories

from draw_plots import makePlot, getEvtsProcessedDict, bbZZllvv_labels_dict, bbtautau_emu_labels_dict, bbWW_emu_labels_dict

from bb2lMET_processes import bbzz_processes, bbzz_processes_new, bbtautau_processes, bbtautau_processes_new, bbWW_processes, bbWW_processes_new, all_processes, bbWW_processes_kl, bb2l_DFOS_processes, bb2l_DFOS_processes_kl, bb2l_combination_processes_kl

def storeWSInput(var_name, cut_level, in_dir, out_dir, processes, signal_cat, labels_dict, do_addOverlow=True, extra_cut=("","")):

	#need the nevtsDict for normalisation:
	nevts_dict = getEvtsProcessedDict( args.inDir, bb2l_DFOS_processes) #TEMP
	# nevts_dict = getEvtsProcessedDict( args.inDir, all_processes)

	plots = plot_list.common_sel_vars

	makePlot(var_name, in_dir, processes, cut_level, nevts_dict, out_dir, labels_dict, plots, store_root_file=True, addOverlow=do_addOverlow, signal_cat=signal_cat, extra_cut=extra_cut)

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Plot distributions for FCC-hh events of type HH(2l+MET)")
	parser.add_argument('--input', '-i', metavar="INPUTDIR", dest="inDir", required=True, help="Path to the input directory")
	parser.add_argument('--outdir', '-o', metavar="OUTPUTDIR", dest="outDir", required=True, help="Output directory, if not specified subdir called Cutflows of working dir.")
	parser.add_argument('--signalCat', metavar="SIGNALCAT", dest="signalCat", required=True, help="Signal category of the analysis: bbZZllvv, or ..?")
	parser.add_argument('--kappaLambda', default=False, action="store_true", help="""Run for kappa-lambda ws: Include signals at multiple kappa_lambda""")
	parser.add_argument('--extraCut', metavar="CUT", dest="extra_cut", required=False, help="Additional cut string on top of base selection, e.g. to define categories")
	parser.add_argument('--smeared', default=False, action="store_true", help="Use smeared mT2HH")
	parser.add_argument('--forComb', default=False, action="store_true", help="Use smeared mT2HH")
	
	args = parser.parse_args()

	print("Going to produce workspace inputs using mT2_HH histograms for analysis:", args.signalCat)



	#settings
	if args.signalCat == "bbtautau_emu":
		processes = bbtautau_processes_new
		files_dir = os.path.join(args.inDir, "bbtautau_emu_analysis")
		cut_level = "sel9_dphiZMET_12"
		labels_dict = bbtautau_emu_labels_dict
		fit_var = "mT2_HH_selBinning"

	elif args.signalCat == "bbZZllvv":
		processes = bbzz_processes_new
		files_dir = os.path.join(args.inDir, "bbZZllvv_analysis")
		cut_level = "sel9_dphiZMET_12"
		labels_dict = bbZZllvv_labels_dict
		fit_var = "mT2_HH_selBinning"

	elif args.signalCat == "bbWW_emu":
		processes = bbWW_processes_new
		if args.kappaLambda:
			processes = bbWW_processes_kl
		files_dir = os.path.join(args.inDir, "bbWW_emu_analysis")
		cut_level = "sel9_mlb_150"
		labels_dict = bbWW_emu_labels_dict
		fit_var = "mT2_HH_selBinning"

	elif args.signalCat == "bb2l_DFOS":
		processes = bb2l_DFOS_processes
		if args.kappaLambda: 
			processes = bb2l_DFOS_processes_kl
		files_dir = os.path.join(args.inDir, "bbWW_emu_analysis") #using the selection from bbWW(emu), not optimum for bbtautau but as a start
		# cut_level = "sel8_HT2_ratio" #try fitting mlb_reco instead of cutting on it!
		cut_level = "sel9_mlb_150"
		labels_dict = bbWW_emu_labels_dict
		fit_var = "mT2_HH_selBinning"

	elif args.signalCat == "bb2l_SFOS_noZ":
		processes = bb2l_DFOS_processes
		if args.kappaLambda: 
			processes = bb2l_DFOS_processes_kl
		files_dir = os.path.join(args.inDir, "noZ") #using the selection from bbWW(emu), not optimum for bbtautau but as a start
		# cut_level = "sel8_HT2_ratio" #try fitting mlb_reco instead of cutting on it!
		cut_level = "sel9_mlb_150"
		labels_dict = bbWW_emu_labels_dict
		fit_var = "mT2_HH_selBinning"

	#bbZZ aimed channel but with all signals
	elif args.signalCat == "bb2l_SFOS_Zpeak":
		processes = bb2l_DFOS_processes
		if args.kappaLambda:
			processes = bb2l_DFOS_processes_kl
		files_dir = os.path.join(args.inDir, "bbZZllvv_analysis") #using the selection from bbWW(emu), not optimum for bbtautau but as a start
		# cut_level = "sel8_HT2_ratio" #try fitting mlb_reco instead of cutting on it!
		cut_level = "sel9_mlb_150"
		labels_dict = bbZZllvv_labels_dict
		fit_var = "mT2_HH_selBinning_SFOS_Z_peak"

	if args.smeared:
		fit_var = "mT2_HH_smeared_selBinning"

	if args.forComb and args.kappaLambda:
		processes = bb2l_combination_processes_kl

	if args.extra_cut:
		extra_cut_string = categories.bb2l_cats[args.extra_cut]
		# storeWSInput("mlb_reco_zoom", cut_level, files_dir, args.outDir, processes, signal_cat=args.signalCat, labels_dict=labels_dict, do_addOverlow=True, extra_cut=(args.extra_cut,extra_cut_string))
		storeWSInput(fit_var, cut_level, files_dir, args.outDir, processes, signal_cat=args.signalCat, labels_dict=labels_dict, do_addOverlow=True, extra_cut=(args.extra_cut,extra_cut_string))
		# storeWSInput("m_pseudo_HH_selBinning", cut_level, files_dir, args.outDir, processes, signal_cat=args.signalCat, labels_dict=labels_dict, do_addOverlow=True, extra_cut=(args.extra_cut,extra_cut_string))
		 

	else: 
		# storeWSInput("mlb_reco_zoom", cut_level, files_dir, args.outDir, processes, signal_cat=args.signalCat, labels_dict=labels_dict, do_addOverlow=True)
		storeWSInput(fit_var, cut_level, files_dir, args.outDir, processes, signal_cat=args.signalCat, labels_dict=labels_dict, do_addOverlow=True)
		# storeWSInput("m_pseudo_HH_selBinning", cut_level, files_dir, args.outDir, processes, signal_cat=args.signalCat, labels_dict=labels_dict, do_addOverlow=True)


#commands:
# python make_WS_inputs.py -i /eos/user/b/bistapf/FCCAnalysesFiles/HH_bb2lMET_analysis/preSel_DFOS_quartStat/ -o ./Plots_bbtautau_emu/ --signalCat bbtautau_emu
# python make_WS_inputs.py -i /eos/user/b/bistapf/FCCAnalysesFiles/HH_bb2lMET_analysis/preSel_DFOS_quartStat/ -o ./Plots_bbWW_emu/ --signalCat bbWW_emu
# python make_WS_inputs.py -i /eos/user/b/bistapf/FCCAnalysesFiles/HH_bb2lMET_analysis/preSel_SFOS_quartStat/ -o ./Plots_bbZZllvv/ --signalCat bbZZllvv

# python make_WS_inputs.py -i /eos/user/b/bistapf/FCCAnalysesFiles/HH_bb2lMET_analysis/preSel_DFOS_quartStat/ -o ./Plots_bbWW_emu_kl/ --signalCat bbWW_emu --kappaLambda

# merging bbWW+bbtautau w. bbWW selection
#python make_WS_inputs.py -i /eos/user/b/bistapf/FCCAnalysesFiles/HH_bb2lMET_analysis/preSel_DFOS_quartStat/ -o ./Plots_bb2lMET_DFOS --signalCat bb2l_DFOS

#make category
#python make_WS_inputs.py -i /eos/user/b/bistapf/FCCAnalysesFiles/HH_bb2lMET_analysis/preSel_DFOS_quartStat/ -o ./Plots_bb2lMET_DFOS --signalCat bb2l_DFOS --extraCut bb2l_DFOS_low_dphi

# with extra cut on MET
#python make_WS_inputs.py -i /eos/user/b/bistapf/FCCAnalysesFiles/HH_bb2lMET_analysis/preSel_DFOS_fullStat/ -o ./Plots_bb2lMET_DFOS --signalCat bb2l_DFOS --extraCut 

#bbZZ analysis with all signals 
# python make_WS_inputs.py -i /eos/user/b/bistapf/FCCAnalysesFiles/HH_bb2lMET_analysis/preSel_SFOS_fullStat/ -o ./Plots_bb2lMET_SFOS_Zpeak/ --signalCat bb2l_SFOS_Zpeak
# python make_WS_inputs.py -i /eos/user/b/bistapf/FCCAnalysesFiles/HH_bb2lMET_analysis/preSel_SFOS_fullStat/ -o ./Plots_bb2lMET_SFOS_Zpeak/ --signalCat bb2l_SFOS_Zpeak