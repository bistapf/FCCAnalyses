#Input directory where the files produced at the pre-selection level are
inputDir  = "./outputs/"

#Where to store your output file(s) - this can point to the same directort as the input, as the files get renamed
outputDir  = "./outputs/"

processList = {
    "fastsim_tutorial_output":{}, #put the name of your input file here (without .root), the output file will have the same name
    "bkg_evts":{}, 
}

#Link to the dictionary that contains all the cross section informations etc...
procDict = "FCCee_procDict_spring2021_IDEA.json" #this loads the official cross-section file from /cvmfs/fcc.cern.ch/, unfortunately it cannot be overwritten at this stage

#Since we cannot use the official file, we can add the cross-section of our file manually like:
procDictAdd={"fastsim_tutorial_output":{"numberOfEvents": 10000000, "sumOfWeights": 10000000, "crossSection": 0.0026219999999999998, "kfactor": 1.0, "matchingEfficiency": 1.0}}
procDictAdd={"bkg_evts":{"numberOfEvents": 10000000, "sumOfWeights": 10000000, "crossSection": 1530.0, "kfactor": 1.0, "matchingEfficiency": 0.403}}

#Number of CPUs to use
nCPUS = 2

#produces a file with the ROOT TTree, in addition to just histograms as output
doTree = True

###Dictionnay of the list of cuts. The key is the name of the selection that will be added to the output file
cutList = {
            "sel0":"n_photons >= 2", 
            "sel1":"n_photons >= 2 && n_b_jets >= 2", 
            }


#Dictionary for the ouput variable/hitograms. The key is the name of the variable in the output files. "name" is the name of the variable in the input file, "title" is the x-axis label of the histogram, "bin" the number of bins of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.
histoList = {
    "m_yy":{"name":"m_yy","title":"m_{yy} [GeV]","bin":30,"xmin":0,"xmax":300},
    "m_bb_leading":{"name":"m_bb_leading","title":"m_{bb} [GeV]","bin":30,"xmin":0,"xmax":300},
    "n_b_jets":{"name":"n_b_jets","title":"No. of b-jets","bin":10,"xmin":0,"xmax":10},
    "n_photons":{"name":"n_photons","title":"No. of photons","bin":10,"xmin":0,"xmax":10},
}
