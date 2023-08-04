from collections import namedtuple
import ROOT


#variables to plot:
default_binning = 25 
PlotSpecs = namedtuple('PlotSpecs', ['name', 'xmin', 'xmax', 'label', 'nbins'])

bbZZ_vs_bbWW_BDT_compare_vars = {

	# "m_ll":PlotSpecs(name="m_ll", xmin=0., xmax=200., label="m_{ll} [GeV]", nbins=35),
	# "dR_ll":PlotSpecs(name="dR_ll", xmin=0.4, xmax=5.4, label="#Delta R_{ll}", nbins=25),
	# "m_bb_zoom":PlotSpecs(name="m_bb", xmin=20., xmax=200., label="m_{bb} [GeV]", nbins=30),
	# "dR_bb":PlotSpecs(name="dR_bb", xmin=0.4, xmax=5.4, label="#Delta R_{bb}", nbins=25),
	# "dPhi_ll_MET":PlotSpecs(name="dPhi_ll_MET", xmin=-3.5, xmax=3.5, label="#Delta#phi_{ll, E_{T}^{miss} }", nbins=35),
	# "MET":PlotSpecs(name="MET", xmin=0., xmax=350., label="E_{T}^{miss} [GeV]", nbins=35),
	# "HT2_ratio":PlotSpecs(name="HT2_ratio", xmin=0., xmax=1.2, label="H_{T}^{2} ratio  ", nbins=40),
	# "mlb_reco_zoom":PlotSpecs(name="mlb_reco", xmin=30., xmax=510., label="m_{lb}^{reco} [GeV]", nbins=12),
	# "mT2_HH_selBinning_fine":PlotSpecs(name="mT2_HH", xmin=50., xmax=400., label="m_{T2}(bb2l+MET) [GeV]", nbins=14), 

	# "n_untagged_jets":PlotSpecs(name="n_untagged_jets", xmin=0., xmax=20., label="n_{jets}(not b-tagged)", nbins=20),
	# "n_b_jets":PlotSpecs(name="n_b_jets", xmin=0., xmax=10., label="n_{jets}(b-tagged)", nbins=10),

	#new variables:

	#dphis where i only use dRs
	"dPhi_ll":PlotSpecs(name="dPhi_ll", xmin=-3.5, xmax=3.5, label="#Delta#phi_{ll}", nbins=35),
	"dPhi_bb":PlotSpecs(name="dPhi_bb", xmin=-3.5, xmax=3.5, label="#Delta#phi_{bb}", nbins=35),

	#pTs of the higgs candidates
	"pT_Hbb_cand":PlotSpecs(name="pT_Hbb_cand", xmin=0., xmax=800., label="p_{T}(bb) [GeV]", nbins=40),
	"pT_ll":PlotSpecs(name="pT_ll", xmin=0., xmax=800., label="p_{T}(ll) [GeV]", nbins=40),

	#phi of ETMiss
	"MET_phi":PlotSpecs(name="MET_phi", xmin=-3.5, xmax=3.5, label="E_{T}^{miss} (#phi)", nbins=35),

	#HH system
	"dPhi_HH":PlotSpecs(name="dPhi_HH", xmin=-3.5, xmax=3.5, label="#Delta#phi_{H,H }", nbins=35),

	#other event wide kinematic vars
	"sum_pT_ll_MET":PlotSpecs(name="sum_pT_ll_MET", xmin=0., xmax=1000., label="| p_{T}^{ll} + E_{T}^{miss} | [GeV]", nbins=50),
	"MET_significance":PlotSpecs(name="MET_significance", xmin=0., xmax=30., label="E_{T}^{miss}/#sqrt(H_{T})", nbins=15),
	"dzeta_85":PlotSpecs(name="dzeta_85", xmin=-500., xmax=500., label="D_{#zeta} [GeV]", nbins=50),
	
}

#TEMP OVERWRITE FOR POSTER PLOTS
common_sel_vars_poster = {

	"m_bb_zoom":PlotSpecs(name="m_bb", xmin=20., xmax=200., label="m_{bb} [GeV]", nbins=18),
	"dR_bb":PlotSpecs(name="dR_bb", xmin=0.4, xmax=5.4, label="#Delta R_{bb}", nbins=20),
	"mlb_reco_zoom":PlotSpecs(name="mlb_reco", xmin=30., xmax=510., label="m_{lb}^{reco} [GeV]", nbins=12),

	}

