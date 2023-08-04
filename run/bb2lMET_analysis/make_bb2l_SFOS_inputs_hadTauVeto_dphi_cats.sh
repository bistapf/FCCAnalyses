#!/bin/bash
INDIR="/eos/user/b/bistapf/FCCAnalysesFiles/HH_bb2lMET_analysis/preSel_SFOS_fullStat/"
ANANAME="bb2l_SFOS_noZ"
CATNAME="tauveto_dphi_cats"
CAT1="bb2l_SFOS_noZ_low_dphi_tauveto"
CAT2="bb2l_SFOS_noZ_high_dphi_tauveto"
SEL_LVL="sel9_mlb_150"
OUTDIR="./Plots_bb2lMET_SFOS_noZ/"
BASENAME="${ANANAME}_histograms_mT2_HH_selBinning_${SEL_LVL}" #using mT2 stransverse mass
# BASENAME="${ANANAME}_histograms_m_pseudo_HH_selBinning_${SEL_LVL}" #using mpseudo



python make_WS_inputs.py -i $INDIR -o $OUTDIR  --signalCat $ANANAME --extraCut $CAT1
python make_WS_inputs.py -i $INDIR -o $OUTDIR  --signalCat $ANANAME --extraCut $CAT2

FILE1="${BASENAME}_${CAT1}.root"
FILE2="${BASENAME}_${CAT2}.root"
MERGEDFILE="${BASENAME}_${CATNAME}.root"
FILEDIR="${OUTDIR}/WS_Input/"

cd $FILEDIR

hadd -f $MERGEDFILE $FILE1 $FILE2
