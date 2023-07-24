from collections import namedtuple
import ROOT


processSpecs = namedtuple('processSpecs', ['sample_list', 'colour_key', 'title'])

########################################### common backgrounds ########################################### 
old_bkgs = {
	"ttbar":processSpecs(sample_list=["mgp8_pp_tt012j_5f"], colour_key=ROOT.TColor.GetColor("#2E9094"), title="#it{t#bar{t}}" ), #TODO: ADD BACK WHEN FIXED
	"V_jets":processSpecs(sample_list=["mgp8_pp_vj_5f_HT_500_1000", "mgp8_pp_vj_5f_HT_1000_2000", 
							"mgp8_pp_vj_5f_HT_2000_5000", "mgp8_pp_vj_5f_HT_5000_10000", "mgp8_pp_vj_5f_HT_10000_27000", "mgp8_pp_vj_5f_HT_27000_100000"], 
							colour_key=ROOT.TColor.GetColor("#00aab6"), title="#it{V}+jets" ), #no surviving events in the local test run ..
	"ttZ":processSpecs(sample_list=["mgp8_pp_ttz_5f"], colour_key=ROOT.TColor.GetColor("#66c79f"), title="#it{t#bar{t}Z}" ),
	"ttH":processSpecs(sample_list=["mgp8_pp_tth01j_5f"], colour_key=ROOT.TColor.GetColor("#c1eb88"), title="#it{t#bar{t}H}" ),
	"ttZZ":processSpecs(sample_list=["mgp8_pp_ttzz_5f"], colour_key=ROOT.TColor.GetColor("#fcfcc6"), title="#it{t#bar{t}ZZ}" ),	
}

##bkgs with all single H merged
new_bkgs ={
	"ttbar":processSpecs(sample_list=["mgp8_pp_tt012j_5f"], colour_key=ROOT.TColor.GetColor("#2E9094"), title="#it{t#bar{t}}" ), 
	"single_top":processSpecs(sample_list=["mgp8_pp_t123j_5f"], colour_key=ROOT.TColor.GetColor("#e6f4f1"), title="Single top" ), #TODO: CHANGE COLOUR 
	"V_jets":processSpecs(sample_list=["mgp8_pp_vj_5f_HT_500_1000", "mgp8_pp_vj_5f_HT_1000_2000", 
							"mgp8_pp_vj_5f_HT_2000_5000", "mgp8_pp_vj_5f_HT_5000_10000", "mgp8_pp_vj_5f_HT_10000_27000", "mgp8_pp_vj_5f_HT_27000_100000"], 
							colour_key=ROOT.TColor.GetColor("#00aab6"), title="#it{V}+jets" ), #no surviving events in the local test run ..
	"ttV":processSpecs(sample_list=["mgp8_pp_ttz_5f", "mgp8_pp_ttw_5f"], colour_key=ROOT.TColor.GetColor("#66c79f"), title="#it{t#bar{t}V}" ),
	"ttVV":processSpecs(sample_list=["mgp8_pp_ttzz_5f", "mgp8_pp_ttww_4f", "mgp8_pp_ttwz_5f"], colour_key=ROOT.TColor.GetColor("#fcfcc6"), title="#it{t#bar{t}VV}" ),
	"Single_Higgs":processSpecs(sample_list=["mgp8_pp_tth01j_5f", "mgp8_pp_h012j_5f", "mgp8_pp_vh012j_5f", "mgp8_pp_vbf_h01j_5f"], colour_key=ROOT.TColor.GetColor("#c1eb88"), title="Single Higgs" ),
}