common_sel_vars = {
	

	#adding for BDT checks
	# "n_untagged_jets":PlotSpecs(name="n_untagged_jets", xmin=0., xmax=20., label="n_{jets}(not b-tagged)", nbins=20),
	# "n_b_jets":PlotSpecs(name="n_b_jets", xmin=0., xmax=10., label="n_{jets}(b-tagged)", nbins=10),

	"mT2_HH_selBinning":PlotSpecs(name="mT2_HH", xmin=75., xmax=400., label="m_{T2}(bb2l+MET) [GeV]", nbins=[ 75., 90., 105., 120., 135., 150., 200. ]), #wo bin with no signal

	#TODO COMMENT BACK IN 
	# #kinematic selections
	"m_bb_zoom":PlotSpecs(name="m_bb", xmin=20., xmax=200., label="m_{bb} [GeV]", nbins=30),
	"m_ll":PlotSpecs(name="m_ll", xmin=0., xmax=200., label="m_{ll} [GeV]", nbins=35),
	"dR_bb":PlotSpecs(name="dR_bb", xmin=0.4, xmax=5.4, label="#Delta R_{bb}", nbins=25),
	"dR_ll":PlotSpecs(name="dR_ll", xmin=0.4, xmax=5.4, label="#Delta R_{ll}", nbins=25),
	"dPhi_ll_MET":PlotSpecs(name="dPhi_ll_MET", xmin=-3.5, xmax=3.5, label="#Delta#phi_{ll, E_{T}^{miss} }", nbins=35),
	"HT2_ratio":PlotSpecs(name="HT2_ratio", xmin=0., xmax=1.2, label="H_{T}^{2} ratio  ", nbins=40),
	"mlb_reco":PlotSpecs(name="mlb_reco", xmin=0., xmax=1000., label="m_{lb}^{reco} [GeV]", nbins=50),
	"mlb_reco_zoom":PlotSpecs(name="mlb_reco", xmin=30., xmax=510., label="m_{lb}^{reco} [GeV]", nbins=12),
	
	# #not used in selection:
	# "MET":PlotSpecs(name="MET", xmin=0., xmax=350., label="E_{T}^{miss} [GeV]", nbins=35),
	# "dPhi_HH":PlotSpecs(name="dPhi_HH", xmin=-3.5, xmax=3.5, label="#Delta#phi_{H,H }", nbins=35),

	# #discriminant variable for cut-based analysis
	# "m_pseudo_HH_selBinning":PlotSpecs(name="m_pseudo_HH", xmin=100., xmax=1200., label="m_{pseudo}(bb2l+MET) [GeV]", nbins=[ 300., 400., 450., 500., 600., 700., 800., 1000., 1200. ]), #no signal below 200 Gev # 200., 250., bins cuas syst fit issue?
	# # "m_pseudo_HH_selBinning":PlotSpecs(name="m_pseudo_HH", xmin=100., xmax=1200., label="m_{pseudo}(bb2l+MET) [GeV]", nbins=[ 250., 300., 350., 400., 450., 500., 600., 700., 800., 1000., 1200. ]), #OLD has empty bins!
	# "m_pseudo_HH_100GevBins":PlotSpecs(name="m_pseudo_HH", xmin=350., xmax=1500., label="m_{pseudo}(bb2l+MET) [GeV]", nbins=15), 

	# #stransverse mass
	# "mT2_HH":PlotSpecs(name="mT2_HH", xmin=0., xmax=550., label="m_{T2}(bb2l+MET) [GeV]", nbins=11), #try fine binning first
	# "mT2_HH_125":PlotSpecs(name="mT2_HH_125", xmin=0., xmax=550., label="m_{T2}(bb2l+MET) [GeV]", nbins=11), #try fine binning first

	# "mT2_H_2l_MET":PlotSpecs(name="mT2_H_2l_MET", xmin=0., xmax=550., label="m_{T2}(H(ll+MET)) [GeV]", nbins=11), #try fine binning first

	

	# "mT2_HH_selBinning":PlotSpecs(name="mT2_HH", xmin=50., xmax=400., label="m_{T2}(bb2l+MET) [GeV]", nbins=7), #coarse and uniform
	# "mT2_HH_selBinning_fine":PlotSpecs(name="mT2_HH", xmin=50., xmax=400., label="m_{T2}(bb2l+MET) [GeV]", nbins=14), 
	# "mT2_HH_selBinning_finest":PlotSpecs(name="mT2_HH", xmin=50., xmax=400., label="m_{T2}(bb2l+MET) [GeV]", nbins=35), 
	
	# "mT2_HH_smeared_selBinning":PlotSpecs(name="mT2_HH_smeared", xmin=75., xmax=400., label="m_{T2}(bb2l+MET) smeared [GeV]", nbins=[ 75., 90., 105., 120., 135., 150., 200. ]), #wo bin with no signal
	# "mT2_HH_selBinning_SFOS_Z_peak":PlotSpecs(name="mT2_HH", xmin=75., xmax=400., label="m_{T2}(bb2l+MET) [GeV]", nbins=[ 75., 105., 120., 135., 150., 200. ]), #wo bin with no signal
	# "mT2_HH_selBinning":PlotSpecs(name="mT2_HH", xmin=75., xmax=400., label="m_{T2}(bb2l+MET) [GeV]", nbins=[ 75., 90., 105., 120., 135., 150., 200., 300., 400. ]), 
	# "mT2_HH_selBinning":PlotSpecs(name="mT2_HH", xmin=75., xmax=400., label="m_{T2}(bb2l+MET) [GeV]", nbins=[ 75., 90., 105., 120., 135., 150., 175., 200., 250., 300., 400. ]), 


	# try to separate bbWW/bbtautau
	# "pzeta_vis":PlotSpecs(name="pzeta_vis", xmin=0., xmax=1000., label="p_{#zeta}^{vis} [GeV]", nbins=50),
	# "pzeta_miss":PlotSpecs(name="pzeta_miss", xmin=0., xmax=1000., label="p_{#zeta}^{miss} [GeV]", nbins=50),
	# "dzeta_85":PlotSpecs(name="dzeta_85", xmin=-500., xmax=500., label="D_{#zeta} [GeV]", nbins=50),

}

