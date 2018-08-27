from __future__ import division
from lxml import etree as ElementTree
import nltk
from bs4 import BeautifulSoup
from nltk import word_tokenize
import pandas as pd
import re


#Directories
courseDir="/Users/khushboo/Workspace/cmu Project/v_1_4 org/"
contentDir =courseDir + "content/"

#StreamLogs File
readinglogfile = 'data/eventStream_MOOC.tsv'
kc_mapping_performance_file = 'data/kc_question_step_mapping.tsv'
steplogfile = 'data/ds863_student_step_All_Data_2287_2015_0813_191857.tsv'

#output Files
file_post_quizzes = "data/sectionwise_post_quizzes.csv"
file_learning_objectives = "data/kc_learning_objectivies.csv"
inline_step_text= "data/inline_assesment.csv"
file_question_section="data/question_section_mapping.csv"
newbook = 'data/book.csv'
fprocessed_logs = "data/preadinglogs.tsv"
kc_question_step_mapping = "data/kc_question_step_mapping.csv"
qmatrix_predefined_kc = "data/kc_qmatrix_predifined_kc.csv"
step2qmatrixid="data/step2qid.csv"
kc2qmatrixid="data/kc2qid.csv"
# ques2qmatrixid ="data/section2aid.csv"
# qmatrix_predefined_sec="data/sec_qmatrix_predifined_kc.csv"

parser = ElementTree.XMLParser(recover=True)

# for child in root:
#     print(child.tag)
all = True

import csv
import os
mpsectiontext = {}

import numpy as np
import pandas as pd
import sklearn
import os.path
import matplotlib.pyplot as plt
import numpy as np


# DRAW_FIRST_ATTEMPT_SUCCESS = False
# DRAW_ALL_ATTEMPT_SUCCESS = False
# DRAW_LAST_ATTEMPT_SUCCESS = False
# DRAW_FIRST_IS_LAST=False
# DRAW_QUESTION_WISE_ATTEMPT=False
# DRAW_READ_DIST=True
# DRAW_READING_GROUPS = True
# DRAW_LEARNING_CURVE=False
# DRAW_LEARNING_CURVE_READING = False


# if  not os.path.isfile(booklenfile):
#     csvwriter = csv.writer(open(booklenfile,'w'),delimiter=',',)
#     csvwriter.writerow(["sectionid","length"])
#     bookstring = open("book.xml", 'r').read()
#     # print(bookstring)
#     tree = ElementTree.parse(open("book.xml", 'r'), parser)
#     root = tree.getroot()
#     print(root.tag)
#
#     for workbookpage in root.iter("workbook_page"):
#
#         if all == True or workbookpage.get("id") == "Methods-ScientificMethod-Text_4":
#             # print(workbookpage.attrib)
#             # print(workbookpage.find("head/title").text)
#             xmlstrhead = ElementTree.tostring(workbookpage.find("head"), encoding='utf8', method='xml')
#             xmlstrbody = ElementTree.tostring(workbookpage.find("body"), encoding='utf8', method='xml')
#
#             soup = BeautifulSoup(xmlstrhead)
#             headtext = soup.get_text()
#             # print(headtext)
#             # print("-----")
#             soup = BeautifulSoup(xmlstrbody)
#             bodytext = soup.get_text()
#             totaltextlen = len(word_tokenize(headtext)) + len(word_tokenize(bodytext))
#             # print(totaltextlen,workbookpage.get("id"))
#             csvwriter.writerow([workbookpage.get("id"),totaltextlen])
#Creating Book text and kc list
if  not os.path.isfile(newbook):
    csvwriter = csv.writer(open(newbook,'w'),delimiter=',',)
    csvwriter.writerow(["unitid","moduleid","sectionid","text","length","title","kclist"])
    bookstring = open("book.xml", 'r').read()
    # print(bookstring)
    tree = ElementTree.parse(open("book.xml", 'r'), parser)
    root = tree.getroot()
    print(root.tag)

    for workbookpage in root.iter("workbook_page"):
        objlist = []
        if all == True :
            # print(workbookpage.attrib)
            # print(workbookpage.find("head/title").text)
            xmlstrhead = ElementTree.tostring(workbookpage.find("head"), encoding='utf8', method='xml')
            xmlstrbody = ElementTree.tostring(workbookpage.find("body"), encoding='utf8', method='xml')
            xmlstrtitle = ElementTree.tostring(workbookpage.find("head/title"), encoding='utf8', method='xml')
            for node in workbookpage.findall("head/objref"):
                objlist.append(node.attrib['idref'])

            soup = BeautifulSoup(xmlstrhead)
            headtext = soup.get_text()
            soup = BeautifulSoup(xmlstrbody)
            bodytext = soup.get_text()
            soup = BeautifulSoup(xmlstrtitle)
            titletext = soup.get_text()
            btext = headtext + " " + bodytext
            btext = re.sub("\s{2,}"," ",btext.replace("\n"," ").replace("\t"," ").strip())
            print(workbookpage.get("id"))
            unit=workbookpage.get("id").split("-")[0].lower()
            module=workbookpage.get("id").split("-")[1].lower()

            totaltextlen = len(word_tokenize(btext))
            csvwriter.writerow([unit,module,workbookpage.get("id"),btext,totaltextlen,titletext.strip(),','.join(objlist)])

