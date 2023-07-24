import os

path="/eos/home-b/bistapf/FCChh_EvtGen/bb2lMET_ntuples/SFOS/mgp8_pp_h012j_5f/"

#remove all 200s

#10s
# for i in range(0, 9):
# 	filepath = os.path.join(path, "chunk20{}.root".format(i))
# 	print("Deleting file:", filepath)
# 	os.remove(filepath)

#higher
# for i in range(20, 99):
# 	filepath = os.path.join(path, "chunk2{}.root".format(i))
# 	print("Deleting file:", filepath)
# 	os.remove(filepath)

# 300s

# for i in range(0, 9):
# 	filepath = os.path.join(path, "chunk30{}.root".format(i))
# 	print("Deleting file:", filepath)
# 	os.remove(filepath)

for i in range(10, 30):
	filepath = os.path.join(path, "chunk3{}.root".format(i))
	print("Deleting file:", filepath)
	os.remove(filepath)