##option for checking selection: single Hs are kept separate
# new_bkgs ={
# 	"ttbar":processSpecs(sample_list=["mgp8_pp_tt012j_5f"], colour_key=ROOT.TColor.GetColor("#2E9094"), title="#it{t#bar{t}}" ), 
# 	"single_top":processSpecs(sample_list=["mgp8_pp_t123j_5f"], colour_key=ROOT.TColor.GetColor("#e6f4f1"), title="Single top" ), #TODO: CHANGE COLOUR 
# 	"V_jets":processSpecs(sample_list=["mgp8_pp_vj_5f_HT_500_1000", "mgp8_pp_vj_5f_HT_1000_2000", 
# 							"mgp8_pp_vj_5f_HT_2000_5000", "mgp8_pp_vj_5f_HT_5000_10000", "mgp8_pp_vj_5f_HT_10000_27000", "mgp8_pp_vj_5f_HT_27000_100000"], 
# 							colour_key=ROOT.TColor.GetColor("#00aab6"), title="#it{V}+jets" ), #no surviving events in the local test run ..
# 	"ttV":processSpecs(sample_list=["mgp8_pp_ttz_5f", "mgp8_pp_ttw_5f"], colour_key=ROOT.TColor.GetColor("#66c79f"), title="#it{t#bar{t}V}" ),
# 	"ttVV":processSpecs(sample_list=["mgp8_pp_ttzz_5f", "mgp8_pp_ttww_4f", "mgp8_pp_ttwz_5f"], colour_key=ROOT.TColor.GetColor("#fcfcc6"), title="#it{t#bar{t}VV}" ),
# 	"ggF_Higgs":processSpecs(sample_list=["mgp8_pp_h012j_5f"], colour_key=ROOT.TColor.GetColor("#c1eb88"), title="ggH" ),
# 	"VBF_Higgs":processSpecs(sample_list=["mgp8_pp_vbf_h01j_5f"], colour_key=ROOT.TColor.GetColor("#c1eb88"), title="VBFH" ),
# 	"VH_Higgs":processSpecs(sample_list=["mgp8_pp_vh012j_5f"], colour_key=ROOT.TColor.GetColor("#c1eb88"), title="VH" ),
# 	"ttH_Higgs":processSpecs(sample_list=["mgp8_pp_tth01j_5f"], colour_key=ROOT.TColor.GetColor("#c1eb88"), title="ttH" ),
# }

########################################### bbZZ(llvv) analysis ########################################### 
bbzz_llvv_signal = {
	"signal":processSpecs(sample_list=["pwp8_pp_hh_lambda100_5f_hhbbzz_zleptonic"], colour_key=ROOT.kBlack, title="#it{HH(bbZZ)}" ),
}

#bbZZ signal and old bkgs
bbzz_processes = bbzz_llvv_signal.copy()
bbzz_processes.update(old_bkgs)

#bbZZ signal and new bkgs
bbzz_processes_new = bbzz_llvv_signal.copy()
bbzz_processes_new.update(new_bkgs)

########################################### bbtautau(lvlv) analysis ########################################### 
bbtautau_signal = {
	"signal":processSpecs(sample_list=["pwp8_pp_hh_lambda100_5f_hhbbtata"], colour_key=ROOT.kBlack, title="#it{HH(bb#tau#tau)}" ),
}

#bbZZ signal and old bkgs
bbtautau_processes = bbtautau_signal.copy()
bbtautau_processes.update(old_bkgs)

#bbZZ signal and new bkgs
bbtautau_processes_new = bbtautau_signal.copy()
bbtautau_processes_new.update(new_bkgs)

########################################### bbWW(lvlv) analysis ########################################### 
bbWW_signal = {
	"signal":processSpecs(sample_list=["pwp8_pp_hh_lambda100_5f_hhbbww"], colour_key=ROOT.kBlack, title="#it{HH(bbWW)}" ),
}

#bbZZ signal and old bkgs
bbWW_processes = bbWW_signal.copy()
bbWW_processes.update(old_bkgs)

#bbZZ signal and new bkgs
bbWW_processes_new = bbWW_signal.copy()
bbWW_processes_new.update(new_bkgs)

#bbWW signals at different kappa_lambda + new bkgs
bbWW_signals = {
	"ggHH_kl_1_kt_1_hbbhww":processSpecs(sample_list=["pwp8_pp_hh_lambda100_5f_hhbbww"], colour_key=ROOT.kBlack, title="#it{HH(bbWW)}" ),
	"ggHH_kl_0p4_kt_1_hbbhww":processSpecs(sample_list=["pwp8_pp_hh_lambda040_5f_hhbbww"], colour_key=ROOT.kBlack, title="#it{HH(bbWW)}" ),
	"ggHH_kl_2p4_kt_1_hbbhww":processSpecs(sample_list=["pwp8_pp_hh_lambda240_5f_hhbbww"], colour_key=ROOT.kBlack, title="#it{HH(bbWW)}" ),
	"ggHH_kl_0p0_kt_1_hbbhww":processSpecs(sample_list=["pwp8_pp_hh_lambda000_5f_hhbbww"], colour_key=ROOT.kBlack, title="#it{HH(bbWW)}" ),
	"ggHH_kl_3p0_kt_1_hbbhww":processSpecs(sample_list=["pwp8_pp_hh_lambda300_5f_hhbbww"], colour_key=ROOT.kBlack, title="#it{HH(bbWW)}" ),
}

