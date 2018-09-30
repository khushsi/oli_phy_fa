
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

KC_Distribution=True
book = "data/book.csv"
if KC_Distribution:

    kc_section_mapping = "data/kc_question_step_mapping.csv"
    df_kc_mapping = pd.read_csv(kc_section_mapping, delimiter=",", header=0)
    df_book = pd.read_csv(book, delimiter=",", header=0)
    kc_reading_step_count={}
    for index,row in df_book.iterrows():
        for kc in str(row['kclist']).split(","):
            kc_reading_step_count[kc+"_SKILL"]=0

    section_dict={}
    step_dict={}
    kc_types = set()

    for index,row in df_kc_mapping.iterrows():
        kc_types.add(df_kc_mapping.loc[index]['kc'].split("_")[0].lower())
        kc = df_kc_mapping.loc[index]['kc'].split("_")[0].lower()
        if row['kc'] in kc_reading_step_count:
            kc_reading_step_count[row['kc']] += 1

    kc_step_count={}
    kc_section_count={}
    for kc in kc_types:
        df_sub = df_kc_mapping[(df_kc_mapping['kc'].str.startswith(kc))]
        kc_step_count[kc] = len(df_sub)
        kc_section_count[kc] = len(set(list(df_sub['questionid'])))



    # plt.bar(kc_step_count.keys(),kc_step_count.values())
    # plt.xlabel('kc types')
    # plt.ylabel('# of steps')
    # plt.title('KC Step distribution')
    # plt.grid(True)
    # plt.xticks(rotation='vertical')
    # plt.show()
    #
    #
    # plt.bar(kc_section_count.keys(),kc_section_count.values())
    # plt.xlabel('kc types')
    # plt.ylabel('# of sections')
    # plt.title('KC Section distribution')
    # plt.xticks(rotation='vertical')
    # plt.grid(True)
    # plt.show()

    # print("Total reading KCs" ,len(kc_reading_step_count)-1)
    # print("Total Tested reading KCs", len( [kc for kc in kc_reading_step_count if kc_reading_step_count[kc] !=0] ))
    # plt.bar([ kc.replace("_SKILL","") for kc in kc_reading_step_count.keys()],kc_reading_step_count.values())
    # plt.xlabel('kc types')
    # plt.ylabel('# of steps')
    # plt.title('KC Step distribution for Reading KCs')
    # plt.grid(True)
    # plt.xticks(rotation='vertical')
    # plt.show()

    abc = kc_reading_step_count.values()
    # print(abc)
    # n, bins, patches = plt.hist(abc,20)
    # plt.xlabel('No of times tested on practice activities')
    # plt.ylabel('# of Reading Skills')
    # # plt.title('KC Step distribution for Reading KCs')
    # plt.grid(True)
    # plt.xticks(rotation='vertical')
    # plt.show()


    # plt.xlabel('kc types')
    # plt.ylabel('# of sections')
    # plt.title('KC Section distribution')
    # plt.xticks(rotation='vertical')
    # plt.grid(True)
    # plt.show()


# if DRAW_READ_DIST:
#
#
#     df_pr_readinglogs.to_csv(fprocessed_logs, sep='\t', encoding='utf-8')
#     durationspent = df_pr_readinglogs[(df_pr_readinglogs['eventType']=='Do') & (df_pr_readinglogs['accuracy'] < 0.5) ]['readingDuration']
#     n, bins, patches = plt.hist(durationspent,10)
#     plt.xlabel('reading time spent')
#     plt.ylabel('# of Observations')
#     plt.title('Histogram of Accuracy < 0.5')
#     plt.grid(True)
#     plt.show()

steplogfile = 'data/ds863_student_step_All_Data_2287_2015_0813_191857.tsv'

fprocessed_logs = "data/preadinglogs.tsv"

df_preadinglogs = pd.read_csv(fprocessed_logs, header=0, delimiter='\t')
df_steplogs = pd.read_csv(steplogfile, header=0, delimiter='\t')



df_preading_grp = df_preadinglogs[df_preadinglogs['eventType'] == 'Read'].groupby(['ds_anon_user_id','eventType']).count()
df_step_grp = df_steplogs.groupby(['Anon Student Id']).count()
student_activity_count={}
studentlist = set()
stepCount = []
readCount= []
student_wise_avg_readtime = {}
for index in df_preading_grp.index:
    student_activity_count[index[0]+"_R"] = df_preading_grp.loc[index]['action']
    studentlist.add(index[0])
    readCount.append(df_preading_grp.loc[index]['action'])


df_preadinglogs_282 = pd.read_csv(open("/Users/khushboo/Workspace/cmu Project/OLI_PHYC_Project/code/oli_phy_fa/data/merged_step_read_file_readkc-283.csv"),header=0)

df_preadinglogs_282['result'] = np.where(df_preadinglogs_282['correct'] == 'correct',1,0)

df_preading_grp1 = df_preadinglogs_282.groupby(['student_id']).mean()

for index in df_preading_grp1.index:
    print(index,",",df_preading_grp1.loc[index]['eventDuration'])

df_preading_grp2 = df_preadinglogs[df_preadinglogs['eventType'] == 'Do'].groupby(['ds_anon_user_id']).mean()

for index in df_preading_grp2.index:
    print(index,",",df_preading_grp2.loc[index]['accuracy'])


for index in df_step_grp.index:
    if index in studentlist:
        student_activity_count[index+"_A"] = df_step_grp.loc[index]['Problem Name']
        stepCount.append(df_step_grp.loc[index]['Problem Name'])

Read_dist=True
step_dist = True
if Read_dist:
    n, bins, patches = plt.hist(readCount,50)
    plt.xlabel('# of Readings done')
    plt.ylabel('# of Students')
    plt.title('Histogram of Studentwise Reading  Count')
    plt.grid(True)
    plt.show()

if step_dist:
    n, bins, patches = plt.hist(stepCount,10)
    plt.xlabel('# of Step / Activities done')
    plt.ylabel('# of Students')
    plt.title('Histogram of Studentwise  Activites Count')
    plt.grid(True)
    plt.show()

avg_read = np.mean(readCount)
avg_step = np.mean(stepCount)

median_read = np.median(readCount)
median_step = np.median(stepCount)


icount_avg = 0
icount_median = 0

for student_id in studentlist:
    if student_id+"_A" in student_activity_count and student_activity_count[student_id+"_A"] > avg_step and student_activity_count[student_id+'_R'] > avg_read:
        icount_avg += 1

    if student_id+"_A" in student_activity_count and student_activity_count[student_id+"_A"] >= median_step and student_activity_count[student_id+'_R'] >= median_read:
        icount_median += 1

print(avg_read,avg_step,icount_avg,icount_median )




#
#
#
#
# for index in df_step_grp.index:
#
#     if index[1]== 'Activity':
#         print(df_step_grp.loc[index]['item_id'])
#
# print(" Read :")
# for index in df_step_grp.index:
#     if index[1] == 'Read':
#         print(df_step_grp.loc[index]['item_id'])

