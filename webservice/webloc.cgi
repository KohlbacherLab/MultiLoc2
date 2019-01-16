#!/usr/bin/python

import sys, os, re, cgi, time, traceback
from subprocess import PIPE, Popen

sys.stderr = sys.stdout

# 2018_12_20_MOD sys.path.append('/share/projects/LOC_PRED/WebServices/YLoc');
sys.path.append('/MultiLoc2');

# Tag YLoc Webservice Instance
os.environ['MULTILOC2_WS'] = '1';

#os.environ['MULTILOC2_DEBUG'] = '1';

os.environ['MULTILOC2_JOBS'] = '/ml2jobs';

os.environ['MULTILOC2_MAX_SEQS'] = '20';

if os.path.isfile("/interproscan/interproscan.sh"):
  os.environ['INTERPROSCAN'] = "/interproscan";



python_path = "/usr/bin/python";

# 2018_12_20_MOD img_path = "http://www-bs2.informatik.uni-tuebingen.de/services/briese/";
img_path = "images/";
download_path = "downloads/";

contact_email = "abi-multiloc2@informatik.uni-tuebingen.de";

try:
  import cgitb;
  import random;
  import md5;
  import re;
  from Bio import SeqIO;
  from Bio.Seq import Seq;
  from Bio.Alphabet import IUPAC, _verify_alphabet;
  cgitb.enable();
except:
  print "\n\n<PRE>"
  traceback.print_exc()



def db_query(statement):
  # create a connection to the database
  #db = MySQLdb.connect(host = "www-bs3", port = 3306, user="yloc",passwd="elucidate",db ="YLocDB")
  db = mysql.connector.connect(user='yloc', password='!yloc818%/', host='localhost', database='YLocDB')

  # get a database cursor from that connection
  cursor = db.cursor();
  cursor.execute(statement)

  if cursor.with_rows:
    return cursor.fetchall()
  else:
    return []


def getJobInfo(id):
  sql_string = "SELECT id,nr_sequences,finished_sequences FROM pending WHERE id='"+str(id)+"';";
  res=db_query(sql_string);

  if len(res) > 0:
    return res[0];
  else:
    sql_string = "SELECT id FROM queries WHERE id='"+str(id)+"';";
    res=db_query(sql_string);

    if len(res) > 0:
      return [1];
    else:
      return [];


def alterJobStatus(id, nr=1, add=True, nr_finished=-1, ip=""):
  if add:
    sql_string = "Insert Into pending (id,nr_sequences,finished_sequences,ip) values ('"+str(id)+"','"+str(nr)+"','0','"+str(ip)+"');";
    res=db_query(sql_string);
  else:
    if nr_finished > 0:
      sql_string = "Update pending set finished_sequences='"+str(nr_finished)+"' where id='"+str(id)+"';";
      res=db_query(sql_string);
    else:
      sql_string = "Delete From pending where id='"+str(id)+"';";
      res=db_query(sql_string);


# ----------------------------------------------------------------------
# Helper Methods
# ----------------------------------------------------------------------
def __job_dir():
  return os.getenv("MULTILOC2_JOBS")


def __job_file_path(file_name):
  return os.path.join(__job_dir(), file_name)


def __job_status(id):
  job_file = __job_file_path(id)

  if os.path.isfile(job_file):
    if os.path.getsize(job_file):
      return "finished"
    else:
      return "pending"
  else:
    return "invalid"


def __max_input_seqs():
  return int(os.getenv("MULTILOC2_MAX_SEQS"))


def __createID():
  id = str(random.random());
  md5object = md5.new(id);
  id = md5object.hexdigest();
  return id;


