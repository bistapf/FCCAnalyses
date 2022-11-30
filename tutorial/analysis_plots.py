import ROOT

# global parameters
intLumi        = 30.0e+06 #in pb-1
ana_tex        = "pp-collisions"
delphesVersion = "3.4.2"
energy         = 100 
collider       = "FCC-hh"
inputDir       = "outputs/"
formats        = ['png','pdf']
yaxis          = ['lin','log']
stacksig       = ['stack','nostack']
outdir         = 'plots'

variables = ['m_bb_leading',]

###Dictonnary with the analysis name as a key, and the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
selections = {}
selections['bbyy']   = ["sel0"]

extralabel = {}
extralabel['sel0'] = "Selection: n_{b-jets} > 1"

colors = {}
colors['bbyy'] = ROOT.kBlue+2
# colors['ZZ'] = ROOT.kGreen+2
# colors['VV'] = ROOT.kGreen+3

plots = {}
plots['bbyy'] = {'signal':{'bbyy':['fastsim_tutorial_output']},
               'backgrounds':{
               				'bbyy':['fastsim_tutorial_output'],
                             }
           }


legend = {}
legend['bbyy'] = 'bbyy'
