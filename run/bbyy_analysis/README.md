#Instructions to produce parquet
##Run analysis module in FCC FW
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

##Process root files
Process root files submittting jobs on condor with:
```
condor_submit Submit.cmd
```
Remember to change the `LAUNCH_FOLDER` in `run_the_skim.sh`
This step will produced root files called `processed_$chunckNumber$` in the same folder were the chuncks are. These root files contain the complex variables needed in the parquet with the right name convention.

##Merge and convert to parquet
Merge the processed trees divided in chunks in one single file changing the path in `mergeTree.py` and running it simply with:
 ```
python mergeTree.py
```
Finally, convert the root files in a Parquet:
```
python openTree.py
```
At the end there will be only one parquet called `df_Sel_All.parquet` with all the samples. 
