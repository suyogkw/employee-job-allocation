#imports
import pandas as pd

def defragment(row):
    values = row.dropna().values
    return pd.Series(values)

#get data
df_emp = pd.read_excel('./data.xlsx','Employees')
df_jobs = pd.read_excel('./data.xlsx','Jobs')

#combine data creation and validation
df = df_emp.melt(id_vars=['empid','vertical'], value_name='jobid')[['empid','vertical','jobid']]
df.drop_duplicates(['empid','jobid'], inplace=True)
df = df.merge(df_jobs, on=['jobid'], suffixes=['_current','_next'])
df = df[df['vertical_current']!=df['vertical_next']]

#allocation method
def allocate(df_in):
    df_data = df_in[df_in.columns]
    res = pd.DataFrame()
    x = df_data.groupby('jobid')['jobid'].transform('size') <= df_data['capacity']

    while len(x[x])>0:
        res = res.append(df_data[x])
        df_data = df_data.merge(res[['empid']], on=['empid'], indicator='i', how='outer').query('i == "left_only"').drop('i', 1)
        x = df_data.groupby('jobid')['jobid'].transform('size') <= df_data['capacity']

    unalloc = df_data[['jobid','empid']].reset_index().pivot(columns='jobid', values='empid')
    unalloc = unalloc.transpose().stack().groupby(level='jobid').apply(defragment)
    res = res if res.empty else res.drop('capacity',1)
    return res, unalloc, df_data


#simple allocation without conflict

result, unallocation, update_df = allocate(df)

#method to measure fairness of assumed allocation
def calculatescore(df, row):
    temp_df = getdfwithoutrow(df, row)
    competitors = temp_df.loc[temp_df.jobid == row.jobid]['empid'].tolist()
    temp_res, temp_unalloc, x = allocate(temp_df)
    if(temp_unalloc.empty):
        return 0 if temp_df.empty else temp_df['empid'].nunique()
    unfair = temp_unalloc.reset_index()[0].str.contains('|'.join(competitors)).any()
    return 0 if temp_res.empty or unfair else temp_res['empid'].nunique()

def getdfwithoutrow(df, row):
    temp_df = df[df.columns]
    temp_df = temp_df.loc[temp_df.empid != row.empid]
    temp_df.loc[temp_df.jobid == row.jobid,'capacity'] -= 1
    return temp_df.loc[temp_df.capacity != 0]

#try for circular combinations
scores = update_df.apply(lambda x: calculatescore(update_df, x), axis=1)

# unfair if score is 0, most fair is selected by max socre allocation
while scores.max()>0:
    result = result.append(update_df.iloc[scores.idxmax()].drop('capacity'))
    update_df = getdfwithoutrow(update_df, update_df.iloc[scores.idxmax()])
    r, unallocation, update_df = allocate(update_df)
    result = result.append(r)
    if update_df.empty:
        break
    scores = update_df.apply(lambda x: calculatescore(update_df, x), axis=1)

#write output
result.sort_values('empid').to_excel('./allocation.xlsx', index=False)
if len(unallocation)>0:
    unallocation.unstack().to_excel('./unallocation.xlsx')