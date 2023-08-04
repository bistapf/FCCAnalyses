import ROOT

# global parameters
intLumi        = 30e+06 #in pb-1
ana_tex        = 'bb2l+MET'
delphesVersion = '3.4.2'
energy         = 240.0
collider       = 'FCC-hh'
inputDir       = '/eos/user/b/bistapf/FCChh_EvtGen/bb2lMET_ntuples/SFOS/noZ/'
formats        = ['png']
yaxis          = ['lin','log']
stacksig       = ['stack','nostack']
outdir         = '/eos/user/b/bistapf/FCChh_EvtGen/bb2lMET_ntuples/SFOS/noZ/plots/'
plotStatUnc    = True

variables = ['mz','mz_zoom','leptonic_recoil_m','leptonic_recoil_m_zoom','leptonic_recoil_m_zoom2']
# rebin = [1, 1, 1, 1, 2] # uniform rebin per variable (optional)

###Dictonnary with the analysis name as a key, and the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
selections = {}
selections['bb2lMET_presel']   = ["sel2_bJets_medium"]

extralabel = {}
extralabel['sel2_bJets_medium'] = "Pre-selection"

colors = {}
colors['ZH'] = ROOT.kRed
colors['WW'] = ROOT.kBlue+1
colors['ZZ'] = ROOT.kGreen+2
colors['VV'] = ROOT.kGreen+3

plots = {}
plots['bb2lMET_presel'] = {'signal':{'hhbbww':['pwp8_pp_hh_lambda100_5f_hhbbww']},
               # 'backgrounds':{'WW':['p8_ee_WW_ecm240'],
               #                'ZZ':['p8_ee_ZZ_ecm240']}
           }

legend = {}
legend['hhbbww'] = 'bbWW'

# fccanalysis plots analysis_plots.py