bbWW_processes_kl = bbWW_signals.copy()
bbWW_processes_kl.update(new_bkgs)

########################################### bb2lMET analyses with merged signals ########################################### 

#TESTER FOR NEW CARD
bb2l_DFOS_signals = {
	"signal":processSpecs(sample_list=["pwp8_pp_hh_lambda100_5f_hhbbww"], colour_key=ROOT.kBlack, title="#it{HH(bbll+MET)}" ),
	# "signal":processSpecs(sample_list=["pwp8_pp_hh_lambda100_5f_hhbbww", "pwp8_pp_hh_lambda100_5f_hhbbtata", "pwp8_pp_hh_lambda100_5f_hhbbzz_zleptonic"], colour_key=ROOT.kBlack, title="#it{HH(bbll+MET)}" ),
	#TEMP
	"ttbar":processSpecs(sample_list=["mgp8_pp_tt012j_5f"], colour_key=ROOT.TColor.GetColor("#2E9094"), title="#it{t#bar{t}}" )
} 

bb2l_DFOS_processes = bb2l_DFOS_signals.copy()
# bb2l_DFOS_processes.update(new_bkgs) #TEMP

#for kappa-lambda interpretation
bb2l_DFOS_signals = {
	"ggHH_kl_1_kt_1":processSpecs(sample_list=["pwp8_pp_hh_lambda100_5f_hhbbww", "pwp8_pp_hh_lambda100_5f_hhbbtata", "pwp8_pp_hh_lambda100_5f_hhbbzz_zleptonic"], colour_key=ROOT.kBlack, title="#it{HH(bbll+MET)}" ),
	# "ggHH_kl_0p0_kt_1":processSpecs(sample_list=["pwp8_pp_hh_lambda000_5f_hhbbww", "pwp8_pp_hh_lambda000_5f_hhbbtata", "pwp8_pp_hh_lambda000_5f_hhbbzz_zleptonic"], colour_key=ROOT.kBlack, title="#it{HH(bbll+MET)}" ),
	"ggHH_kl_0p4_kt_1":processSpecs(sample_list=["pwp8_pp_hh_lambda040_5f_hhbbww", "pwp8_pp_hh_lambda040_5f_hhbbtata", "pwp8_pp_hh_lambda040_5f_hhbbzz_zleptonic"], colour_key=ROOT.kBlack, title="#it{HH(bbll+MET)}" ),
	"ggHH_kl_2p4_kt_1":processSpecs(sample_list=["pwp8_pp_hh_lambda240_5f_hhbbww", "pwp8_pp_hh_lambda240_5f_hhbbtata", "pwp8_pp_hh_lambda240_5f_hhbbzz_zleptonic"], colour_key=ROOT.kBlack, title="#it{HH(bbll+MET)}" ),
	# "ggHH_kl_3p0_kt_1":processSpecs(sample_list=["pwp8_pp_hh_lambda300_5f_hhbbww", "pwp8_pp_hh_lambda300_5f_hhbbtata", "pwp8_pp_hh_lambda300_5f_hhbbzz_zleptonic"], colour_key=ROOT.kBlack, title="#it{HH(bbll+MET)}" ),
} 

bb2l_DFOS_processes_kl = bb2l_DFOS_signals.copy()
bb2l_DFOS_processes_kl.update(new_bkgs)

########################################### Naming for combination with Angelas WS ########################################### 

