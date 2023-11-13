from collections import namedtuple
import ROOT
import argparse
import os 
import numpy as np
from helpers import get_rdf, 

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptTitle(0)

def plot_truth_distributions(inputdir, outputdir):

	#get the rdf
	rdf = helpers.get_rdf(inputdir)

	if not rdf:
                print("Empty file for:", input_filepath, " Exiting.")
                return

	#distributions to plot
	bbyy_truth_plots={
	  "pT_truth_Hbb":PlotSpecs(name="pT_truth_Hbb", xmin=0., xmax=200., label="p_{T} H (#arrow bb) truth [GeV]", nbins=20),
	}

	for plot in bbyy_truth_plots:
		hist = 








if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Plot distributions for validation of new signal files")
	parser.add_argument('--input', '-i', metavar="INPUTDIR", dest="inDir", required=True, help="Path to the input directory")
	parser.add_argument('--outdir', '-o', metavar="OUTPUTDIR", dest="outDir", required=True, help="Output directory.")
	args = parser.parse_args()

	if not os.path.exists(args.outDir):
		os.mkdir(args.outDir)


	#use a custom namedntuple to transfer the plotting info
	PlotSpecs = namedtuple('PlotSpecs', ['name', 'xmin', 'xmax', 'label', 'nbins'])

	plot_truth_distributions(args.inDir, args.outDir)


#python eff_checks_btag_bbyy.py -i /eos/user/b/bistapf/FCChh_EvtGen/FCCAnalysis_scenI_valid_ntuples/ -o ./Plots_bbyy_btag_checks/ 