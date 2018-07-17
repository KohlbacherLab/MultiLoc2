import re, os, sys, util

tmpfile_path=""

def predict(origin,table,proteins,path,libsvm_path,model=12345, id=1):
	model=str(model)

	file_path = tmpfile_path+str(id)
	input_file = open("%stest_svm.dat" % file_path, 'w')
	no_fv_proteins = []
	for i in range(0, len(proteins)):
		featurevector=""
		if origin == "animal":
			featurevector= "0"+" 1:"+str(proteins[i]['score_sp'])+" 2:"+str(proteins[i]['score_mtp'])+" 3:"+str(proteins[i]['score_other'])+" 4:"+str(proteins[i]['score_sa'])+" 5:"+str(proteins[i]['score_nuc'])+" 6:"+str(proteins[i]['score_nuc_vs_cyt'])+" 7:"+str(proteins[i]['score_lys'])+" 8:"+str(proteins[i]['score_cyt'])+" 9:"+str(proteins[i]['score_mit'])+" 10:"+str(proteins[i]['score_per'])+" 11:"+str(proteins[i]['score_er'])+" 12:"+str(proteins[i]['score_gol'])+" 13:"+str(proteins[i]['score_ext'])+" 14:"+str(proteins[i]['score_pm'])+" 15:"+str(proteins[i]['predictNLS'])+" 16:"+str(proteins[i]['er_target'])+" 17:"+str(proteins[i]['peroxi_target'])+" 18:"+str(proteins[i]['nuclear_bipartite'])+" 19:"+str(proteins[i]['pm_receptor_domain'])+" 20:"+str(proteins[i]['dna_associated_domain'])+" 21:"+str(proteins[i]['nls_mono'])+" 22:"+str(proteins[i]['phylo_score_nuc'])+" 23:"+str(proteins[i]['phylo_score_cyt'])+" 24:"+str(proteins[i]['phylo_score_mit'])+" 25:"+str(proteins[i]['phylo_score_ext'])+" 26:"+str(proteins[i]['phylo_score_pm'])+" 27:"+str(proteins[i]['phylo_score_per'])+" 28:"+str(proteins[i]['phylo_score_er'])+" 29:"+str(proteins[i]['phylo_score_gol'])+" 30:"+str(proteins[i]['phylo_score_lys'])+" 31:"+str(proteins[i]['go_score_nuc'])+" 32:"+str(proteins[i]['go_score_cyt'])+" 33:"+str(proteins[i]['go_score_mit'])+" 34:"+str(proteins[i]['go_score_ext'])+" 35:"+str(proteins[i]['go_score_pm'])+" 36:"+str(proteins[i]['go_score_per'])+" 37:"+str(proteins[i]['go_score_er'])+" 38:"+str(proteins[i]['go_score_gol'])+" 39:"+str(proteins[i]['go_score_lys'])+"\n"
		elif origin == "fungi":
			featurevector= "0"+" 1:"+str(proteins[i]['score_sp'])+" 2:"+str(proteins[i]['score_mtp'])+" 3:"+str(proteins[i]['score_other'])+" 4:"+str(proteins[i]['score_sa'])+" 5:"+str(proteins[i]['score_nuc'])+" 6:"+str(proteins[i]['score_nuc_vs_cyt'])+" 7:"+str(proteins[i]['score_vac'])+" 8:"+str(proteins[i]['score_cyt'])+" 9:"+str(proteins[i]['score_mit'])+" 10:"+str(proteins[i]['score_per'])+" 11:"+str(proteins[i]['score_er'])+" 12:"+str(proteins[i]['score_gol'])+" 13:"+str(proteins[i]['score_ext'])+" 14:"+str(proteins[i]['score_pm'])+" 15:"+str(proteins[i]['predictNLS'])+" 16:"+str(proteins[i]['er_target'])+" 17:"+str(proteins[i]['peroxi_target'])+" 18:"+str(proteins[i]['nuclear_bipartite'])+" 19:"+str(proteins[i]['pm_receptor_domain'])+" 20:"+str(proteins[i]['dna_associated_domain'])+" 21:"+str(proteins[i]['nls_mono'])+" 22:"+str(proteins[i]['phylo_score_nuc'])+" 23:"+str(proteins[i]['phylo_score_cyt'])+" 24:"+str(proteins[i]['phylo_score_mit'])+" 25:"+str(proteins[i]['phylo_score_ext'])+" 26:"+str(proteins[i]['phylo_score_pm'])+" 27:"+str(proteins[i]['phylo_score_per'])+" 28:"+str(proteins[i]['phylo_score_er'])+" 29:"+str(proteins[i]['phylo_score_gol'])+" 30:"+str(proteins[i]['phylo_score_vac'])+" 31:"+str(proteins[i]['go_score_nuc'])+" 32:"+str(proteins[i]['go_score_cyt'])+" 33:"+str(proteins[i]['go_score_mit'])+" 34:"+str(proteins[i]['go_score_ext'])+" 35:"+str(proteins[i]['go_score_pm'])+" 36:"+str(proteins[i]['go_score_per'])+" 37:"+str(proteins[i]['go_score_er'])+" 38:"+str(proteins[i]['go_score_gol'])+" 39:"+str(proteins[i]['go_score_vac'])+"\n"
		else:
			featurevector= "0"+" 1:"+str(proteins[i]['score_sp'])+" 2:"+str(proteins[i]['score_mtp'])+" 3:"+str(proteins[i]['score_ctp'])+" 4:"+str(proteins[i]['score_other'])+" 5:"+str(proteins[i]['score_sa'])+" 6:"+str(proteins[i]['score_nuc'])+" 7:"+str(proteins[i]['score_nuc_vs_cyt'])+" 8:"+str(proteins[i]['score_mtp_vs_ctp'])+" 9:"+str(proteins[i]['score_vac'])+" 10:"+str(proteins[i]['score_cyt'])+" 11:"+str(proteins[i]['score_mit'])+" 12:"+str(proteins[i]['score_chl'])+" 13:"+str(proteins[i]['score_per'])+" 14:"+str(proteins[i]['score_er'])+" 15:"+str(proteins[i]['score_gol'])+" 16:"+str(proteins[i]['score_ext'])+" 17:"+str(proteins[i]['score_pm'])+" 18:"+str(proteins[i]['predictNLS'])+" 19:"+str(proteins[i]['er_target'])+" 20:"+str(proteins[i]['peroxi_target'])+" 21:"+str(proteins[i]['nuclear_bipartite'])+" 22:"+str(proteins[i]['pm_receptor_domain'])+" 23:"+str(proteins[i]['dna_associated_domain'])+" 24:"+str(proteins[i]['nls_mono'])+" 25:"+str(proteins[i]['phylo_score_nuc'])+" 26:"+str(proteins[i]['phylo_score_cyt'])+" 27:"+str(proteins[i]['phylo_score_mit'])+" 28:"+str(proteins[i]['phylo_score_ext'])+" 29:"+str(proteins[i]['phylo_score_pm'])+" 30:"+str(proteins[i]['phylo_score_per'])+" 31:"+str(proteins[i]['phylo_score_er'])+" 32:"+str(proteins[i]['phylo_score_gol'])+" 33:"+str(proteins[i]['phylo_score_vac'])+" 34:"+str(proteins[i]['phylo_score_chl'])+" 35:"+str(proteins[i]['go_score_nuc'])+" 36:"+str(proteins[i]['go_score_cyt'])+" 37:"+str(proteins[i]['go_score_mit'])+" 38:"+str(proteins[i]['go_score_ext'])+" 39:"+str(proteins[i]['go_score_pm'])+" 40:"+str(proteins[i]['go_score_per'])+" 41:"+str(proteins[i]['go_score_er'])+" 42:"+str(proteins[i]['go_score_gol'])+" 43:"+str(proteins[i]['go_score_vac'])+" 44:"+str(proteins[i]['go_score_chl'])+"\n"
		input_file.write(featurevector)
	input_file.close()
	return util.predict_one_vs_one(table,origin,model,path,libsvm_path,tmpfile_path,id,proteins,no_fv_proteins)

def animal_predict(proteins,path,libsvm_path,model=12345, id=1):
	return predict("animal","Benchmark80A",proteins,path,libsvm_path,model, id)

def fungi_predict(proteins,path,libsvm_path,model=12345, id=1):
	return predict("fungi","Benchmark80F",proteins,path,libsvm_path,model, id)

def plant_predict(proteins,path,libsvm_path,model=12345, id=1):
	return predict("plant","Benchmark80P",proteins,path,libsvm_path,model, id)