compare_vars_bbWW_bbtautau ={

	# "MET":PlotSpecs(name="MET", xmin=0., xmax=350., label="E_{T}^{miss} [GeV]", nbins=35),
	
	# try to separate bbWW/bbtautau
	# "pzeta_vis":PlotSpecs(name="pzeta_vis", xmin=0., xmax=1000., label="p_{#zeta}^{vis} [GeV]", nbins=50),
	# "pzeta_miss":PlotSpecs(name="pzeta_miss", xmin=0., xmax=1000., label="p_{#zeta}^{miss} [GeV]", nbins=50),
	# "dzeta_60":PlotSpecs(name="dzeta_60", xmin=-500., xmax=500., label="D_{#zeta}(60) [GeV]", nbins=50),
	# "dzeta_65":PlotSpecs(name="dzeta_65", xmin=-500., xmax=500., label="D_{#zeta}(65) [GeV]", nbins=50),
	# "dzeta_70":PlotSpecs(name="dzeta_70", xmin=-500., xmax=500., label="D_{#zeta}(70) [GeV]", nbins=50),
	# "dzeta_75":PlotSpecs(name="dzeta_75", xmin=-500., xmax=500., label="D_{#zeta}(75) [GeV]", nbins=50),
	# "dzeta_80":PlotSpecs(name="dzeta_80", xmin=-500., xmax=500., label="D_{#zeta}(80) [GeV]", nbins=50),
	# "dzeta_85":PlotSpecs(name="dzeta_85", xmin=-500., xmax=500., label="D_{#zeta}(85) [GeV]", nbins=50),
	# "dzeta_90":PlotSpecs(name="dzeta_90", xmin=-500., xmax=500., label="D_{#zeta}(90) [GeV]", nbins=50),
	# "dzeta_95":PlotSpecs(name="dzeta_95", xmin=-500., xmax=500., label="D_{#zeta}(95) [GeV]", nbins=50),

	#try collineaer mass
	
	"m_collinear":PlotSpecs(name="m_collinear", xmin=0., xmax=500., label="m_{coll} [GeV]", nbins=50),
	"x_lep1_reco":PlotSpecs(name="x_lep1", xmin=0., xmax=1., label="x1 ", nbins=50),
	"x_lep2_reco":PlotSpecs(name="x_lep2", xmin=0., xmax=1., label="x2 ", nbins=50),
	
	#test the mT of the leptons
	# "mT_lep1":PlotSpecs(name="mT_lep1", xmin=0., xmax=200., label="m_{T}(lead lep) [GeV]", nbins=40),
	# "mT_lep2":PlotSpecs(name="mT_lep2", xmin=0., xmax=200., label="m_{T}(sublead lep) [GeV]", nbins=40),
	

}

