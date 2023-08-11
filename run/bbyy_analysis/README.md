# Instructions to produce parquet
## Run analysis module in FCC FW
First source the FW setup:
```
source setup.sh
```
Then run the analysis module locally to test:
```
fccanalysis run analysis_bbyy_selections_v2.py --nevents 100
```
Remember to switch to `runBatch = False` in the script!!

Then run on batch by switching back `runBatch = True` (ideally this could be pass asargument) and run simply:
```
fccanalysis run analysis_bbyy_selections_v2.py
```
This step will produce root files needed for the following.
To generate the json file with info on xs, total number of generated events, sumofweights etc. run
```
python create_norm_dict.py -i <directory_with_your_ntuples>
```
## Process root files
Process root files submittting jobs on condor with:
```
condor_submit Submit.cmd
```
Remember to change the `LAUNCH_FOLDER` in `run_the_skim.sh`
This step will produced root files called `processed_$chunckNumber$` in the same folder were the chuncks are. These root files contain the complex variables needed in the parquet with the right name convention.

## Merge and convert to parquet
Merge the processed trees divided in chunks in one single file changing the path in `mergeTree.py` and running it simply with:
 ```
python mergeTree.py
```
Finally, convert the root files in a Parquet:
```
python openTree.py
```
At the end there will be only one parquet called `df_Sel_All_haa_Mbtag.parquet` with all the samples. 

## Notebooks: Run DNNs and define cuts and categorization
`full_3DNN.ipynb` performs ttH killer dnn training and other 2 "global" dnns training (one in Mx>350 GeV, th other in Mx<350 GeV).
It saves the dnn models to be retrieved later by `applyDNN_SelCat_full3DNN.ipynb`. 
`applyDNN_SelCat_full3DNN.ipynb` applies the dnns to the whole dataset (trick to not make the notebook crush: run separatly on df_signal and df_bkg then concatenate the dfs). It finds the best cut for ttH killer and the best delimiters for high/low purity and central/sidebands regions. Finally it saves one dataframe for each category in a parquet file. 

## Create inputs for Combine
Run `create_histo_allCats.py` to open the dfs of the previous step, extract the m_gg, bin the distribution and save it in a root file. Here a+jj is added (scaled from the jj+aa) and 'data_obs' is append at the resulting root file to satisfy Combine requirements.

## Create card and run Combine
Run:
```
bash run_cards_allCats.sh bbgg <name_folder_you_like>
```
It will produce cards, combine them, run the fit, plot the NLL scan for every scarios (I,II,III)