def __print_header(refresh=0,id=1):
  print "Content-type: text/html\n"
  print "<HTML><HEAD>";

  if refresh >0:
    print "<meta http-equiv='refresh' content='" + str(refresh) + "; URL=webloc.cgi?id=" + str(id) + "'>"

  print "<TITLE>MultiLoc2</TITLE>"
  print "<style type='text/css'>";
  print " h1 { color:#734D38; font-family:Verdana; font-variant:small-caps; font-size:30pt; font-weight:bold; }  "
  print " h2 { color:#000000; font-family:Verdana; font-size:13pt; font-weight:bold; }  "
  print " h3 { color:#000000; font-family:Verdana; font-size:10pt; font-weight:bold; }  "
  print " #navi { margin: 0px 10px; height:32px; background-color:#FFFFFF; border:0px; border-top:1px; border-style:solid; border-color:#000000;}"
  print " #navi a { color:#FFFFFF; font-size:10pt; background-color: #003380; padding:0px 18px; padding-bottom:3px; margin:0pt; border:1px; border-color:#000000; border-style:solid; text-decoration:none;margin-right:3pt;}"
  print " #navi a:hover {  background-color: #aaccff; color:#000000; border-color:#000000;  }"
  print " #navi .current { background-color: #cbdbff; color:#000000; border-color:#0F0F0F;}"
  print " #subnavi { padding-bottom:5px; padding-top:0px; text-align:right; margin-left:0px;width:190px;background-color:#FFFFFF; border:0px; border-top:2px; border-bottom:2px; border-color:#B38D68; border-style:solid;} ";
  print " #subnavi ul { margin:0px;padding:0px; text-align:right;list-style:none; width:140px; }";
  print " #subnavi li { text-align:right; }";
  print " #subnavi li a {  font-size:10pt; text-align:left; padding:2px; margin-left:20px; height:15px; width:140px; background:#EEEEEE; display:block; margin-top:5px; text-decoration:none; border:0px; border-left:4px; border-color:#CCCCCC; border-style:solid;}"
  print " #subnavi li a:hover { border-color:#777777;  }"
  print " #subnavi .current { background-color: #DDDDDD; color:#444444; }";
  print " a { font-family:Verdana; color:#000000; } ";
  print " img { border:none; }";
  print " hr { border:0px solid #000000; height:1px; background-color:#000000;}";
  print " a.helptext { color:#000000; } ";
  print " p.underl a { color:#000000; text-decoration:underline;} ";
  print " th.underl a {text-decoration:underline;};"

  print " p { font-family:Verdana; vertical-align:top; font-size:10pt; font-weight:normal; color:#000000; text-decoration:none; padding:3px; border:0px; text-align:left; } ";
  print " div { font-family:Verdana; vertical-align:top; font-size:10pt; font-weight:normal; color:#000000; text-decoration:none; padding:0px; border:0px; text-align:left; } ";
  print " .input { font-family:Verdana; vertical-align:top; font-size:10pt; font-weight:normal; color:#000000; text-decoration:none; padding:3px; text-align:left; } ";
  print " .button {  background-color:#cbdbff; } ";
  print " .button2 { cursor:pointer; background-color:#dee7ec; font-family:Verdana; vertical-align:top; font-size:10pt; font-weight:normal; color:#000000; text-decoration:none;  border:0px solid #000000; padding:2px; margin2px; text-align:center;} ";
  print " td { font-family:Verdana; vertical-align:top; font-size:10pt; font-weight:normal; color:#000000; text-decoration:none; padding:3px; border:0px; text-align:left; } ";
  print " th { font-family:Verdana; vertical-align:top; font-size:10pt; font-weight:normal; color:#000000; text-decoration:none; padding:20px; border:0px; text-align:left; } ";
  print " th a {  font-size:10pt; color:#000000; text-decoration:none; } ";
  print " .headerprediction { vertical-align:center; height:10pt; font-size:8pt; color:#000000; text-decoration:none; font-weight:normal; text-align:left;} ";
  print " .predict1 {  vertical-align:center; background-color:#CCE6FF; height:12pt; font-size:10pt; color:#000000; text-decoration:none; font-weight:normal; text-align:left;} ";
  print " .attr1 {   background-color:#EEEEFF; font-size:12pt; color:#000000; text-decoration:none; font-weight:normal; text-align:left;} ";
  print " .predict2 { vertical-align:center;  background-color:#DDF6FF; height:12pt;  font-size:10pt; color:#222222; text-decoration:none; font-weight:normal; text-align:left;} ";
  print " .attr2 {  background-color:#EEEEFF; font-size:10pt; color:#222222; text-decoration:none; font-weight:normal; text-align:left;} ";
  print " .tablematrix { font-family:Arial; color:#000000; background-color:#FFFFFF; vertical-align:top;  font-size:10pt; padding: 1px 1px; border:0px; }";
  print " .amatrix1 { vertical-align:center;  background-color:#EEEEFE; height:12pt;  font-size:10pt; color:#222222; text-decoration:none; font-weight:normal; text-align:left; padding:1px;} ";
  print " .amatrix2 { vertical-align:center;  background-color:#E2E2F2; height:12pt;  font-size:10pt; color:#222222; text-decoration:none; font-weight:normal; text-align:left; padding:1px;} ";
  print " .amatrix3 { vertical-align:center;  background-color:#FFFFFF; height:12pt;  font-size:10pt; color:#222222; text-decoration:none; font-weight:normal; text-align:left; padding:1px; border:3px solid #D2D2D2;} ";
  print " .amatrixside { vertical-align:center;  background-color:#cbdbff;    font-weight:bold; font-size:10pt; color:#222222; text-decoration:none;  text-align:left; } ";
  print " .empty {  background-color:#FFFFFF; font-size:10pt; color:#444444; text-decoration:none; font-weight:normal; text-align:left;} ";
  print " .thpredict {  background-color:#EEEEEE; font-size:12pt; color:#00000; text-decoration:none; font-weight:bold; padding-bottom: 2px; padding-top:2px; text-align:left;} ";
  print " .thheading {  background-color:#FFFFFF; font-size:11pt; color:#00000; text-decoration:none; font-weight:bold; padding-bottom: 2px; padding-top:2px; text-align:left;} ";
  #print " th.thheading span  { display:none;  position:absolute; left:30em;  } ";
  #print " th.thheading:hover span { display:block; background-color:#FFFFC5; color:#000000; font-size:10pt; cursor:help; text-decoration:none; font-weight:normal; cursor:help; width:400pt; border:1px solid #000000; padding:3px; } ";
  #print " th.thheading:hover {   cursor:help; } ";
  print " .thheading2 {  background-color:#FFFFFF; font-size:11pt; color:#00000; text-decoration:none; font-weight:bold; padding-bottom: 2px; padding-top:2px; text-align:left;} ";
  print " .thheading span {  color:#000000; font-size:10pt; cursor:help; text-decoration:none; font-weight:normal; cursor:help; padding:3px; } ";
  print " a.thheading2 span  { display:none;  position:absolute; left:30em;  } ";
  print " a.thheading2:hover span { display:block; background-color:#FFFFC5; color:#000000; font-size:10pt; cursor:help; text-decoration:none; font-weight:normal; cursor:help; width:400pt; border:1px solid #000000; padding:3px; } ";
  print " a.thheading2:hover {   cursor:help; } ";

  print " a.helptext span  { display:none;  position:absolute; } ";
  print " a.helptext:hover span { display:block; background-color:#FFFFC5; color:#000000; font-size:10pt; cursor:help; text-decoration:none; font-weight:normal; cursor:help; width:200pt; border:1px solid #000000; padding:3px; } ";
  print " a.helptext:hover {   cursor:help; } ";

  print " a.helptextsmall span  { display:none;  position:absolute; } ";
  print " a.helptextsmall:hover span { display:block; background-color:#FFFFC5; color:#000000; font-size:10pt; cursor:help; text-decoration:none; font-weight:normal; cursor:help; width:70pt; border:1px solid #000000; padding:3px; } ";
  print " a.helptextsmall:hover {   cursor:help; } ";

  print " td.probtable span  { display:none;  position:absolute; top:30em; right:6em;  } "
  print " td.probtable:hover span  { display:block; background-color:#FFFFFF; color:#000000; font-size:10pt; cursor:help; text-decoration:none; font-weight:normal; cursor:help; width:330pt;padding:3px; border:1px solid #cbdbff;} ";
  print " td.probtable:hover {   cursor:help; } ";
  print " a.probtable span  { display:none;  position:absolute; top:30em; right:6em;  } "
  print " a.probtable:hover span  { display:block; background-color:#FFFFFF; color:#000000; font-size:10pt; cursor:help; text-decoration:none; font-weight:normal; cursor:help; width:330pt;padding:3px; border:1px solid #cbdbff;} ";
  print " a.probtable:hover {   cursor:help; } ";

  print " td.attinfo span  { display:none;  position:absolute; left:5em; } "
  print " td.attinfo:hover span  { display:block; background-color:#FFFFC5; color:#000000; font-size:10pt; cursor:help; text-decoration:none; font-weight:normal; cursor:help; width:600pt;padding:3px; border:1px solid #000000; padding:3px;} ";
  print " td.attinfo:hover {   cursor:help; } ";
  print " a.attinfo span  { display:none;  position:absolute; left:5em;  } "
  print " a.attinfo:hover span  { display:block; background-color:#FFFFC5; color:#000000; font-size:10pt; cursor:help; text-decoration:none; font-weight:normal; cursor:help; width:600pt;padding:3px; border:1px solid #000000; padding:3px; } ";
  print " a.attinfo:hover {   cursor:help; } ";

  print " a.amatrix3 span  { display:none;  position:absolute; left:30em; } ";
  print " a.amatrix3:hover span { display:block; background-color:#FFFFC5; color:#000000; font-size:10pt; cursor:help; text-decoration:none; font-weight:normal; cursor:help; width:400pt; border:1px solid #000000; padding:3px; } ";
  print " a.amatrix3:hover {   cursor:help; } ";

  print " .amatrixlarge { font-size:12pt; padding:8px; padding-left:1px;}";
  print " .amatrixmedium {font-size:10pt; padding:3px; padding-left:1px;}";
  print " .amatrixsmall {font-size:8pt; padding:1px;}";


  print " .tablepredict { font-family:Arial; color:#000000; background-color:#FFFFFF; width:100%; vertical-align:top;  font-size:10pt; padding: 1px 1px; padding-left:0pt; border:0px;text-decoration:none;  }";
  print " .popup { color:#000000; cursor:help; text-decoration:none;}";


  print "</style>";
  print "<SCRIPT LANGUAGE='javascript'>";
  print "<!--";
  print "function openNewWindow(address) {";
  print "   x=window.open (address, 'new', config='height=650, width=800, toolbar=no, menubar=no, scrollbars=yes, resizable=yes, location=no, directories=no, status=no');"
  print "  x.focus();";
  print " };"
  print "function openHelpWindow(address) {";
  print "   x=window.open (address, 'help', config='height=600, width=800, toolbar=no, menubar=no, scrollbars=yes, resizable=yes, location=no, directories=no, status=no');"
  print "  x.focus();";
  print " };"
  print "function openExternalWindow(address) {";
  print "   x=window.open (address, 'external', config='height=600, width=800, toolbar=no, menubar=no, scrollbars=yes, resizable=yes, location=no, directories=no, status=no');"
  print "  x.focus();";
  print " };"
  print "function openNewPage(address) {";
  print "   this.document.open(address);"
  print " };"
  print "-->";
  print "</SCRIPT>";

  print "</HEAD></HTML>";


