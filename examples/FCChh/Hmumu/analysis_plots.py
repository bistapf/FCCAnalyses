import ROOT

# global parameters
intLumi        = 30e+06 #in pb-1
ana_tex        = 'pp #rightarrow H #rightarrow #mu#mu analysis '
delphesVersion = '3.4.2'
energy         = 100
collider       = 'FCC-hh'
inputDir       = '/eos/experiment/fcc/hh/analysis_ntuples/fcc_v06/II/Hmumu_analysis/final/'
formats        = ['png']
# formats        = ['png','pdf']
yaxis          = ['log']
# yaxis          = ['lin','log']
stacksig       = ['stack']
# stacksig       = ['stack','nostack']
outdir         = './plots_Hmumu/'
# outdir         = '/eos/user/b/bistapf/FCChh_SingleHAnalyses/Hmumu'
plotStatUnc    = True

variables = ['m_mumu','m_mumu_zoom', 'pT_mumu', 'pT_muplus', 'pT_muminus', 'pT_mumu_full', 'm_mumu_1bin']

# rebin = [1, 1, 1, 1, 2] # uniform rebin per variable (optional)

### Dictionary with the analysis name as a key, and the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
selections = {}
selections['Hmumu_analysis']   = ["sel1_mumupair", "sel2_mH","sel3_pTH50", "sel3_pTH100", "sel3_pTH200", "sel3_pTH300", "sel3_pTH400", "sel3_pTH500"]

extralabel = {}
extralabel['sel1_mumupair'] = "Pre-selected events"
extralabel['sel2_mH'] = "Selected events"
extralabel['sel3_pTH50'] = "Sel. evts & p_{T}(#mu#mu)} > 50 GeV"
extralabel['sel3_pTH100'] = "Sel. evts & p_{T}(#mu#mu)} > 100 GeV"
extralabel['sel3_pTH200'] = "Sel. evts & p_{T}(#mu#mu)} > 200 GeV"
extralabel['sel3_pTH300'] = "Sel. evts & p_{T}(#mu#mu)} > 300 GeV"
extralabel['sel3_pTH400'] = "Sel. evts & p_{T}(#mu#mu)} > 400 GeV"
extralabel['sel3_pTH500'] = "Sel. evts & p_{T}(#mu#mu)} > 500 GeV"

colors = {}
colors['ggH_mumu_signal'] = ROOT.kRed
colors['mumu_cont'] = ROOT.kBlue

plots = {}
plots['Hmumu_analysis'] = {
                            'signal':{'ggH_mumu_signal':[ 'mgp8_pp_h012j_5f_hmumu']},
                            'backgrounds':{'mumu_cont':[ 'mgp8_pp_mumu012j_mhcut_5f_HT_0_100', 
                                                         'mgp8_pp_mumu012j_mhcut_5f_HT_100_300',
                                                         'mgp8_pp_mumu012j_mhcut_5f_HT_300_500',
                                                         'mgp8_pp_mumu012j_mhcut_5f_HT_500_700',
                                                         'mgp8_pp_mumu012j_mhcut_5f_HT_700_900',
                                                         'mgp8_pp_mumu012j_mhcut_5f_HT_900_1100',
                                                         'mgp8_pp_mumu012j_mhcut_5f_HT_1100_100000',
                                                        ]},
           }

legend = {}
legend['ggH_mumu_signal'] = 'Hmumu'
legend['mumu_cont'] = 'bkg'