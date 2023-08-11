#!/usr/bin/env python
# Author: C.Caputo (UCLouvain)

import CombineHarvester.CombineTools.ch as ch

import ROOT as R
import glob
import os

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--reg", type=str, required=True, choices=['sb', 'c'], help="region in mbb" )
parser.add_argument("--tag", type=str, required=True, help="Datacard name tag" )
parser.add_argument("--input", type=str, required=True, help="Root files input path" )
parser.add_argument("--scen", type=str, required=True, choices=['I', 'II', 'III'],help="Scenario (I, II, III)")
args = parser.parse_args()

cb = ch.CombineHarvester()

reg  = args.reg
tag   = args.tag
input = args.input
scen = args.scen

####DEF: syst for different scenarios##
systScenI = {"lumi" : 0.005,
             "btag" : 0.005,
             "sigxs": 0.005,
             "phid" : 0.005} 
systScenII = {"lumi" : 0.01,
             "btag" : 0.01,
             "sigxs": 0.01,
             "phid" : 0.01}
systScenIII = {"lumi" : 0.02,
             "btag" : 0.02,
             "sigxs": 0.02,
             "phid" : 0.02}
           
syst_dict = {"I"  : systScenI,
             "II" : systScenII,
             "III": systScenIII
             }

auxiliaries  = os.environ['CMSSW_BASE'] + '/src/HiggsAnalysis/CombinedLimit/HH_FCChh_newCard_2023'
aux_shapes   = auxiliaries +'/{inputFolder}'.format(inputFolder=input)

print auxiliaries
print aux_shapes


chns = ['great350_high_purity', 'great350_medium_purity', 'small350_high_purity', 'small350_medium_purity']

print(chns)


bkg_procs = {
  'great350_high_purity'   : ['mgg_mgp8_pp_tth01j_5f_haa', 'mgg_mgp8_pp_h012j_5f_haa', 'mgg_mgp8_pp_jjaa_5f','mgg_mgp8_pp_jja_5f', 'mgg_mgp8_pp_vh012j_5f_haa', 'mgg_mgp8_pp_vbf_h01j_5f_haa'],
  'great350_medium_purity'   : ['mgg_mgp8_pp_tth01j_5f_haa', 'mgg_mgp8_pp_h012j_5f_haa', 'mgg_mgp8_pp_jjaa_5f', 'mgg_mgp8_pp_jja_5f','mgg_mgp8_pp_vh012j_5f_haa', 'mgg_mgp8_pp_vbf_h01j_5f_haa'],
  'small350_high_purity'   : ['mgg_mgp8_pp_tth01j_5f_haa', 'mgg_mgp8_pp_h012j_5f_haa', 'mgg_mgp8_pp_jjaa_5f','mgg_mgp8_pp_jja_5f', 'mgg_mgp8_pp_vh012j_5f_haa', 'mgg_mgp8_pp_vbf_h01j_5f_haa'],
  'small350_medium_purity'   : ['mgg_mgp8_pp_tth01j_5f_haa', 'mgg_mgp8_pp_h012j_5f_haa', 'mgg_mgp8_pp_jjaa_5f', 'mgg_mgp8_pp_jja_5f','mgg_mgp8_pp_vh012j_5f_haa', 'mgg_mgp8_pp_vbf_h01j_5f_haa']
}

sig_procs = ['mgg_pwp8_pp_hh_lambda100_5f_hhbbaa', 'mgg_pwp8_pp_hh_lambda240_5f_hhbbaa', 'mgg_pwp8_pp_hh_lambda300_5f_hhbbaa']



cats = {
  'great350_medium_purity' : [
    (0, 'great350_medium_purity'),
  ],
  'great350_high_purity' : [
    (0, 'great350_high_purity'),
  ],
  'small350_medium_purity' : [
    (0, 'small350_medium_purity'),
  ],
  'small350_high_purity' : [
    (0, 'small350_high_purity'),
  ]
}

print(cats)
print '>> Creating processes and observations...'