compare_vars_bbWW_bbtautau_ttbar ={
	
	# "mT2_H_2l_MET":PlotSpecs(name="mT2_H_2l_MET", xmin=0., xmax=150., label="m_{T2}(H(ll+MET)) [GeV]", nbins=30), #try fine binning first

	# #m_pseudo binnings studies
	# "m_pseudo_HH_selBinning":PlotSpecs(name="m_pseudo_HH", xmin=100., xmax=1200., label="m_{pseudo}(bb2l+MET) [GeV]", nbins=[ 250., 300., 350., 400., 450., 500., 600., 700., 800., 1000., 1200. ]), #no signal below 200 Gev # 200., 250., bins cuas syst fit issue?
	# "m_pseudo_HH_fine":PlotSpecs(name="m_pseudo_HH", xmin=0., xmax=2000., label="m_{pseudo}(bb2l+MET) [GeV]", nbins=40), #no signal below 200 Gev # 200., 250., bins cuas syst fit issue?

	# "m_pseudo_HH_newBinning":PlotSpecs(name="m_pseudo_HH", xmin=350., xmax=1500., label="m_{pseudo}(bb2l+MET) [GeV]", nbins=[ 350., 400., 450., 500., 550., 600., 650., 700., 750., 800., 900., 1000., 1100., 1200., 1300., 1500. ]), #no signal below 200 Gev # 200., 250., bins cuas syst fit issue?
	# "m_pseudo_HH_50GevBins":PlotSpecs(name="m_pseudo_HH", xmin=350., xmax=1500., label="m_{pseudo}(bb2l+MET) [GeV]", nbins=30), #no signal below 200 Gev # 200., 250., bins cuas syst fit issue?
	# "m_pseudo_HH_100GevBins":PlotSpecs(name="m_pseudo_HH", xmin=350., xmax=1500., label="m_{pseudo}(bb2l+MET) [GeV]", nbins=15), #no signal below 200 Gev # 200., 250., bins cuas syst fit issue?

	# "mlb_reco_zoom":PlotSpecs(name="mlb_reco", xmin=30., xmax=510., label="m_{lb}^{reco} [GeV]", nbins=12),
	# "mlb_reco":PlotSpecs(name="mlb_reco", xmin=0., xmax=750., label="m_{lb}^{reco} [GeV]", nbins=50),

	#stransverse mass
	"mT2_HH":PlotSpecs(name="mT2_HH", xmin=0., xmax=600., label="m_{T2}(bb2l+MET) [GeV]", nbins=30), 
	"mT2_HH_zoom":PlotSpecs(name="mT2_HH", xmin=0., xmax=300., label="m_{T2}(bb2l+MET) [GeV]", nbins=30), 
	# "mT2_HH_125":PlotSpecs(name="mT2_HH_125", xmin=0., xmax=600., label="m_{T2}(bb2l+MET) [GeV]", nbins=30),#try fine binning first
}

compare_vars_bbWW_ttbar ={

	"mlb_reco_zoom":PlotSpecs(name="mlb_reco", xmin=30., xmax=510., label="m_{lb}^{reco} [GeV]", nbins=24),
	# "mlb_reco":PlotSpecs(name="mlb_reco", xmin=0., xmax=750., label="m_{lb}^{reco} [GeV]", nbins=50),
	# "MET":PlotSpecs(name="MET", xmin=0., xmax=350., label="E_{T}^{miss} [GeV]", nbins=35),
	
}

compare_vars_HH_ggH ={
	"MET":PlotSpecs(name="MET", xmin=0., xmax=350., label="E_{T}^{miss} [GeV]", nbins=35),
	"dR_bb":PlotSpecs(name="dR_bb", xmin=0.4, xmax=5.4, label="#Delta R_{bb}", nbins=25),
	"n_jets":PlotSpecs(name="n_jets", xmin=0., xmax=10., label="n_{jets}", nbins=10),
	"n_untagged_jets":PlotSpecs(name="n_untagged_jets", xmin=0., xmax=10., label="n_{jets}(untagged)", nbins=10),
	"n_b_jets":PlotSpecs(name="n_b_jets", xmin=0., xmax=10., label="n_{jets}(b-tagged)", nbins=10),
	"m_ll":PlotSpecs(name="m_ll", xmin=0., xmax=200., label="m_{ll} [GeV]", nbins=35),
	"m_bb_zoom":PlotSpecs(name="m_bb", xmin=20., xmax=200., label="m_{bb} [GeV]", nbins=30),
}

