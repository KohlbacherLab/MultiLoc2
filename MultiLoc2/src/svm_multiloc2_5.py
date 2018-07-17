import re, os, sys, util

tmpfile_path=""

def predict(origin,table,proteins,path,libsvm_path,model=12345, id=1):
	model=str(model)

	file_path = tmpfile_path+str(id)
	input_file = open("%stest_svm.dat" % file_path, 'w')
	no_fv_proteins = []
	for i in range(0, len(proteins)):
		featurevector=""
		if origin == "plant":
			featurevector= "0"+" 1:"+str(proteins[i]['score_sp'])+" 2:"+str(proteins[i]['score_mtp'])+" 3:"+str(proteins[i]['score_ctp'])+" 4:"+str(proteins[i]['score_other'])+" 5:"+str(proteins[i]['score_nuc'])+" 6:"+str(proteins[i]['score_nuc_vs_cyt'])+" 7:"+str(proteins[i]['score_mtp_vs_ctp'])+" 8:"+str(proteins[i]['score_cyt'])+" 9:"+str(proteins[i]['score_mit'])+" 10:"+str(proteins[i]['score_chl'])+" 11:"+str(proteins[i]['score_ext'])+" 12:"+str(proteins[i]['predictNLS'])+" 13:"+str(proteins[i]['er_target'])+" 14:"+str(proteins[i]['peroxi_target'])+" 15:"+str(proteins[i]['nuclear_bipartite'])+" 16:"+str(proteins[i]['pm_receptor_domain'])+" 17:"+str(proteins[i]['dna_associated_domain'])+" 18:"+str(proteins[i]['nls_mono'])+" 19:"+str(proteins[i]['phylo_score_nuc'])+" 20:"+str(proteins[i]['phylo_score_cyt'])+" 21:"+str(proteins[i]['phylo_score_mit'])+" 22:"+str(proteins[i]['phylo_score_chl'])+" 23:"+str(proteins[i]['phylo_score_ext'])+" 24:"+str(proteins[i]['go_score_nuc'])+" 25:"+str(proteins[i]['go_score_cyt'])+" 26:"+str(proteins[i]['go_score_mit'])+" 27:"+str(proteins[i]['go_score_chl'])+" 28:"+str(proteins[i]['go_score_ext'])+"\n"
		else:
			featurevector= "0"+" 1:"+str(proteins[i]['score_sp'])+" 2:"+str(proteins[i]['score_mtp'])+" 3:"+str(proteins[i]['score_other'])+" 4:"+str(proteins[i]['score_nuc'])+" 5:"+str(proteins[i]['score_nuc_vs_cyt'])+" 6:"+str(proteins[i]['score_cyt'])+" 7:"+str(proteins[i]['score_mit'])+" 8:"+str(proteins[i]['score_ext'])+" 9:"+str(proteins[i]['predictNLS'])+" 10:"+str(proteins[i]['er_target'])+" 11:"+str(proteins[i]['peroxi_target'])+" 12:"+str(proteins[i]['nuclear_bipartite'])+" 13:"+str(proteins[i]['pm_receptor_domain'])+" 14:"+str(proteins[i]['dna_associated_domain'])+" 15:"+str(proteins[i]['nls_mono'])+" 16:"+str(proteins[i]['phylo_score_nuc'])+" 17:"+str(proteins[i]['phylo_score_cyt'])+" 18:"+str(proteins[i]['phylo_score_mit'])+" 19:"+str(proteins[i]['phylo_score_ext'])+" 20:"+str(proteins[i]['go_score_nuc'])+" 21:"+str(proteins[i]['go_score_cyt'])+" 22:"+str(proteins[i]['go_score_mit'])+" 23:"+str(proteins[i]['go_score_ext'])+"\n"
		input_file.write(featurevector)
	input_file.close()
	return util.predict_one_vs_one(table,origin,model,path,libsvm_path,tmpfile_path,id,proteins,no_fv_proteins)

def animal_predict(proteins,path,libsvm_path,model=12345, id=1):
	return predict("animal","BACELLOA",proteins,path,libsvm_path,model, id)

def fungi_predict(proteins,path,libsvm_path,model=12345, id=1):
	return predict("fungi","BACELLOF",proteins,path,libsvm_path,model, id)

def plant_predict(proteins,path,libsvm_path,model=12345, id=1):
	return predict("plant","BACELLOP",proteins,path,libsvm_path,model, id)