#Section wise question list
if  not os.path.isfile(file_question_section):
    csvwriter = csv.writer(open(file_question_section,'w'),delimiter=',',)
    csvwriter.writerow(["questionid","sectionid"])
    bookstring = open("book.xml", 'r').read()
    # print(bookstring)
    tree = ElementTree.parse(open("book.xml", 'r'), parser)
    root = tree.getroot()
    print(root.tag)

    for workbookpage in root.iter("workbook_page"):
        body = workbookpage.find("body")
        for ques in body.findall(".//wbinline"):

            csvwriter.writerow([ques.get("idref"),workbookpage.get("id")])

        # for sec in body.findall("section"):
        #     for ques in body.findall("wbinline"):
        #         print("here")
        #         csvwriter.writerow([ques.get("idref"),workbookpage.get("id")])

#Question Step to KC mapping
if( not os.path.isfile(kc_question_step_mapping)) :
    df_kc_mapping = pd.read_csv(kc_mapping_performance_file, delimiter="\t",header=0)
    kc_file = open(kc_question_step_mapping,'w')
    csvwriter = csv.writer(kc_file,delimiter=',',)
    csvwriter.writerow(["questionid","stepid","kc"])
    for index,row in df_kc_mapping.iterrows():
        if df_kc_mapping.loc[index]['KC (psychology-1.4)'].strip() != "":
            csvwriter.writerow([df_kc_mapping.loc[index]["Problem Name"],df_kc_mapping.loc[index]["Step Name"],df_kc_mapping.loc[index]["KC (psychology-1.4)"]])
    kc_file.close()

# Adding event Types, reading speed
df_question_section=pd.read_csv(file_question_section,header=0)

df_book_len = pd.read_csv(newbook, header=0)

df_kc_section_mapping = pd.read_csv(kc_question_step_mapping)

if( not os.path.isfile(fprocessed_logs)) :
    df_readinglogs = pd.read_csv(readinglogfile, delimiter="\t",header=0)
    df_readinglogs["textlen"] = 0
    df_readinglogs["sectionid"] = 0

    book_len={}
    for index,row in df_book_len.iterrows():
        book_len[df_book_len.loc[index]["sectionid"]] = df_book_len.loc[index]["length"]

    for index,row in df_question_section.iterrows():
        mpsectiontext[df_question_section.loc[index]["questionid"]] = df_question_section.loc[index]["sectionid"]

    for index,row in df_readinglogs.iterrows():
        if(df_readinglogs.loc[index]["eventType"] == "Read"):
            df_readinglogs.loc[index,"sectionid"] = df_readinglogs.loc[index]["info"].strip()
            df_readinglogs.loc[index,"texlen"] = book_len[df_readinglogs.loc[index]["info"].strip()]

        if(df_readinglogs.loc[index]["eventType"] == "Do"):
            df_readinglogs.loc[index,"sectionid"] = mpsectiontext[df_readinglogs.loc[index]["info"].strip()]
            # df_readinglogs.loc[index, "textlen"] = book_len[df_readinglogs.loc[index]["sectionid"]]

    df_readinglogs['nbwordsperduramin'] = df_readinglogs['eventDuration'] / df_readinglogs['texlen']

    #change format of start_time and end_time
    df_readinglogs['start_time'] = df_readinglogs.start_time.astype('datetime64[ns]')
    df_readinglogs['end_time'] = df_readinglogs.end_time.astype('datetime64[ns]')

    durationspent = []

    for index, row in df_readinglogs.iterrows():
        if (df_readinglogs.loc[index]['eventType'] == 'Do') and (df_readinglogs.loc[index]['accuracy'] <= 0.5):
            df_reading = df_readinglogs[(df_readinglogs['eventType'] == 'Read')
                                        & (
                                        df_readinglogs['ds_anon_user_id'] == df_readinglogs.loc[index]["ds_anon_user_id"])
                                        & (df_readinglogs['sectionid'] == df_readinglogs.loc[index]["sectionid"])
                                        & (df_readinglogs['end_time'] < df_readinglogs.loc[index]["start_time"])]
            readingtime = df_reading['eventDuration'].sum()
            df_readinglogs.loc[index,'readingDuration'] = readingtime
            df_readinglogs.loc[index,'readingSpeed'] = readingtime / book_len[df_readinglogs.loc[index]['sectionid']]
            # durationspent.append(readingtime)
    df_readinglogs.to_csv(fprocessed_logs, sep='\t', encoding='utf-8')