compare_x1 ={
	"x_lep1_reco":PlotSpecs(name="x_lep1", xmin=0., xmax=1., label="x1 ", nbins=50),
	"x_lep1_truth":PlotSpecs(name="x_lep1_truth", xmin=0., xmax=1., label="x1 ", nbins=50),
}

compare_x2 ={
	"x_lep2_reco":PlotSpecs(name="x_lep2", xmin=0., xmax=1., label="x2 ", nbins=50),
	"x_lep2_truth":PlotSpecs(name="x_lep2_truth", xmin=0., xmax=1., label="x2 ", nbins=50),
}

plots_2D ={
		#for 2D plots
	"mlb_reco_zoom":PlotSpecs(name="mlb_reco", xmin=0., xmax=550., label="m_{lb}^{reco} [GeV]", nbins=26),
	"mT2_HH":PlotSpecs(name="mT2_HH", xmin=0., xmax=550., label="m_{T2}(bb2l+MET) [GeV]", nbins=26),
}

#old plots used in the documentation
bbZZllvv_old_plots ={
	#corners of phase space for the bbZZ chapter:
	# high pT
	# "pT_ll":PlotSpecs(name="pT_ll", xmin=0., xmax=800., label="p_{T}(ZZ) [GeV]", nbins=40),
	# "pT_Hbb_cand":PlotSpecs(name="pT_Hbb_cand", xmin=0., xmax=800., label="p_{T}(bb) [GeV]", nbins=40),
	"pT_ll_selBinning":PlotSpecs(name="pT_ll", xmin=0., xmax=1000., label="p_{T}(ZZ) [GeV]", nbins=[40., 80., 120., 160., 200., 240., 280., 320., 360., 400., 500., 600., 700., 800., 900., ]),
	"pT_Hbb_cand_selBinning":PlotSpecs(name="pT_Hbb_cand", xmin=0., xmax=1000., label="p_{T}(bb)[GeV]", nbins=[40., 80., 120., 160., 200., 240., 280., 320., 360., 400., 500., 600., 700., 800., 900., ]),
	
	#untagged jets:
	"n_untagged_jets":PlotSpecs(name="n_untagged_jets", xmin=0., xmax=10., label="n_{jets}(untagged)", nbins=10),
	"pT_untagged_jets":PlotSpecs(name="pT_untagged_jets", xmin=0., xmax=500., label="p_{T}(untagged jets) [GeV]", nbins=10),
	"n_sel_untagged_jets":PlotSpecs(name="n_sel_untagged_jets", xmin=0., xmax=8., label="n_{jets}(untagged, p_{T} > 50 GeV)", nbins=8),

	#no longer used mass variables, just to keep for documentation purposes:
	# "mT_bbll_MET_sel":PlotSpecs(name="mT_bbll_MET", xmin=0., xmax=590., label="m_{T}(bbZZ) [GeV]", nbins=[0., 30., 60., 90., 120., 150., 180., 210., 270., 330., 390., 490.,]),
	# "m_pseudo_HH_selBinning":PlotSpecs(name="m_pseudo_HH", xmin=100., xmax=1200., label="m_{pseudo}(bb2l+MET) [GeV]", nbins=[ 300., 400., 450., 500., 600., 700., 800., 1000., 1200. ]),
	# "mT_pseudo_HH_selBinning":PlotSpecs(name="mT_pseudo_HH", xmin=100., xmax=800., label="m_{T}^{pseudo}(bbZZ) [GeV]", nbins=[100., 150., 200., 250., 300., 350., 400., 450., 500., 600., 700., 800. ]),
}

bbtautau_old_plots ={
#kinematic selections
	"m_bb_zoom":PlotSpecs(name="m_bb", xmin=20., xmax=200., label="m_{bb} [GeV]", nbins=30),
	"m_ll":PlotSpecs(name="m_ll", xmin=0., xmax=200., label="m_{ll} [GeV]", nbins=35),
	"dR_bb":PlotSpecs(name="dR_bb", xmin=0.4, xmax=5.4, label="#Delta R_{bb}", nbins=25),
	"dR_ll":PlotSpecs(name="dR_ll", xmin=0.4, xmax=5.4, label="#Delta R_{ll}", nbins=25),
	"MET":PlotSpecs(name="MET", xmin=0., xmax=350., label="E_{T}^{miss} [GeV]", nbins=35),
	"dPhi_ll_MET":PlotSpecs(name="dPhi_ll_MET", xmin=-3.5, xmax=3.5, label="#Delta#phi_{ll, E_{T}^{miss} }", nbins=35),
	"sum_pT_ll_MET":PlotSpecs(name="sum_pT_ll_MET", xmin=0., xmax=1000., label="| p_{T}^{ll} + E_{T}^{miss} | [GeV]", nbins=50),
	"HT2_ratio":PlotSpecs(name="HT2_ratio", xmin=0., xmax=1.2, label="H_{T}^{2} ratio  ", nbins=40),
	
}

