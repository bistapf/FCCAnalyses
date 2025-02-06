#Derive the uncertainty systematics, depending on the pT of the muon

import ROOT
import numpy as np
import matplotlib.pyplot as plt
import os
import json

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptTitle(0)


# To work with RDF, need to compile the RDF function in C
ROOT.gInterpreter.Declare(
"""
using namespace ROOT;
float GetEfficiencyScaleFactor(float pt) {
    return 1.+(0.25*sqrt(2500./pow(pt, 2) + 25./pt + 1.))/100.;
}
""")

def f(pt):
    return 0.25*np.sqrt(2500./pt**2 + 25./pt + 1.)

def SF_function(pt):
    return 1.+(0.25*np.sqrt(2500./pt**2 + 25./pt + 1.))/100.

def test_unc_fct():
    pt = np.arange(5., 100., 1)

    for tester_pt in np.arange(5., 100., 1):
        print("pT = {} , delta Eff in % = {:.2f} and SF = {:.4f}".format(tester_pt, f(tester_pt), SF_function(tester_pt)))

    plt.plot(pt, SF_function(pt), lw=2.0, color='blue',  label='mu')
    plt.plot(pt, 2*SF_function(pt), lw=2.0, color='green', label='e, gamma')
    plt.xlabel(r'$p_T [GeV]$', fontsize=18)
    plt.ylabel(r'Scale factor', fontsize=18)

    plt.legend()

    #plt.show()
    plt.savefig('SF_vs_pT.png',format='png')


def get_rdf(input_filepath):

    print("Getting rdf from:", input_filepath)
    rdf = None
    if input_filepath.endswith(".root"):
        try:
            rdf = ROOT.RDataFrame("events", input_filepath)
        except:
            print("File {} appears to be empty.".format(input_filepath))
            return
    else:
        print("Adding chunks ..")
        # rdf = ROOT.RDataFrame("events", input_filepath+"/chunk99.root")
        rdf = ROOT.RDataFrame("events", input_filepath+"/chunk*")

    if not rdf:
        print("Empty file for:", input_filepath, " Exiting.")
        return

    # print(rdf.GetColumnNames())

    return rdf

def plot_histo(rdf, var, outpath, outname, fileformat=".png"):
    temp_hist = rdf.Histo1D(var)
    canvas = ROOT.TCanvas("canvas", "canvas", 800, 800) 
    canvas.cd()
    temp_hist.Draw()
    canvas.SaveAs(os.path.join(outpath, outname+fileformat))

def plot_scalefactors(process_name, SF_vs_pT_dict, plotdir):
    out_path = os.path.join(plotdir, "EffScaleFactor_vs_pT_for_{}.png".format(process))
    
    x = list(SF_vs_pT_dict.keys())
    y = list(SF_vs_pT_dict.values())

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, marker='o')  # 'o' adds markers to the data points
    plt.title('Muon reconstruction efficiencies')
    plt.xlabel('Minimum pT(H) in GeV')
    plt.ylabel('Scalefactor (up)')
    plt.grid(True)
    plt.xticks(x)  # Set x ticks to be the keys of the dictionary
    plt.yticks([round(i, 2) for i in y])  # Customize y ticks to show rounded values
    plt.savefig(out_path)



# #_____________________________________________________________________________________________________
# def efficiency_uncertainty_function(pt):
#     return 0.25*np.sqrt(2500./pt**2 + 25./pt + 1.)

# #_____________________________________________________________________________________________________