def __print_head():
  print "<BODY bgcolor=#DDDDDD>";
  print "<center>";
  print "<TABLE bgcolor=#FFFFFF border=0 width=95% height=95%>";
  print "<TR height=80pt><TD width=150 style='padding-left:20pt'><img src='" + str(img_path) + "multiloc2.png' width='300'></TD>";
  print "<TD width=100% style='vertical-align:middle; padding:0px; padding-left:20pt;'><h2>Integrating phylogeny and Gene Ontology terms into Subcellular Protein Localization Prediction</h2></TD></TR>";
  print "<TR><TH colspan=2 width=100% height=40pt>";
  print "<div id='navi'>"

  class_list = ["","","",""];

  if not form.has_key("page"):
    class_list[0] = "class='current'";
  elif form["page"].value=="info":
    class_list[1] = "class='current'";
  elif form["page"].value=="imprint":
    class_list[2] = "class='current'";
  elif form["page"].value=="gdpr":
    class_list[3] = "class='current'";
  else:
    class_list[0] = "class='current'";

  print "<a "+class_list[0]+" href='webloc.cgi'>Predict with MultiLoc2</a>";
  print "<a "+class_list[1]+" href='webloc.cgi?page=info'>Information</a>";
  print "<a "+class_list[2]+" href='webloc.cgi?page=imprint'>Impressum</a>";
  print "<a "+class_list[3]+" href='webloc.cgi?page=gdpr'>Datenschutzerklaerung</a>";
  print "</div></TH></TR>"
  print "<TR><TH colspan=2 height=80% style='padding-left:30pt;'>";


