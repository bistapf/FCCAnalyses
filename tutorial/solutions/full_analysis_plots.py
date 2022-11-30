import ROOT

# global parameters
intLumi        = 30.0e+06 #in pb-1
ana_tex        = "pp-collisions"
delphesVersion = "3.4.2"
energy         = 100 
collider       = "FCC-hh"
inputDir       = "outputs/"
formats        = ['png']
yaxis          = ['lin','log']
stacksig       = ['nostack']
outdir         = 'plots'

variables = ['m_bb_leading', 'm_yy', 'n_b_jets', 'n_photons']

###Dictonnary with the analysis name as a key, and the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
selections = {}
selections['bbyy']   = ["sel0", "sel1"]

extralabel = {}
extralabel['sel0'] = "Selection: n_{y} > 1"
extralabel['sel1'] = "Selection: n_{y} > 1 && n_{b-jets} > 1"

colors = {}
colors['bbyy'] = ROOT.kBlue+2
colors['yy+jets'] = ROOT.kGreen+2

plots = {}
plots['bbyy'] = {'signal':{'bbyy':['fastsim_tutorial_output']},
               'backgrounds':{
               				'yy+jets':['bkg_evts'],
                             }
           }


legend = {}
legend['bbyy'] = 'bbyy signal'
legend['yy+jets'] = 'yy+jets bkg'