#for kappa-lambda interpretation
bb2l_combination_signals = {
	"GluGluToHH_1":processSpecs(sample_list=["pwp8_pp_hh_lambda100_5f_hhbbww", "pwp8_pp_hh_lambda100_5f_hhbbtata", "pwp8_pp_hh_lambda100_5f_hhbbzz_zleptonic"], colour_key=ROOT.kBlack, title="#it{HH(bbll+MET)}" ),
	# "ggHH_kl_0p0_kt_1":processSpecs(sample_list=["pwp8_pp_hh_lambda000_5f_hhbbww", "pwp8_pp_hh_lambda000_5f_hhbbtata", "pwp8_pp_hh_lambda000_5f_hhbbzz_zleptonic"], colour_key=ROOT.kBlack, title="#it{HH(bbll+MET)}" ),
	# "ggHH_kl_0p4_kt_1":processSpecs(sample_list=["pwp8_pp_hh_lambda040_5f_hhbbww", "pwp8_pp_hh_lambda040_5f_hhbbtata", "pwp8_pp_hh_lambda040_5f_hhbbzz_zleptonic"], colour_key=ROOT.kBlack, title="#it{HH(bbll+MET)}" ),
	"GluGluToHH_2p45":processSpecs(sample_list=["pwp8_pp_hh_lambda240_5f_hhbbww", "pwp8_pp_hh_lambda240_5f_hhbbtata", "pwp8_pp_hh_lambda240_5f_hhbbzz_zleptonic"], colour_key=ROOT.kBlack, title="#it{HH(bbll+MET)}" ),
	"GluGluToHH_5":processSpecs(sample_list=["pwp8_pp_hh_lambda300_5f_hhbbww", "pwp8_pp_hh_lambda300_5f_hhbbtata", "pwp8_pp_hh_lambda300_5f_hhbbzz_zleptonic"], colour_key=ROOT.kBlack, title="#it{HH(bbll+MET)}" ),
} 

bb2l_combination_processes_kl = bb2l_combination_signals.copy()
bb2l_combination_processes_kl.update(new_bkgs)

########################################### ALL PROCESSES ########################################### 

all_processes = new_bkgs.copy()
#kappa lambda = 1 SM signals
all_processes["pwp8_pp_hh_lambda100_5f_hhbbww"] = processSpecs(sample_list=["pwp8_pp_hh_lambda100_5f_hhbbww"], colour_key=ROOT.kBlack, title="#it{HH(bbWW)}" )
all_processes["pwp8_pp_hh_lambda100_5f_hhbbtata"] = processSpecs(sample_list=["pwp8_pp_hh_lambda100_5f_hhbbtata"], colour_key=ROOT.kMagenta+2, title="#it{HH(bb#tau#tau)}" )
all_processes["pwp8_pp_hh_lambda100_5f_hhbbzz_zleptonic"] = processSpecs(sample_list=["pwp8_pp_hh_lambda100_5f_hhbbzz_zleptonic"], colour_key=ROOT.kBlack, title="#it{HH(bbZZ)}" )
# all_processes["pwp8_pp_hh_lambda100_5f_hhbbzz_zleptonic"] = processSpecs(sample_list=["pwp8_pp_hh_lambda100_5f_hhbbzz_zleptonic"], colour_key=ROOT.kBlack, title="#it{HH(bbZZ)}" )

#bbWW kappalambda samples
all_processes["pwp8_pp_hh_lambda040_5f_hhbbww"] = processSpecs(sample_list=["pwp8_pp_hh_lambda040_5f_hhbbww"], colour_key=ROOT.kRed+2, title="#it{HH(bbWW)}" )
all_processes["pwp8_pp_hh_lambda240_5f_hhbbww"] = processSpecs(sample_list=["pwp8_pp_hh_lambda240_5f_hhbbww"], colour_key=ROOT.kRed+2, title="#it{HH(bbWW)}" )
all_processes["pwp8_pp_hh_lambda300_5f_hhbbww"] = processSpecs(sample_list=["pwp8_pp_hh_lambda300_5f_hhbbww"], colour_key=ROOT.kRed+2, title="#it{HH(bbWW)}" )
all_processes["pwp8_pp_hh_lambda000_5f_hhbbww"] = processSpecs(sample_list=["pwp8_pp_hh_lambda000_5f_hhbbww"], colour_key=ROOT.kRed+2, title="#it{HH(bbWW)}" )