def __print_foot():
  print "</TH></TR>";
  print "<TR><TH colspan=2 bgcolor=#FFFFFF>"
  print "<hr>";
  print "<BR><p style='font-size:8pt;'>";
  print "Contact: mail to <a style='font-size:8pt;' href=mailto:" + contact_email + ">MultiLoc2 Admin</a></p>";
  print "</TH></TR>"
  print "</TABLE>";
  print "</BODY></HTML>";


def __print_start_screen(error_msg = ""):
  __print_header();
  __print_head();

  print "<form name=yloc enctype='multipart/form-data' action='webloc.cgi' method='post'>";

  if error_msg != "":
    print "<p style='color:#FF0000;'><b>An error occured: " + error_msg + "</b></p>";

  print "<table style='border:1px solid #cbdbff;width:100%;'><tr><td>"
  print "Choose prediction method:<BR>";
  print "</td></tr></table><BR>";

  print "<select name='pred_method' size=1>";
  print "<option value='1'>MultiLoc2-LowRes (Animal), 4 Localizations</option>"
  print "<option value='2'>MultiLoc2-LowRes (Fungal), 4 Localizations</option>"
  print "<option value='3'>MultiLoc2-LowRes (Plant), 5 Localizations</option>"
  print "<option value='4'>MultiLoc2-HighRes (Animal), 9 Localizations</option>"
  print "<option value='5'>MultiLoc2-HighRes (Fungal), 9 Localizations</option>"
  print "<option value='6'>MultiLoc2-HighRes (Plant), 10 Localizations</option>"
  print "</select><BR><BR><BR><BR>";

  print "<table style='border:1px solid #cbdbff;width:100%;'><tr><td>"
  print "Paste your amino acid sequence(s) in fasta format (maximum 20 sequences):<BR>";
  print "</td></tr></table><BR>";

  print "<textarea class=input name='plain_sequence' cols=100 rows=10></textarea><BR>";
  print "<BR>OR<BR><BR>"
  print "Upload a FASTA file (maximum 20 sequences): <input type='file' name='fastafile' size='60'><BR><BR><BR><BR>"

  print "<input type='hidden' name='page' value='predict'>";
  print "<input class=button type='submit' name='Submit' value='Predict'>";
  print "</form><BR><BR><BR>";

  print "<form enctype='multipart/form-data' action='webloc.cgi' method='post'>";
  print "<table style='border:1px solid #cbdbff;width:100%;'><tr><td>"
  print "To search for the results of a previous prediction enter the query ID.";
  print "</td></tr></table><BR>";
  print "Query ID: <input name=id type=text size=40></input>";
  print "<input type='hidden' name='page' value='predicted'>";
  print "<input  class=button  type='submit' name='Submit' value='Search'>";
  print "</form>";

  __print_foot();


