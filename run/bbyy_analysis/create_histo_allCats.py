from root_numpy import fill_hist
import pyarrow.parquet as pq
import pandas as pd
import ROOT
import numpy as np

df_dict=["great350_high_purity_sb", "great350_high_purity_c","great350_medium_purity_sb","great350_medium_purity_c","small350_high_purity_sb","small350_high_purity_c" , "small350_medium_purity_sb", "small350_medium_purity_c" ]

edges_dict ={
         "great350_high_purity_sb": [100.,118, 120, 121, 122, 123, 124, 125, 126, 127, 128,129, 130, 132, 180],
         "great350_high_purity_c" : [100.,118, 120, 121, 122, 123, 124, 125, 126, 127, 128,129, 130, 132, 180],
         "great350_medium_purity_sb": [100.,118, 120, 121, 122, 123, 124, 125, 126, 127, 128,129, 130, 132, 180],
         "great350_medium_purity_c" : [100.,118, 120, 121, 122, 123, 124, 125, 126, 127, 128,129, 130, 132, 180],
        
         "small350_high_purity_sb": [100., 122, 123, 124, 125, 126, 127, 128, 180],
         "small350_high_purity_c": [100., 122, 123, 124, 125, 126, 127, 128, 180],
         "small350_medium_purity_sb": [100., 122, 123, 124, 125, 126, 127, 128, 180],
         "small350_medium_purity_c": [100., 122, 123, 124, 125, 126, 127, 128, 180],
         
}


for kdf in df_dict:
    skim_pq = pq.read_table("./InputParquets/"+kdf+".parquet")
    df = skim_pq.to_pandas() 
    out_file = ROOT.TFile("/afs/cern.ch/user/p/pmastrap/Combine/CMSSW_10_2_13/src/HiggsAnalysis/CombinedLimit/HH_FCChh_newCard_2023/input_files/"+kdf+".root","RECREATE")
    for i in df.process.unique():
        histo = ROOT.TH1D("mgg_"+str(i) ,"mgg_"+str(i), len(np.array(edges_dict[kdf]))-1,np.array(edges_dict[kdf]))
        histo.Sumw2()
        fill_hist(histo, (df.loc[df.process == str(i),:]['haa_m']).to_numpy(),
                  weights=(df.loc[df.process == str(i),:]['weight']).to_numpy())
        histo.Write()

        #addition of jja (scaling jjaa)
        if "jjaa" in i:
           name = i.replace("jjaa","jja")
           histo_jja = ROOT.TH1D("mgg_"+str(name) ,"mgg_"+str(name), len(np.array(edges_dict[kdf]))-1,np.array(edges_dict[kdf]))
           histo_jja.Sumw2()
           fill_hist(histo_jja, (df.loc[df.process == str(i),:]['haa_m']).to_numpy(),
                  weights=(df.loc[df.process == str(i),:]['weight']*0.09).to_numpy())
           histo_jja.Write()
           for ibin in range(1,histo_jja.GetNbinsX()+1):
               if histo_jja.GetBinContent(ibin) < 0:
                   print("sono entrato")
                   print("process ", str(i))
                   histo_jja.SetBinContent(ibin,1e-3)

        for ibin in range(1,histo.GetNbinsX()+1):
           if histo.GetBinContent(ibin) < 0:
               print("sono entrato")
               print("process ", str(i))
               histo.SetBinContent(ibin,1e-3)

    data_obs = ROOT.TH1D( "data_obs" ,"data_obs",1,0.,1.)
    data_obs.Fill(1)
    data_obs.Write()
    out_file.Close()
