
import pandas as pd
import matplotlib.pyplot as plt


KC_Distribution=True

if KC_Distribution:

    kc_section_mapping = "data/kc_section_mapping.csv"
    df_kc_mapping = pd.read_csv(kc_section_mapping, delimiter=",", header=0)
    section_dict={}
    step_dict={}
    kc_types = set()

    for index,row in df_kc_mapping.iterrows():
        kc_types.add(df_kc_mapping.loc[index]['kc'].split("_")[0].lower())
        kc = df_kc_mapping.loc[index]['kc'].split("_")[0].lower()

    kc_step_count={}
    kc_section_count={}

    for kc in kc_types:
        df_sub = df_kc_mapping[(df_kc_mapping['kc'].str.startswith(kc))]

        kc_step_count[kc] = len(df_sub)
        kc_section_count[kc] = len(set(list(df_sub['sectionid'])))

    # plt.bar(kc_step_count.keys(),kc_step_count.values())
    # plt.xlabel('kc types')
    # plt.ylabel('# of steps')
    # plt.title('KC Step distribution')
    # plt.grid(True)
    # plt.xticks(rotation='vertical')
    # plt.show()


    plt.bar(kc_section_count.keys(),kc_section_count.values())
    plt.xlabel('kc types')
    plt.ylabel('# of sections')
    plt.title('KC Section distribution')
    plt.xticks(rotation='vertical')
    plt.grid(True)
    plt.show()



# if DRAW_READ_DIST:
#
#
#     # df_pr_readinglogs.to_csv(fprocessed_logs, sep='\t', encoding='utf-8')
#     durationspent = df_pr_readinglogs[(df_pr_readinglogs['eventType']=='Do') & (df_pr_readinglogs['accuracy'] < 0.5) ]['readingDuration']
#     n, bins, patches = plt.hist(durationspent,10)
#     plt.xlabel('reading time spent')
#     plt.ylabel('# of Observations')
#     plt.title('Histogram of Accuracy < 0.5')
#     plt.grid(True)
#     plt.show()