"""
Intermediate Screen
"""
def __print_intermediate_screen(id, seqs_n=0):
  __print_header(seqs_n*10, id);
  __print_head();

  print "<h2>Prediction in progress</h2>";

  print "Query ID: " + str(id) + "<BR><BR>";

  if seqs_n:
    print "Number of Sequences: " + str(seqs_n) + "<BR><BR>";

  print "<b>Please wait while MultiLoc2 is processing.</b><BR>";
  print "This page refreshes automatically.<BR><BR>";
  print "Alternatively note your Query ID and come back later.<BR>"

  __print_foot();


def __print_result_screen(id):
  __print_header();
  __print_head();

  # Fetch predicion results
  out_f = open(__job_file_path(id + "__result"), "r")
  results = out_f.read().split("\n")
  out_f.close()

  print "<h2>MultiLoc2 prediction results.</h2><BR>";

  print "<p>Predictor: " + results[2].split("=")[1].strip() + "</p>";
  print "<p>Origin: "    + results[3].split("=")[1].strip() + "</p><BR>";

  for i in results[4:]:
    print "<p>" + i.strip() + "</p>"

  __print_foot();


"""
Decision whether waiting screen is printed or result screen is shown.
"""
def __printResultOrWaitingScreen(id):
  try:
    job_status = __job_status(id)
    if job_status == "finished":
      # Job is finished
      __print_result_screen(id);
    elif job_status == "pending":
      # Job is pending
      __print_intermediate_screen(id);
    else:
      # Job is does not exist
      __print_start_screen("Could not find a query with ID " +str(id));
  except:
    print "\n\n<PRE>"
    traceback.print_exc()


def __validate_sequence_input(id, seqs):
  # Write input sequences to fasta file
  seqs_file = __job_file_path(id + "__input.fasta")
  f = open(seqs_file, "w")
  f.write(seqs)
  f.close()

  records = []

  error_msg = ""
  for record in SeqIO.parse(seqs_file, "fasta"):
    if len(records) > __max_input_seqs():
      error_msg = "ERROR: Please do not submit more than " + str(__max_input_seqs()) + " FASTA sequences."
      break;
    if len(record.id) == 0:
      error_msg = "ERROR: Please give every FASTA record a name."
      break;
    if len(record.seq) == 0:
      error_msg = "ERROR: Input contained empty FASTA records."
      break;
    else:
      record.seq = record.seq.upper()
      my_seq = Seq(str(record.seq), IUPAC.protein)
      if not _verify_alphabet(my_seq):
        error_msg = "ERROR: Input contained non-protein or invalid FASTA records."
        break;

      records.append(record)

  if len(error_msg):
    os.remove(seqs_file);
    return (0, error_msg)
  else:
    SeqIO.write(records, seqs_file, "fasta")
    return (len(records), "")


def __start_ml2_prediction(id, origin, predictor):
  try:
    job_status_file = __job_file_path(id)
    os.mknod(job_status_file)

    job_log_file = __job_file_path(id + "__log")

    in_f       = __job_file_path(id + "__input.fasta")
    out_f      = __job_file_path(id + "__result")
    ips_f      = __job_file_path(id + "__ips.out")

    command = "/MultiLoc2/run_multiloc2_ws.sh " + in_f + " " + origin + " " + predictor + " " + out_f + " " + ips_f + " " + job_status_file + " " + __job_dir() + " > " + job_log_file + " & "

    tmp = open(__job_file_path(id + "__ml2_call"), "w")
    tmp.write(command)
    tmp.close()

    os.system(command)
  except:
    print "\n\n<PRE>"
    traceback.print_exc()