compare_vars_gaus_for_smear = {
	# "Gaussian":PlotSpecs(name="Gaus_blur", xmin=-100., xmax=100., label="Gauss(5., 37)", nbins=100),
	"Gaussian":PlotSpecs(name="Gaus_blur", xmin=-5., xmax=5., label="Gauss(0., 0.66)", nbins=35),
}

compare_vars_met_smear = {
	"MET":PlotSpecs(name="MET", xmin=0., xmax=350., label="E_{T}^{miss} [GeV]", nbins=35),
	"MET_recalc":PlotSpecs(name="MET_recalc", xmin=0., xmax=350., label="E_{T}^{miss} [GeV]", nbins=35),
	# "MET_smeared":PlotSpecs(name="MET_smeared", xmin=0., xmax=350., label="E_{T}^{miss} [GeV]", nbins=35),
}

compare_vars_met_diff = {
	# "MET_diff_in_evt":PlotSpecs(name="MET_diff_in_evt", xmin=-200., xmax=1000., label="E_{T}^{miss} (smear) -  E_{T}^{miss}(orig) [GeV]", nbins=60),}
	"MET_diff_in_evt":PlotSpecs(name="MET_diff_in_evt", xmin=-200., xmax=200., label="E_{T}^{miss} (smear) -  E_{T}^{miss}(orig) [GeV]", nbins=35),}
compare_vars_met_x_diff ={
	"MET_x_diff_in_evt":PlotSpecs(name="MET_x_diff_in_evt", xmin=-200., xmax=200., label="E_{x}^{miss} (smear) -  E_{x}^{miss}(orig) [GeV]", nbins=35),}
compare_vars_met_y_diff ={
	"MET_y_diff_in_evt":PlotSpecs(name="MET_y_diff_in_evt", xmin=-200., xmax=200., label="E_{y}^{miss} (smear) -  E_{y}^{miss}(orig) [GeV]", nbins=35),
}
compare_vars_met_ratio ={
	"MET_ratio_in_evt":PlotSpecs(name="MET_ratio_in_evt", xmin=-5., xmax=5., label="E_{T}^{miss} (smear) /  E_{T}^{miss}(orig) [GeV]", nbins=35),
}
compare_vars_met_x_ratio ={
	"MET_x_ratio_in_evt":PlotSpecs(name="MET_x_ratio_in_evt", xmin=-5., xmax=5., label="E_{x}^{miss} (smear) /  E_{x}^{miss}(orig) [GeV]", nbins=35),
}
compare_vars_met_y_ratio ={
	"MET_y_ratio_in_evt":PlotSpecs(name="MET_y_ratio_in_evt", xmin=-5., xmax=5., label="E_{y}^{miss} (smear) /  E_{y}^{miss}(orig) [GeV]", nbins=35),
}

compare_vars_met_x_smear = {
	"MET_x":PlotSpecs(name="MET_x", xmin=-350., xmax=350., label="E_{x}^{miss} [GeV]", nbins=35),
	"MET_x_smeared":PlotSpecs(name="MET_x_smeared", xmin=-350., xmax=350., label="E_{x}^{miss} [GeV]", nbins=35),
}

compare_vars_met_y_smear = {
	"MET_y":PlotSpecs(name="MET_y", xmin=-350., xmax=350., label="E_{y}^{miss} [GeV]", nbins=35),
	"MET_y_smeared":PlotSpecs(name="MET_y_smeared", xmin=-350., xmax=350., label="E_{y}^{miss} [GeV]", nbins=35),
}

