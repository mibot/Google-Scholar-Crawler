import re
from glob import glob
import pandas as pd

# dataPath = os.path.abspath(os.path.relpath('data'))

# df = pd.read_csv("data/papers_62.csv", sep="\t", encoding="utf-8")

dfs = []


def merge():
    path = "data/csv"
    filenames = glob(path + "/*.csv")
    filenames.sort()
    # sorted(filenames, key=str)
    for file in filenames:
        df = pd.read_csv(file, index_col=None, header=0, sep="\t", encoding="utf-8")
        dfs.append(df)

    df_merged = pd.concat(dfs, axis=0, ignore_index=True)
    df_final = df_merged.sort_values('query_id')

    df_final.to_csv("data/csv/resolved_papers.csv", index=None, encoding='utf-8', sep="\t")

    return "File merged..!"


def removeDuplicate():
    df = pd.read_csv("data/csv/resolved_papers.csv", sep="\t", encoding="utf-8")

    df_unique = df
    df_unique.drop_duplicates(subset=['title', 'authors'], keep='first', inplace=True)

    # df_unique = df.drop_duplicates(subset=['title', 'author'], keep=False)

    df_unique.to_csv("data/csv/resolved_papers_unique_v2.csv", index=None, encoding='utf-8', sep="\t")

    return "Row duplicates deleted..!!"


def removeBooksGoogle():
    # toRemove = "/books.google.com/books?"
    toRemove = "books.google.com"
    df = pd.read_csv("data/csv/resolved_papers_unique.csv", sep="\t", encoding="utf-8", keep_default_na=False)
    indexNames = df[df['source'] == toRemove].index
    df.drop(indexNames, inplace=True)
    # df.reset_index(drop=True, inplace=True)

    df_final = df.reset_index(drop=True)
    df_final.index += 30059
    df_final.index.name = "id"

    df_final['year'] = df_final['year'].replace(to_replace='[^0-9]+', value='', regex=True)  # remove text from INT col

    df_final.to_csv("data/csv/resolved_papers_unique_id.csv", encoding='utf-8', sep="\t")

    return "File cleaned...!"


df1 = pd.read_csv("data/csv/resolved_papers_unique.csv", sep="\t", encoding="utf-8", keep_default_na=False)
df2 = pd.read_csv("data/csv/resolved_papers_unique_v2.csv", sep="\t", encoding="utf-8", keep_default_na=False)


df_merged = pd.concat([df1,df2], axis=0, ignore_index=True)

toRemove = "books.google.com"
indexNames = df_merged[df_merged['source'] == toRemove].index
df_merged.drop(indexNames, inplace=True)
df_merged.sort_values('query_id', inplace=True)
df_merged.reset_index(drop=True, inplace=True)

df_merged.drop_duplicates(subset=['title', 'authors'], keep=False, inplace=True)
df_merged.sort_values('query_id', inplace=True)
df_merged.reset_index(drop=True, inplace=True)

df_merged.index += 35134
df_merged.index.name = "id"

df_merged['year'] = df_merged['year'].replace(to_replace='[^0-9]+', value='', regex=True)  # remove text from INT col

df_merged.to_csv("data/csv/resolved_papers_unique_id_v2.csv", encoding='utf-8', sep="\t")

# import numpy as np
#
# clpd_slr2017 = pd.read_csv("clpd_slr2017.tsv", sep="\t", encoding="utf-8", dtype={"id": np.int32, 'query_id': np.int32, 'year': np.int32},
#                            quoting=2)
# df_clpd_slr2017 = clpd_slr2017.iloc[:, :4]
#
# clpd_slr2018 = pd.read_csv("data/resolved_papers_unique_id.csv", sep="\t", encoding="utf-8", keep_default_na=False)
# df_clpd_slr2018 = clpd_slr2018.iloc[:, :4]
#
# df_merged = pd.merge(df_clpd_slr2017,df_clpd_slr2018, indicator=True, how='outer').query('_merge=="left_only"').drop('_merge', axis=1)
#
# df_merged = pd.concat([df_clpd_slr2017, df_clpd_slr2018], axis=0, ignore_index=True)
# df_unique = df_merged.drop_duplicates(subset=['title', 'authors'], keep=False)
# df_unique.to_csv("data/resolved_papers_unique_removed.csv", index=None, encoding='utf-8', sep="\t")
# def addId():
#     with open(os.path.join(dataPath, 'results', 'resolved_query_unique.csv'), 'rb') as f:
#         with open(os.path.join(dataPath, 'results', 'resolved_query_unique_id.csv'), 'wb') as g:
#             reader = UnicodeReader(f)
#             writer = UnicodeWriter(g)
#             count = 1
#             for row in reader:
#                 writer.writerow(str(count).split() + row)
#                 count += 1
#     f.close()
#     g.close()
#     return "Id added"