def __print_prediction_page():
  try:
    # Check if only one input method hast been selected
    pasted = form["plain_sequence"].value
    file_name = form['fastafile'].filename

    seqs = ""

    if len(pasted):
      if file_name:
        __print_start_screen("Please choose only one sequence input option: Texfield or File. You have been redirected to the start page.");
        return;
      else:
        seqs = pasted
    else:
      if file_name:
        seqs = form["fastafile"].file.read();
      else:
        __print_start_screen("Sequence input missing. You have been redirected to the start page.");
        return;

    id = __createID();
    result = __validate_sequence_input(id, seqs);

    if result[0]:
      pred_method = int(form['pred_method'].value)

      if pred_method==1 or pred_method==2 or pred_method==3:
        predictor = "LowRes"
      else:
        predictor = "HighRes"

      if pred_method==1 or pred_method==4:
        origin = "animal"
      elif pred_method==5 or pred_method==5:
        origin = "fungal"
      else:
        origin="plant"

      __start_ml2_prediction(id, origin, predictor);
      __print_intermediate_screen(id, result[0]);
      return;
    else:
      __print_start_screen(result[1]);
      return;

  except:
    print "\n\n<PRE>"
    traceback.print_exc()


def __print_error(error_msg):
  print "<p><b><font color=#FF0000>An error occured: "+error_msg+"</b></p>";


def __blastp_version_info():
  try:
    p = Popen("blastp -version", shell=True, stdout=PIPE, stderr=PIPE);
    blastp_v, stderr  = p.communicate();

    print "<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + blastp_v.split("\n")[0].strip() + "</p>";
    print "<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + blastp_v.split("\n")[1].strip() + "</p>";
  except:
    if os.getenv("MULTILOC2_DEBUG"):
      print "\n\n<PRE>"
      traceback.print_exc()
    else:
      print "<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Cannot detect BLASTp version</p>";


def __libsvm_version_info():
  try:
    p = Popen("dpkg -s libsvm-tools", shell=True, stdout=PIPE, stderr=PIPE);
    stdout, stderr = p.communicate();

    version_info = ""
    tmp = stdout.split("\n")
    for line in tmp:
      if line.startswith("Version"):
        version_info = line.strip()

    if len(version_info):
      print "<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + version_info + "</p>";
    else:
      print "<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Cannot detect LIBSVM version</p>";
  except:
    if os.getenv("MULTILOC2_DEBUG"):
      print "\n\n<PRE>";
      traceback.print_exc();
    else:
      print "<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Cannot detect LIBSVM version</p>";


def __interproscan_version_info():
  try:
    if os.getenv("INTERPROSCAN"):
      ips_path = os.path.join(os.getenv("INTERPROSCAN"), "interproscan.sh");
      p = Popen(ips_path + " -version", shell=True, stdout=PIPE, stderr=PIPE);
      stdout, stderr = p.communicate();

      print "<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + stdout.split("\n")[0].strip() + "</p>";
      print "<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + stdout.split("\n")[1].strip() + "</p>";
    else:
      print "<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Cannot detect InterProScan version</p>";
  except:
    if os.getenv("MULTILOC2_DEBUG"):
      print "\n\n<PRE>"
      traceback.print_exc()
    else:
      print "<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Cannot detect InterProScan version</p>";