compare_vars_met_res_smeared = {
	"Baseline":PlotSpecs(name="MET_res", xmin=-1., xmax=1., label="(E_{T}^{miss}(reco) - E_{T}^{miss}(truth))/E_{T}^{miss}(truth)", nbins=40),
	"Smeared":PlotSpecs(name="MET_res_smear", xmin=-1., xmax=1., label="(E_{T}^{miss}(reco) - E_{T}^{miss}(truth))/E_{T}^{miss}(truth)", nbins=40),
	# "Baseline":PlotSpecs(name="MET_res", xmin=-2., xmax=78., label="(E_{T}^{miss}(reco) - E_{T}^{miss}(truth))/E_{T}^{miss}(truth)", nbins=80),
	# "Smeared":PlotSpecs(name="MET_res_smear", xmin=-2., xmax=78., label="(E_{T}^{miss}(reco) - E_{T}^{miss}(truth))/E_{T}^{miss}(truth)", nbins=80),

}

compare_vars_met_res_abs_smeared = {
	"Baseline":PlotSpecs(name="MET_res_abs", xmin=-75., xmax=75., label="E_{T}^{miss}(reco) - E_{T}^{miss}(truth)", nbins=50),
	"Smeared":PlotSpecs(name="MET_res_abs_smear", xmin=-75., xmax=75., label="E_{T}^{miss}(reco) - E_{T}^{miss}(truth)", nbins=50),

}

compare_vars_met_x_res_smeared = {
	"Baseline":PlotSpecs(name="MET_x_res", xmin=-1., xmax=1., label="(E_{x}^{miss}(reco) - E_{x}^{miss}(truth))/E_{x}^{miss}(truth)", nbins=40),
	"Smeared":PlotSpecs(name="MET_x_res_smear", xmin=-1., xmax=1., label="(E_{x}^{miss}(reco) - E_{x}^{miss}(truth))/E_{x}^{miss}(truth)", nbins=40),

}

compare_vars_dPhiZMET_smeared = {
	"Baseline":PlotSpecs(name="dPhi_ll_MET", xmin=-3.5, xmax=3.5, label="#Delta#phi_{ll, E_{T}^{miss} }", nbins=35),
	"Smeared":PlotSpecs(name="dPhi_ll_MET_smeared", xmin=-3.5, xmax=3.5, label="#Delta#phi_{ll, E_{T}^{miss} }", nbins=35),

}

compare_vars_HT2ratio_smeared = {
	"Baseline":PlotSpecs(name="HT2_ratio", xmin=0., xmax=1.2, label="H_{T}^{2} ratio  ", nbins=40),
	"Smeared":PlotSpecs(name="HT2_ratio_smeared", xmin=0., xmax=1.2, label="H_{T}^{2} ratio  ", nbins=40),
}

compare_vars_mT2_smeared = {
	"Baseline":PlotSpecs(name="mT2_HH", xmin=75., xmax=400., label="m_{T2}(bb2l+MET) [GeV]", nbins=[ 75., 90., 105., 120., 135., 150., 200. ]),
	"Smeared":PlotSpecs(name="mT2_HH_smeared", xmin=75., xmax=400., label="m_{T2}(bb2l+MET) [GeV]", nbins=[ 75., 90., 105., 120., 135., 150., 200. ]),
}

compare_vars_input_check = {
	"m_ll_diff":PlotSpecs(name="m_ll_diff", xmin=-0.01, xmax=0.01, label="Diff in m_ll", nbins=40),
	"m_bb_diff":PlotSpecs(name="m_bb_diff",xmin=-0.01, xmax=0.01, label="Diff in m_bb", nbins=40),
	"px_bb_diff":PlotSpecs(name="px_bb_diff",xmin=-0.01, xmax=0.01, label="Diff in px_bb", nbins=40),
	"px_ll_diff":PlotSpecs(name="px_ll_diff",xmin=-0.01, xmax=0.01, label="Diff in pll_bb", nbins=40),
}

plot_list_2D= {
	"MET":PlotSpecs(name="MET", xmin=0., xmax=350., label="E_{T}^{miss} [GeV]", nbins=35),
	"MET_recalc":PlotSpecs(name="MET_recalc", xmin=0., xmax=350., label="E_{T}^{miss} [GeV]", nbins=35),
}


