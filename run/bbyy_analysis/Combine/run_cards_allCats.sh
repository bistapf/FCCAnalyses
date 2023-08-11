#!/bin/bash 
#bbtautau or bbgg or bbbb or ALL
channel=$1
#name of the dir to put limits
folder=$2 

echo $channel
if [ $channel = "bbgg" ] || [ $channel = "ALL" ]
then

    SCENARIOS=('I' 'II' 'III')
 
    for scen in "${SCENARIOS[@]}"
    do
        python card_maker_allCats.py --input input_files --tag $folder --reg sb --scen "$scen"
        python card_maker_allCats.py --input input_files --tag $folder --reg c --scen "$scen"
        cd LIMITS/$folder/$scen
        combineCards.py ./sb/HHbbgg_small350_medium_purity_0_100TeV.txt ./c/HHbbgg_small350_medium_purity_0_100TeV.txt > small350_medium_purity.txt
        combineCards.py ./sb/HHbbgg_small350_high_purity_0_100TeV.txt ./c/HHbbgg_small350_high_purity_0_100TeV.txt > small350_high_purity.txt
        combineCards.py small350_medium_purity.txt small350_high_purity.txt > small350_combine.txt
  
        combineCards.py ./sb/HHbbgg_great350_medium_purity_0_100TeV.txt ./c/HHbbgg_great350_medium_purity_0_100TeV.txt > great350_medium_purity.txt
        combineCards.py ./sb/HHbbgg_great350_high_purity_0_100TeV.txt ./c/HHbbgg_great350_high_purity_0_100TeV.txt > great350_high_purity.txt
        combineCards.py great350_medium_purity.txt great350_high_purity.txt > great350_combine.txt
     
        combineCards.py great350_combine.txt small350_combine.txt > combine_all.txt
        text2workspace.py combine_all.txt -P HiggsAnalysis.CombinedLimit.HHModel:HHdefault --mass=125 
        
        combine -M MultiDimFit combine_all.root --verbose 1 --algo grid --points=200 -P kl --floatOtherPOIs=0 --setParameterRanges kl=0.8,1.5 --cl=0.68 --setParameters r=1,r_gghh=1,r_qqhh=1,CV=1,C2V=3,kt=1 --robustFit 1 -t -1 --fastScan -n fastScan
        #plot1DScan.py higgsCombinefastScan.MultiDimFit.mH120.root --POI kl --output fastscan 
        
        combine -M MultiDimFit combine_all.root --verbose 1 --algo grid --points=200 -P kl --floatOtherPOIs=0 --setParameterRanges kl=0.8,1.5 --cl=0.68 --setParameters r=1,r_gghh=1,r_qqhh=1,CV=1,C2V=3,kt=1 --robustFit 1 -t -1
        #plot1DScan.py higgsCombineTest.MultiDimFit.mH120.root --POI kl --output scan 
        cd -
    done
    cd LIMITS/$folder/
    plot1DScan.py ./I/higgsCombinefastScan.MultiDimFit.mH120.root --POI kl --others ./I/higgsCombineTest.MultiDimFit.mH120.root:scenI:4 ./II/higgsCombineTest.MultiDimFit.mH120.root:scenII:3 ./III/higgsCombineTest.MultiDimFit.mH120.root:scenIII:6 --main-label onlystat --logo FCC-hh --logo-sub "Work in progress" --y-max 15


    #combine -M AsymptoticLimits combine_all.root --run blind -m 125 > output_Asym_Lim.txt
    #combine -M Significance combine_all.root -t -1 --expectSignal=1  > output_Sig.txt
    #combineTool.py -M Impacts -d combine_all.root -m 125 -t -1 --doInitialFit --robustFit 1 --rMax 100 --expectSignal 10
    #combineTool.py -M Impacts -d combine_all.root -m 125 -t -1 --robustFit 1 --doFits --parallel 8 --rMax 100 --expectSignal 10
    #combineTool.py -M Impacts -d combine_all.root -m 125 -t -1 -o impacts.json --rMax 100 --expectSignal 10
    #plotImpacts.py -i impacts.json -o impacts_combined_10
    #rm higgsCombine*
fi