def __print_info_page():
  __print_header();
  __print_head();

  print "<h2>How to Cite</h2>";
  print "<p>&nbsp;&nbsp;&nbsp;&nbsp;Blum, T.; Briesemeister, S. and Kohlbacher, O. (2009).</p>";
  print "<p>&nbsp;&nbsp;&nbsp;&nbsp;<a href='http://dx.doi.org/10.1186/1471-2105-10-274' style='color:blue' target='_blank'>MultiLoc2: integrating phylogeny and Gene Ontology terms improves subcellular protein localization prediction.</a></p>";
  print "<p>&nbsp;&nbsp;&nbsp;&nbsp;BMC Bioinformatics, 10:274</p><BR>";
  print "&nbsp;&nbsp;&nbsp;&nbsp;Supplementary Material: <a href='" + download_path + "MultiLoc2_supplementary_material.pdf' style='color:blue' target='_blank'>MultiLoc2_supplementary_material.pdf</a>"
  print "<BR><BR><BR>";

  print "<h2>License</h2>";
  print "<p>&nbsp;&nbsp;&nbsp;&nbsp;MultiLoc2 is distributed under the GNU General Public License (GPL).</p>";
  print "<p>&nbsp;&nbsp;&nbsp;&nbsp;MultiLoc2 is using LIBSVM, BLAST, and InterProScan. These software tools have their own license terms.</p>";
  print "<BR><BR>";

  print "<h2>Third Party Software Tools</h2>";
  print "<p>&nbsp;&nbsp;&nbsp;&nbsp;MultiLoc2 is implemented in Python 2.7 and uses LIBSVM, BLAST, and optionally InterProScan.</p>";
  print "<p>&nbsp;&nbsp;&nbsp;&nbsp;LIBSVM Version Info:</p>";
  __libsvm_version_info();
  print "<p>&nbsp;&nbsp;&nbsp;&nbsp;BLAST Version Info:</p>";
  __blastp_version_info();
  print "<p>&nbsp;&nbsp;&nbsp;&nbsp;InterProScan Version Info:</p>";
  __interproscan_version_info();
  print "<BR><BR>";

  print "<h2>Run MultiLoc2 Locally</h2>";
  print "<p>&nbsp;&nbsp;&nbsp;&nbsp;MultiLoc2 is available as a repository to build a docker image, which also includes this websever: <a href='https://github.com/KohlbacherLab/MultiLoc2' style='color:blue' target='_blank'>MultiLoc2 at KohlbacherLab GitHub</a></p>";
  print "<BR>";
  print "<p>&nbsp;&nbsp;&nbsp;&nbsp;Please note:</p>";
  print "<p>&nbsp;&nbsp;&nbsp;&nbsp;Using other versions of third party software tools, especially of BLAST and InterProScan, in your local installation may result in slightly different prediction scores compared to those calculated by the online service.</p>";
  print "<BR><BR>";

  print "<h2>Data Sets</h2>";
  print "<BR><BR><BR>";

  __print_foot();