for chn in chns:
    cb.AddObservations(  ['*'],  ['HHbbgg'], ['100TeV'], [chn],                 cats[chn]      )
    cb.AddProcesses(     ['*'],  ['HHbbgg'], ['100TeV'], [chn], bkg_procs[chn], cats[chn], False  )
    cb.AddProcesses(     [''], ['HHbbgg'], ['100TeV'], [chn], sig_procs,      cats[chn], True   )#mod 125



print '>> Adding systematic uncertainties...'
signal = cb.cp().signals().process_set()

MC_Backgrouds = ['mgg_mgp8_pp_tth01j_5f_haa', 'mgg_mgp8_pp_h012j_5f_haa', 'mgg_mgp8_pp_jjaa_5f', 'mgg_mgp8_pp_jja_5f','mgg_mgp8_pp_vh012j_5f_haa', 'mgg_mgp8_pp_vbf_h01j_5f_haa']
 
cb.cp().process(signal+MC_Backgrouds).AddSyst(cb, "lumi", "lnN", ch.SystMap()([1.+syst_dict[scen]["lumi"],1.-syst_dict[scen]["lumi"]]))
cb.cp().process(signal+MC_Backgrouds).AddSyst(cb, "phid", "lnN", ch.SystMap()([1.+syst_dict[scen]["phid"],1.-syst_dict[scen]["phid"]]))
cb.cp().process(signal+MC_Backgrouds).AddSyst(cb, "btag", "lnN", ch.SystMap()([1.+syst_dict[scen]["btag"],1-syst_dict[scen]["btag"]]))
cb.cp().process(signal).AddSyst(cb, "sigxs", "lnN", ch.SystMap()([1.+syst_dict[scen]["sigxs"],1-syst_dict[scen]["sigxs"]]))



print '>> Extracting histograms from input root files...'
for chn in chns:
    file = aux_shapes + "/" + chn + "_"+reg+".root"
    cb.cp().channel([chn]).era(['100TeV']).backgrounds().ExtractShapes(
        file, '$PROCESS', '$PROCESS_$SYSTEMATIC')
    cb.cp().channel([chn]).era(['100TeV']).signals().ExtractShapes(
        file, '$PROCESS$MASS', '$PROCESS$MASS_$SYSTEMATIC')

print '>> Setting standardised bin names...'
ch.SetStandardBinNames(cb)

writer = ch.CardWriter('LIMITS/$TAG/$ANALYSIS_$CHANNEL_$BINID_$ERA.txt',
                       'LIMITS/$TAG/$ANALYSIS_$CHANNEL.input.root')

print(writer)

writer.SetVerbosity(2)
writer.WriteCards('{}/{}/{}'.format(tag,scen,reg), cb) ## the first argument is the $TAG
# for chn in chns: writer.WriteCards(chn,cb.cp().channel([chn]))
#HHbbtautau_tau_0_13TeV
#for chn in chns:
#     with open("./LIMITS/"+tag+"/HHbbtautau_"+chn+"_0_14TeV.txt",'a') as f:
#          f.write("* autoMCStats 0  1  1")

print '>> Done!'
#for chn in chns:
##if()
#     #with open("./LIMITS/"+tag+"/"+reg+"/"+str(chns[0])+"_"+str(chns[0])+"_0_13TeV.txt",'a') as f:
#    print(chn)
#    with open('LIMITS/'+tag+'/'+reg+'/HHbbgg_'+chn+'_0_100TeV.txt', 'a') as f:
#          f.write("Signal_rateParam rateParam HHbbgg_"+chn+"_0_100TeV mgg_pwp8_pp_hh_lambda100_5f_hhbbaa 15.000\n")
#          f.write("Signal_rateParam rateParam HHbbgg_"+chn+"_0_100TeV mgg_pwp8_pp_hh_lambda240_5f_hhbbaa 15.000\n")
#          f.write("Signal_rateParam rateParam HHbbgg_"+chn+"_0_100TeV mgg_pwp8_pp_hh_lambda300_5f_hhbbaa 15.000\n")
#          f.write(" ")
print '>> Done!'
