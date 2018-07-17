import os, sys, re

class Error(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

def search_program(program, warning):
	path =""
	print "searching for %s ... " %(program)
	path = run_shell_command("which " + program)
	if (path != ""):
		print "... found: %s" %(path)
		print
		return re.sub(program+"$","",path)
	elif warning == 1:
		print "Warning: %s not found!" %(program)
		print "It is recommended but not required to install %s and to include its path into your $PATH variable!" %(program)
		return path
	else:
		msg = "Error: %s not found!" %(program)
		msg = msg + " Include the path to %s into your $PATH variable and restart python configure.py!" %(program)
		raise Error(msg)

def run_shell_command(cmd):
	stdout_handle = os.popen(cmd, "r")
	return re.sub("\n","",stdout_handle.read())

def set_path_in_src_files(type,path,src_path):
	cmd= "sed -i 's/%s\s*=\s*\"[^\"]*\"/%s=\"" %(type,type)
	cmd = cmd + re.sub("/","\\/",path) + "\"/g' " + src_path + "*.py"
	run_shell_command(cmd)

#main program
print
print "Start MultiLoc2 configuration:"
print
multiloc2_path = run_shell_command("pwd")
tmp_file_path = multiloc2_path + "/tmp/"
src_path = multiloc2_path + "/src/"
svm_data_path = multiloc2_path + "/data/svm_models/MultiLoc2/"
genome_path =  multiloc2_path + "/data/NCBI/"

svm_predict_path = search_program("svm-predict",0)
blast_path = search_program("blastall",0)
formatdb_path = search_program("formatdb",0)
inter_pro_scan_path = search_program("iprscan",1)

print "\nset all static paths in source files ..."
#all is fine here
set_path_in_src_files("src_path",src_path,src_path)
set_path_in_src_files("tmpfile_path",tmp_file_path,src_path)
set_path_in_src_files("svm_data_path",svm_data_path,src_path)
set_path_in_src_files("genome_path",genome_path,src_path)
set_path_in_src_files("libsvm_path",svm_predict_path,src_path)
set_path_in_src_files("blast_path",blast_path,src_path)
set_path_in_src_files("formatdb_path",formatdb_path,src_path)
set_path_in_src_files("inter_pro_scan_path",inter_pro_scan_path,src_path)

print "... create script run_multiloc2_with_iprscan"
file = open("run_multiloc2_with_iprscan","w")
file.write("%siprscan -cli -i $1 -o interpro.out -format raw -goterms -iprlookup\n" %(inter_pro_scan_path))
file.write("python %smultiloc2_prediction.py -fasta=$1 -origin=$2 -result=$3 -go=interpro.out" %(src_path))
file.close()
os.system("chmod 755 run_multiloc2_with_iprscan")

print "... completed"
print "MultiLoc2 is ready to use!"
