cut_list_bb2lmet_noZ = {
			"sel1_lepton_pair":"n_OS_ll_pairs > 0", 
			"sel2_bJets":"n_b_jets_medium > 1", 
			"sel3_mbb":"m_bb[0] > 85 && m_bb[0] < 150",
			"sel4_dRbb":"dR_bb[0] < 2.0", 
			"sel5_mll":"m_ll[0] > 10 && m_ll[0] < 80", 
			"sel6_dRll":"dR_ll[0] < 1.8", 
			"sel7_dphiZMET_12":"abs(dPhi_ll_MET[0]) < 2.0", 
			"sel8_HT2_ratio":"HT2_ratio[0] > 0.8", 
			"sel9_mlb_150":"mlb_reco[0] > 150.", 
}

cut_names_bbZZllvv = {
			"sel1_lepton_pair":">= 1 SFOS lepton pair", 
			"sel2_bJets":">= 2 b-jets", 
			"sel3_mbb":"85 < m_bb < 150 GeV",
			"sel4_dRbb":"dR_bb < 2", 
			"sel5_mll":"80 < m_ll < 101 GeV", 
			"sel6_dRll":"dR_ll < 1.8", 
			"sel7_dphiZMET_12":"|dPhi_ll_MET| < 1.2", 
			"sel8_HT2_ratio":"HT2_ratio > 0.8", 
			"sel9_mlb_150":"mlb_reco > 150 GeV", 
			"sel10_MET_200":"ETmiss < 200 GeV", 
}


