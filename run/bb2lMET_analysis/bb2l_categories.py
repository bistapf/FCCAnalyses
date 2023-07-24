bb2l_cats ={
	#cutname:cut string (as used as extra cut in draw_plots)
	"bb2l_DFOS_low_dphi":"abs(dPhi_ll_MET[0]) < 1.2",
	"bb2l_SFOS_noZ_low_dphi":"abs(dPhi_ll_MET[0]) < 1.2",
	"bb2l_DFOS_high_dphi":"abs(dPhi_ll_MET[0]) > 1.2 && abs(dPhi_ll_MET[0]) < 2.0",
	"bb2l_SFOS_noZ_high_dphi":"abs(dPhi_ll_MET[0]) > 1.2 && abs(dPhi_ll_MET[0]) < 2.0",
	"bb2l_w_MET_ge_50":"MET[0] > 50.",
	"bb2l_w_MET_ge_25":"MET[0] > 25.",
	"bb2l_w_dRll_le_18":"dR_ll[0] < 1.8",
	"bb2l_w_mlb_ge_100":"mlb_reco[0] > 100.",
	"bb2l_w_mll_on_Z":"m_ll[0] > 80 && m_ll[0] < 101.",
	#for WS for combination
	"bb2l_DFOS_low_dphi_tauveto":"abs(dPhi_ll_MET[0]) < 1.2 && n_tau_jets_iso == 0",
	"bb2l_DFOS_high_dphi_tauveto":"abs(dPhi_ll_MET[0]) > 1.2 && abs(dPhi_ll_MET[0]) < 2.0 && n_tau_jets_iso == 0",
	#same for SFOS, no Z:
	"bb2l_SFOS_noZ_low_dphi_tauveto":"abs(dPhi_ll_MET[0]) < 1.2 && n_tau_jets_iso == 0",
	"bb2l_SFOS_noZ_high_dphi_tauveto":"abs(dPhi_ll_MET[0]) > 1.2 && abs(dPhi_ll_MET[0]) < 2.0 && n_tau_jets_iso == 0",
	#use smeared dphi
	"bb2l_DFOS_low_dphi_smeared":"abs(dPhi_ll_MET_smeared) < 1.2",
	"bb2l_DFOS_high_dphi_smeared":"abs(dPhi_ll_MET_smeared) > 1.2 && abs(dPhi_ll_MET_smeared) < 2.0 ",
}