# old vars:
# "pT_ll":PlotSpecs(name="pT_ll", xmin=0., xmax=200., label="p_{T}^{ll} [GeV]", nbins=35),
	# 
	# "HT2_Hemu_plus_Hbb":PlotSpecs(name="HT2_Hemu_plus_Hbb", xmin=0., xmax=1000., label="H_{T}^{2}  [GeV]", nbins=50),
	# "HT2_Hemu_plus_Hbb":PlotSpecs(name="HT2_Hemu_plus_Hbb", xmin=0., xmax=1000., label="H_{T}^{2}  [GeV]", nbins=50),

		#for ttbar CR:
	# "n_OS_pair_singlebin":PlotSpecs(name="n_OS_emu_pairs", xmin=0., xmax=10., label="single bin", nbins=1),

		# "MET_phi":PlotSpecs(name="MET_phi", xmin=-3.5, xmax=3.5, label="E_{T}^{miss} (#phi)", nbins=35),
	
	# 
	# "MET_significance":PlotSpecs(name="MET_significance", xmin=0., xmax=30., label="E_{T}^{miss}/#sqrt(H_{T})", nbins=15),

	# 
	#

	#
	# "dPhi_ll":PlotSpecs(name="dPhi_ll", xmin=-3.5, xmax=3.5, label="#Delta#phi_{ll}", nbins=35),
	# "dPhi_bb":PlotSpecs(name="dPhi_bb", xmin=-3.5, xmax=3.5, label="#Delta#phi_{bb}", nbins=35),

	# 
	# "n_b_jets":PlotSpecs(name="n_b_jets", xmin=0., xmax=10., label="n_{jets}(b-tagged)", nbins=10),
	# 
	# 

		# "mT_pseudo_HH":PlotSpecs(name="mT_pseudo_HH", xmin=200., xmax=1400., label="m_{T}^{pseudo}(bb#tau#tau) [GeV]", nbins=60),
	# "mT_pseudo_HH_selBinning":PlotSpecs(name="mT_pseudo_HH", xmin=100., xmax=800., label="m_{T}^{pseudo}(bb#tau#tau) [GeV]", nbins=[100., 150., 200., 250., 300., 350., 400., 450., 500., 600., 700., 800. ]),

	# transverse mass variables
	# "mT_bbll_MET":PlotSpecs(name="mT_bbll_MET", xmin=0., xmax=600., label="m_{T}(bbZZ) [GeV]", nbins=20),
	# 
	
# "m_pseudo_HH_selBinning":PlotSpecs(name="m_pseudo_HH", xmin=250., xmax=800., label="m_{pseudo}(bb#tau#tau) [GeV]", nbins=[ 250., 300., 350., 400., 450., 500., 600., 700., 800., 1000. ]),

	#discriminants
	# "m_pseudo_HH":PlotSpecs(name="m_pseudo_HH", xmin=50., xmax=1200., label="m_{pseudo}(bbWW) [GeV]", nbins=30),
	
	# "m_pseudo_HH_smeared_selBinning":PlotSpecs(name="m_pseudo_HH_smeared", xmin=100., xmax=1200., label="m_{pseudo}(bbWW) [GeV]", nbins=[ 300., 350., 400., 450., 500., 600., 700., 800., 1000., 1200. ]), #no signal below 200 Gev # 200., 250., bins cuas syst fit issue?
	

	# "m_pseudo_HH_selBinning":PlotSpecs(name="m_pseudo_HH", xmin=100., xmax=1200., label="m_{pseudo}(bbWW) [GeV]", nbins=[100., 150., 200., 250., 300., 350., 400., 450., 500., 600., 700., 800., 1000., 1200. ]),
	# "mT_pseudo_HH":PlotSpecs(name="mT_pseudo_HH", xmin=200., xmax=1400., label="m_{T}^{pseudo}(bbZZ) [GeV]", nbins=60),
	# 

	# kinematic variables to define corners of phase space

	
	#jet vetos
	
	#unused variables:
		# "n_jets":PlotSpecs(name="n_jets", xmin=0., xmax=10., label="n_{jets}", nbins=10),

	# other angles between the two Higgs candidates:
	# "dR_Hbb_HZZ_cands":PlotSpecs(name="dR_Hbb_HZZ_cands", xmin=0.4, xmax=5.4, label="#Delta R_{HH}", nbins=25),
	# "dEta_Hbb_HZZ_cands":PlotSpecs(name="dEta_Hbb_HZZ_cands", xmin=0., xmax=5., label="#Delta #eta_{HH}", nbins=25),

	#added new variables of lb system, which might help top suppression (following eg. atlas top mass measurement in di-lepton channel)
	
	# "mlb_reco_MET":PlotSpecs(name="mlb_reco_MET", xmin=0., xmax=1000., label="m_{lb}^{reco} (w. MET) [GeV]", nbins=50),
	# "dR_lb":PlotSpecs(name="dR_lb", xmin=0.4, xmax=5.4, label="#Delta R_{lb}", nbins=25),
