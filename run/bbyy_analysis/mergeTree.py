#
#
#Careful, it work only in a cmsenv
#
#
file_name = ['mgp8_pp_h012j_5f_haa', 'mgp8_pp_vbf_h01j_5f_haa', 'mgp8_pp_tth01j_5f_haa', 'mgp8_pp_vh012j_5f_haa','pwp8_pp_hh_lambda000_5f_hhbbaa', 'pwp8_pp_hh_lambda100_5f_hhbbaa', 'pwp8_pp_hh_lambda240_5f_hhbbaa','pwp8_pp_hh_lambda300_5f_hhbbaa','mgp8_pp_jjaa_5f']

import os
for name in file_name:
         print(name)
         os.system('hadd '+name+'.root $(find /eos/user/p/pmastrap/FCCFW/Analysis/FCCAnalyses/run/Delphescard_validation/FCCAnalysis_ntuples_forAnalysis/'+ name + ' -name "processed*.root")')