def __print_imprint_page():
  __print_header();
  __print_head();

  print "<h2>Impressum / Imprint</h2>";
  print '''<h3>Allgemeine Informationen gem. &sect; 5 TMG, &sect; 55 RStVG</h3>
  <table>
  <tbody>
  <tr>
  <td>Adresse</td>
  <td>
  <p>Eberhard Karls Universit&auml;t T&uuml;bingen</p>
  <p>Geschwister-Scholl-Platz</p>
  <p>72074 T&uuml;bingen</p>
  </td>
  </tr>
  <tr>
  <td><br /></td>
  <td>Die Universit&auml;t T&uuml;bingen ist eine K&ouml;rperschaft des &ouml;ffentlichen Rechts. Sie wird durch den Rektor Prof. Dr. Bernd Engler (eMail: bernd. engler [at] uni-tuebingen.de) gesetzlich vertreten</td>
  </tr>
  <tr>
  <td>Telefonzentrale</td>
  <td>+49 (0) 70 71/29-0</td>
  </tr>
  <tr>
  <td>Fax Zentrale Verwaltung</td>
  <td>+49 (0) 70 71/29-59 90</td>
  </tr>
  <tr>
  <td>Internet-Adresse</td>
  <td><a href="https://www.uni-tuebingen.de/">https://www.uni-tuebingen.de</a></td>
  </tr>
  <tr>
  <td>Umsatzsteuer-Identifikationsnummer</td>
  <td>
  <p>gem&auml;&szlig; &sect; 27a Umsatzsteuergesetz:&nbsp;<strong>DE812383453</strong></p>
  </td>
  </tr>
  <tr>
  <td>Aufsichtsbeh&ouml;rde</td>
  <td>Ministerium f&uuml;r Wissenschaft, Forschung und Kunst Baden-W&uuml;rttemberg</td>
  </tr>
  </tbody>
  </table>

  <h3>1. Externe Links</h3>
  <p>Diese Webseite der Universit&auml;t T&uuml;bingen enth&auml;lt auch entsprechend gekennzeichnete Links oder Verweise auf Websites Dritter. Durch den Link vermittelt die Universit&auml;t T&uuml;bingen lediglich den Zugang zur Nutzung dieser Inhalte. Eine Zustimmung zu den Inhalten den verlinkten Seiten Dritter ist damit nicht verbunden. Die Universit&auml;t T&uuml;bingen &uuml;bernimmt daher keine Verantwortung f&uuml;r die Verf&uuml;gbarkeit oder den Inhalt solcher Websites und keine Haftung f&uuml;r Sch&auml;den oder Verletzungen, die aus der Nutzung, gleich welcher Art, solcher Inhalte entstehen. Hierf&uuml;r haftet allein der Anbieter der jeweiligen Seite.&nbsp;&nbsp;</p>

  <p>Bei der erstmaligen Verkn&uuml;pfung mit einem anderen
  Internetangebot hat die Redaktion dessen Inhalt daraufhin &uuml;berpr&uuml;ft, ob
  durch ihn eine m&ouml;gliche zivilrechtliche oder strafrechtliche
  Verantwortlichkeit ausgel&ouml;st wird. Dort nachtr&auml;glich eingebundene
  Inhalte k&ouml;nnen jedoch leider nicht &uuml;berpr&uuml;ft werden. Der Verweis auf
  dieses Angebot wird unverz&uuml;glich aufgehoben werden, sobald die Redaktion feststellt oder von anderen darauf hingewiesen wird, dass ein
  bestimmtes Angebot, zu dem ein Link bereitgestellt wurde, eine zivil-
  oder strafrechtliche Verantwortlichkeit ausl&ouml;st.</p>

  <h3>2.&nbsp;Urheberrecht</h3>
  <p>Copyright (c), Universitaet T&uuml;bingen. Alle Rechte vorbehalten.</p>
  <p>Alle auf dieser Website ver&ouml;ffentlichten Inhalte (Layout, Texte, Bilder, Grafiken, Video- und Tondateien usw.) unterliegen dem Urheberrecht. Jede vom Urheberrechtsgesetz nicht zugelassene Verwertung bedarf vorheriger ausdr&uuml;cklicher Zustimmung der Universit&auml;t T&uuml;bingen. Dies gilt insbesondere f&uuml;r Vervielf&auml;ltigung, Bearbeitung, &uuml;bersetzung, Einspeicherung, Verarbeitung bzw. Wiedergabe von Inhalten in Datenbanken oder anderen elektronischen Medien und Systemen. Fotokopien und Downloads von Web-Seiten f&uuml;r den privaten, wissenschaftlichen und nicht kommerziellen Gebrauch d&uuml;rfen hergestellt werden.</p>
  <p>Das Urheberrecht f&uuml;r die Wort-Bild-Marke liegt ausdr&uuml;cklich bei der Universit&auml;t T&uuml;bingen.</p>
  <p>Wir erlauben ausdr&uuml;cklich und begr&uuml;&szlig;en das Zitieren unserer Dokumente und Webseiten sowie das Setzen von Links auf unsere Website.</p>

  <h3>3.&nbsp;Haftungsausschluss</h3>
  <p>Die Informationen auf dieser Website wurden nach bestem Wissen und Gewissen sorgf&auml;ltig zusammengestellt und gepr&uuml;ft. Es wird jedoch keine Gew&auml;hr, weder ausdr&uuml;cklich noch stillschweigend, f&uuml;r die Vollst&auml;ndigkeit, Richtigkeit oder Aktualit&auml;t sowie die jederzeitige Verf&uuml;gbarkeit der bereit gestellten Informationen &uuml;bernommen. Eine Haftung f&uuml;r Sch&auml;den, die aus der Nutzung oder Nichtnutzung der auf dieser Website angebotenen Informationen entstehen ist, soweit gesetzlich zul&auml;ssig, ausgeschlossen.</p>

  <h3>Ansprechpartner</h3>
  <p>Prof. Dr. Oliver Kohlbacher<br />Sand 14<br />72076 T&uuml;bingen<br />Telefon: +49-7071-29-70458<br />Fax: +49-7071-29-5152<br />eMail: oliver. kohlbacher [at] uni-tuebingen.de</p>
  ''';

  __print_foot();

def __print_gdpr_page():
  __print_header();
  __print_head();

  print "<h2>Datenschutzerklaerung / GDPR Disclaimer</h2>";

  __print_foot();


# ### Main ###

form=cgi.FieldStorage()

try:
  if not (form.has_key("page") or form.has_key("id")):
    __print_start_screen();
  elif form.has_key("id"):
    __printResultOrWaitingScreen(form["id"].value);
  elif form.has_key("page"):
    if form["page"].value == "predict":
      __print_prediction_page();
    elif form["page"].value == "info":
      __print_info_page();
    elif form["page"].value == "imprint":
      __print_imprint_page();
    elif form["page"].value == "gdpr":
      __print_gdpr_page();
    else:
      __print_start_screen("Unkown value of parameter 'page'. You have been redirected to the start page.");
except:
  print "\n\n<PRE>"
  traceback.print_exc()