#bbtautau kappalambda samples
all_processes["pwp8_pp_hh_lambda040_5f_hhbbtataa"] = processSpecs(sample_list=["pwp8_pp_hh_lambda040_5f_hhbbtata"], colour_key=ROOT.kRed+2, title="#it{HH(bb#tau#tau)}" )
all_processes["pwp8_pp_hh_lambda240_5f_hhbbtataa"] = processSpecs(sample_list=["pwp8_pp_hh_lambda240_5f_hhbbtata"], colour_key=ROOT.kRed+2, title="#it{HH(bb#tau#tau)}" )
all_processes["pwp8_pp_hh_lambda300_5f_hhbbtataa"] = processSpecs(sample_list=["pwp8_pp_hh_lambda300_5f_hhbbtata"], colour_key=ROOT.kRed+2, title="#it{HH(bb#tau#tau)}" )
all_processes["pwp8_pp_hh_lambda000_5f_hhbbtataa"] = processSpecs(sample_list=["pwp8_pp_hh_lambda000_5f_hhbbtata"], colour_key=ROOT.kRed+2, title="#it{HH(bb#tau#tau)}" )

#bbZZ kappalambda samples
all_processes["pwp8_pp_hh_lambda040_5f_hhbbzz_zleptonic"] = processSpecs(sample_list=["pwp8_pp_hh_lambda040_5f_hhbbzz_zleptonic"], colour_key=ROOT.kRed+2, title="#it{HH(bbZZ)}" )
all_processes["pwp8_pp_hh_lambda240_5f_hhbbzz_zleptonic"] = processSpecs(sample_list=["pwp8_pp_hh_lambda240_5f_hhbbzz_zleptonic"], colour_key=ROOT.kRed+2, title="#it{HH(bbZZ)}" )
all_processes["pwp8_pp_hh_lambda300_5f_hhbbzz_zleptonic"] = processSpecs(sample_list=["pwp8_pp_hh_lambda300_5f_hhbbzz_zleptonic"], colour_key=ROOT.kRed+2, title="#it{HH(bbZZ)}" )
all_processes["pwp8_pp_hh_lambda000_5f_hhbbzz_zleptonic"] = processSpecs(sample_list=["pwp8_pp_hh_lambda000_5f_hhbbzz_zleptonic"], colour_key=ROOT.kRed+2, title="#it{HH(bbZZ)}" )


## adding a combined all bkgs for the BDT setup:
all_processes["other_bkgs"] = processSpecs(sample_list=["mgp8_pp_vj_5f_HT_500_1000", "mgp8_pp_vj_5f_HT_1000_2000", "mgp8_pp_vj_5f_HT_2000_5000", 
														"mgp8_pp_vj_5f_HT_5000_10000", "mgp8_pp_vj_5f_HT_10000_27000", "mgp8_pp_vj_5f_HT_27000_100000", #V_jets
														"mgp8_pp_t123j_5f", #single top
														"mgp8_pp_ttz_5f", "mgp8_pp_ttw_5f", #ttV
														"mgp8_pp_ttzz_5f", "mgp8_pp_ttww_4f", "mgp8_pp_ttwz_5f", #ttVV
														"mgp8_pp_tth01j_5f", "mgp8_pp_h012j_5f", "mgp8_pp_vh012j_5f", "mgp8_pp_vbf_h01j_5f", #single H
														], 
											colour_key=ROOT.TColor.GetColor("#c1eb88"), 
											title="Other" )

# other bkgs that are not single H or ttbar grouped
all_processes["rest"] = processSpecs(sample_list=["mgp8_pp_vj_5f_HT_500_1000", "mgp8_pp_vj_5f_HT_1000_2000", "mgp8_pp_vj_5f_HT_2000_5000", 
														"mgp8_pp_vj_5f_HT_5000_10000", "mgp8_pp_vj_5f_HT_10000_27000", "mgp8_pp_vj_5f_HT_27000_100000", #V_jets
														"mgp8_pp_t123j_5f", #single top
														"mgp8_pp_ttz_5f", "mgp8_pp_ttw_5f", #ttV
														"mgp8_pp_ttzz_5f", "mgp8_pp_ttww_4f", "mgp8_pp_ttwz_5f", #ttVV
														], 
											colour_key=ROOT.kMagenta+2, 
											title="Rest" )
