import glob 
import ROOT

inputDir = "/eos/user/b/bistapf/FCChh_EvtGen/bb2lMET_ntuples/SFOS/"
pr = "mgp8_pp_tt012j_5f"

processEvents={}
SumOfWeights={}
eventsTTree={}

processEvents[pr]=0
eventsTTree[pr]=0
SumOfWeights[pr]=0


flist=glob.glob(inputDir+pr+"/chunk*.root")
for f in flist:
	tfin = ROOT.TFile.Open(f)
	print ('  ----> ',f)
	tfin.cd()
	found=False
	for key in tfin.GetListOfKeys():
		if 'eventsProcessed' == key.GetName():
			events = tfin.eventsProcessed.GetVal()
			processEvents[pr]+=events
			sow = tfin.SumOfWeights.GetVal()
			SumOfWeights[pr] = sow
			found=True
			print(events)
	if not found:
		print("Couldnt find the eventsProcessed Tparameter")
		continue
		processEvents[pr]=1
		SumOfWeights[pr]=1

	tt=tfin.Get("events")

	if not tt:
		print("Tree not found in file", tfin, " possibly empty chunk - continuing with next one.")
		continue 

	eventsTTree[pr]+=tt.GetEntries()
	print(tt.GetEntries())

	tfin.Close()

print("evtsProcessed", processEvents[pr])
print("evtsTree", eventsTTree[pr])