if __name__ == "__main__":
    #plot and check first
    # test_unc_fct() 

    #input and output dirs
    base_inpath = "/eos/experiment/fcc/hh/analysis_ntuples/fcc_v06/II/Hmumu_analysis/final/"
    base_outpath = base_inpath
    base_plotpath = "./plots_Hmumu_Eff_Scalefactors/"

    if not os.path.exists(base_plotpath):
        os.mkdir(base_plotpath)

    processes = [
                    "mgp8_pp_h012j_5f_hmumu", #SIGNAL
                    
                    "mgp8_pp_mumu012j_mhcut_5f_HT_0_100",
                    "mgp8_pp_mumu012j_mhcut_5f_HT_100_300",
                    "mgp8_pp_mumu012j_mhcut_5f_HT_300_500",
                    "mgp8_pp_mumu012j_mhcut_5f_HT_500_700",
                    "mgp8_pp_mumu012j_mhcut_5f_HT_700_900",
                    "mgp8_pp_mumu012j_mhcut_5f_HT_900_1100",
                    "mgp8_pp_mumu012j_mhcut_5f_HT_1100_100000",
                    # "mgp8_pp_mumu012j_mhcut_5f_HT_100_300",
                    # "mgp8_pp_mumu012j_mhcut_5f_HT_300_500",
                    # "mgp8_pp_mumu012j_mhcut_5f_HT_500_700",
                    # "mgp8_pp_mumu012j_mhcut_5f_HT_700_900",
                    # "mgp8_pp_mumu012j_mhcut_5f_HT_900_1100",
                    # "mgp8_pp_mumu012j_mhcut_5f_HT_1100_100000",
                ]
    dict_of_SFs = {}

    for process in processes:
        print("Processing sample: ", process)

        # loop over all pT minimum cuts, and make a list of SF
        dict_SF_vs_pT = {}
        for pT_cut in range(50, 550, 50):
            print("Getting Scalefactors for pT cut = ", pT_cut)
        
            infilename = "{}_sel3_pTH{}.root".format(process, pT_cut)
            infilepath = os.path.join(base_inpath, infilename)
            outfilename = "{}_sel3_pTH{}_SYST1UP.root".format(process, pT_cut)
            outfilepath = os.path.join(base_inpath, outfilename)
            rdf = get_rdf(infilepath)

            if not rdf:
                continue

            rdf = (rdf.Define("SF_muplus", "GetEfficiencyScaleFactor(mu_plus_pt[0])")
                    .Define("SF_muminus", "GetEfficiencyScaleFactor(mu_minus_pt[0])")
                    .Define("SF_muons", "SF_muplus*SF_muminus")
                )

            rdf.Snapshot("events", outfilepath, ["SF_muons", "SF_muplus", "SF_muminus", "mu_plus_pt", "mu_minus_pt", "m_mumu"])
            
            hist_base_name = "{}_pTH{}_hist_".format(process, pT_cut)
            plot_histo(rdf, "SF_muons", base_plotpath, hist_base_name+"SF_muons")
            plot_histo(rdf, "SF_muplus", base_plotpath, hist_base_name+"SF_muplus")
            plot_histo(rdf, "SF_muminus", base_plotpath, hist_base_name+"SF_muminus")

            #fill the histogram of the observable with the new SF and divide by nominal 
            hist_m_mumu_model = ROOT.RDF.TH1DModel("m_mumu_1bin","m_mumu_1bin", 1, 124., 126.)
            hist_m_mumu_nom = rdf.Histo1D(hist_m_mumu_model, "m_mumu")
            hist_m_mumu_up = rdf.Histo1D(hist_m_mumu_model, "m_mumu", "SF_muons")

            #calculate: 
            nominal_yield = hist_m_mumu_nom.GetValue().Integral()
            up_yield = hist_m_mumu_up.GetValue().Integral()
            syst_var_up = up_yield/nominal_yield
            print("Nominal yield: {:.2f}".format(nominal_yield))
            print("Up syst yield: {:.2f}".format(up_yield))
            print("Up systematic variation: {:.6f}".format(syst_var_up))

            dict_SF_vs_pT[pT_cut] = syst_var_up
            # list_SF.append(syst_var_up)
        
        #put the list of SFs for the process in the dictionary
        # print(list_SF)
        dict_of_SFs[process] = dict_SF_vs_pT
        plot_scalefactors(process, dict_SF_vs_pT, base_plotpath)
    
    print(dict_of_SFs)
    with open('/afs/cern.ch/user/b/bistapf/combine_EL9/Hmumu_analysis/SF_eff_vs_pT_100TeV.json', 'w') as json_file:
        json.dump(dict_of_SFs, json_file)

   
   
    # #plot the total SF as a check:
    # hist_SF_muons = rdf.Histo1D("SF_muons")
    # hist_SF_muplus = rdf.Histo1D("SF_muplus")
    # hist_SF_muminus = rdf.Histo1D("SF_muminus")

    # #setup canvas
    # canvas = ROOT.TCanvas("canvas", "canvas", 800, 800) 
    # canvas.cd()
    # hist_SF_muons.Draw()
    # canvas.SaveAs("./hist_SF_muons.png")

    # canvas.Clear()
    # hist_SF_muplus.Draw()
    # canvas.SaveAs("./hist_SF_muplus.png")\

    # canvas.Clear()
    # hist_SF_muminus.Draw()
    # canvas.SaveAs("./hist_SF_muminus.png")

    # #fill the histogram of the observable with the new SF and divide by nominal 
    # hist_m_mumu_model = ROOT.RDF.TH1DModel("m_mumu_1bin","m_mumu_1bin", 1, 124., 126.)
    # hist_m_mumu_nom = rdf.Histo1D(hist_m_mumu_model, "m_mumu")
    # hist_m_mumu_up = rdf.Histo1D(hist_m_mumu_model, "m_mumu", "SF_muons")

    # #calculate: 
    # nominal_yield = hist_m_mumu_nom.GetValue().Integral()
    # up_yield = hist_m_mumu_up.GetValue().Integral()
    # syst_var_up = up_yield/nominal_yield
    # print("Nominal yield: {:.2f}".format(nominal_yield))
    # print("Up syst yield: {:.2f}".format(up_yield))
    # print("Up systematic variation: {:.2f}".format(syst_var_up))
    # print("Integral of SF histogram:", hist_SF_muons.GetValue().Integral())
    # print("Sum of SF column weight:", rdf.Sum("SF_muons").GetValue())
    