#qmatrix for predifined KCs
if( not os.path.isfile(qmatrix_predefined_kc)) :
    csvwriterqm = csv.writer(open(qmatrix_predefined_kc,'w'),delimiter=',',)
    # csvwriterqm_sec = csv.writer(open(qmatrix_predefined_sec,'w'),delimiter=',',)

    csvwriterkc = csv.writer(open(kc2qmatrixid,'w'), delimiter=',', )

    # csvwritersec = csv.writer(open(sec2qmatrixid, 'w'), delimiter=',', )
    # csvwritersec.writerow(["section"])

    csvwriterstep = csv.writer(open(step2qmatrixid,'w'), delimiter=',', )
    question_dict={}
    df_kc_mapping = pd.read_csv(kc_question_step_mapping, delimiter=",", header=0)
    kc_list=[]
    for index, row in df_kc_mapping.iterrows():
        if row['kc'] not in kc_list:
            csvwriterkc.writerow([row['kc']])
            kc_list.append(row['kc'])

    for index,row in df_kc_mapping.iterrows():
        csvwriterstep.writerow([row['questionid']+"_"+row['stepid']])
        if row['questionid'] not in question_dict:
            question_dict[row['questionid']] = []

        # print(row['kc'])
        row_kc = []
        row_kc = [1 if kc.strip() == row['kc'].strip() else 0 for kc in kc_list]
        question_dict[row['questionid']].append(row['kc'])
        # print(sum(row_kc))
        csvwriterqm.writerow(row_kc)

    #     csvwritersec.writerow([row['sectionid']])
    #     row_kc = []
    #     row_kc = [1 if kc.strip() in section_dict[key] else 0 for kc in kc_list]
    #     csvwriterqm_sec.writerow(row_kc)

# Learning Objectives
ln_obj_folder="/x-oli-learning_objectives/"
lbd_assessment="/x-oli-inline-assessment/"
if not os.path.isfile(file_learning_objectives):
    csvwriter = csv.writer(open(file_learning_objectives,'w'))
    csvwriter.writerow(['kc','objective'])

    for dir in os.listdir(contentDir):
        if os.path.isdir(contentDir+dir+ln_obj_folder):
            for subdir in os.listdir(contentDir+dir+ln_obj_folder):
                # print(bookstring)
                tree = ElementTree.parse(open(contentDir+dir+ln_obj_folder+subdir, 'r'), parser)
                root = tree.getroot()
                obj = root.findall("objective")
                for ob in obj:
                    # print(ob.text)
                    abc = ElementTree.tostring(ob, encoding='utf8', method='xml')
                    soup = BeautifulSoup(abc)
                    headtext = soup.get_text()
                    csvwriter.writerow([ob.attrib['id'],re.sub("\s{2,}"," ",headtext.replace("\n"," ").replace("\t"," ").strip())])

# step_dict = {}
# df_step = pd.read_csv(open(step2qmatrixid,"r"))
# for index,row in df_step.iterrows():
#     kc = row[0].split()
#     df_step[kc[0]+"_"+kc[1]]

if not os.path.isfile(inline_step_text):
    csvwriter = csv.writer(open(inline_step_text,'w'))
    csvwriter.writerow(['kc','objective'])

    for dir in os.listdir(contentDir):
        if os.path.isdir(contentDir+dir+lbd_assessment):
            for subdir in os.listdir(contentDir+dir+lbd_assessment):
                print(dir+lbd_assessment+subdir)
                tree = ElementTree.parse(open(contentDir+dir+lbd_assessment+subdir, 'r'), parser)
                root = tree.getroot()
                obj = root.findall("question")
                for ob in obj:
                    if not "_lbd_" in subdir :
                        qid = ob.attrib['id']
                        step = subdir.replace(".xml","") + "_" + qid
                        print(step)
                        # print(ob.text)
                        abc = ElementTree.tostring(ob, encoding='utf8', method='xml')
                        soup = BeautifulSoup(abc)
                        headtext = soup.get_text()
                        csvwriter.writerow([ob.attrib['id'],re.sub("\s{2,}"," ",headtext.replace("\n"," ").replace("\t"," ").strip())])

merged_step_read_file = 'data/merged_step_read_file1.csv'
if not os.path.isfile(merged_step_read_file):
    df_preadinglogs = pd.read_csv(fprocessed_logs,header=0,delimiter='\t')
    df_steplogs = pd.read_csv(steplogfile,header=0,delimiter='\t')
    keep = ['keep','tooFast']
    csvwriter = csv.writer(open(inline_step_text,'w'))
    csvwriter.writerow(['student_id','start_time','end_time','step_id','type','correct','reading_time'])

    for index,row in df_steplogs.iterrows():
        prevattempts = len(df_steplogs[(df_steplogs['Anon Student Id'] ==row['Anon Student Id'])
                                   & (df_steplogs['Step Start Time'] < row['Step Start Time'] )
                                   & (df_steplogs['Problem Name'] == row['Problem Name'])
                                   & (df_steplogs['Step Name'] == row['Step Name'])])
        if prevattempts > 0:
            print(prevattempts,index,row['Anon Student Id'],row['Problem Name'], row['Step Name'])

    for index,row in df_readinglogs.iterrows():
        if row['eventType'] == 'Read' and row['remove_possible'] in keep:
            csvwriter.writerow([row['ds_anon_user_id'],row['start_time'],row['end_time'],row['info'],row['eventType'],0,row['readingDuration']])

    # for index,row in df_steplogs.iterrows():
    #     csvwriter.writerow([row['Anon Student Id'],row['Step Start Time'],row['Step End Time'],row['']])










