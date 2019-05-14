#imports
import pandas as pd

#get data
df_grads = pd.read_excel('./Graduates.xlsx','Grads')
df_jobs = pd.read_excel('./Jobs.xlsx','Jobs')

#data consistency
res = pd.DataFrame()
df = df_grads.melt(id_vars=['gradid','vertical'], value_name='jobid')[['gradid','vertical','jobid']]
df.drop_duplicates(['gradid','jobid'], inplace=True)
df = df.merge(df_jobs, on=['jobid'], suffixes=['_current','_next'])
df = df[df['vertical_current']!=df['vertical_next']]

#create result
x = df.groupby('jobid')['jobid'].transform('size') <= df['capacity']
while len(x[x])>0:
    res = res.append(df[x])
    df = df.merge(res[['gradid']], on=['gradid'], indicator='i', how='outer').query('i == "left_only"').drop('i', 1)
    x = df.groupby('jobid')['jobid'].transform('size') <= df['capacity']

res.drop('capacity',1).sort_values('gradid').to_excel('./allocation.xlsx', index=False)
unalloc = df[['jobid','gradid']].reset_index().pivot(columns='jobid', values='gradid').transpose()
unalloc.to_excel('./unallocation.xlsx')