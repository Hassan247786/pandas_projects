import pandas as pd
from matplotlib import pyplot as plt

institutions_filename = 'E:/Syllabus/pandas_practise/Most-Recent-Cohorts-Institution.csv.gz'
fields_filename = 'E:/Syllabus/pandas_practise/FieldOfStudyData1718_1819_PP.csv.gz'
institution_df = pd.read_csv(institutions_filename, 
                usecols=['OPEID6', 'INSTNM', 'CITY', 'STABBR', 'FTFTPCTPELL',
                'TUITIONFEE_IN', 'TUITIONFEE_OUT', 'ADM_RATE', 'NPT4_PUB', 
                'NPT4_PRIV', 'NPT41_PUB', 'NPT41_PRIV', 'NPT45_PUB', 
                'NPT45_PRIV', 'MD_EARN_WNE_P10', 'C100_4'], engine='pyarrow')
fields_of_study_df = pd.read_csv(fields_filename, 
                usecols=['OPEID6', 'INSTNM', 'CREDDESC', 'CIPDESC', 'CONTROL'], engine='pyarrow')
pd.set_option('display.max_columns', None)

state_w_greatest_num_unis = (
    institution_df.groupby('STABBR')['OPEID6'] # OPEID6 contains institution unique ID
    .count() 
    .sort_values(ascending=False) 
    .head(1))
city_state_w_greatest_num_unis = (
    institution_df
    .groupby(['STABBR', 'CITY'])['INSTNM']
    .nunique()
    .sort_values(ascending=False)
    .head(1))
memory_before = (institution_df
                 .memory_usage(deep=True) # each individual string's memory taken into account
                 .sum()) 
institution_df[['CITY', 'STABBR']] = (
    institution_df[['CITY', 'STABBR']]
    .astype('category'))
memory_after = institution_df.memory_usage(deep=True).sum()
memory_saved = memory_before - memory_after
histogram_values = (fields_of_study_df
                    .loc[fields_of_study_df['CREDDESC'] == 'Bachelors Degree']
                    .groupby('INSTNM')['CIPDESC']
                    .count())
histogram_values.plot(
    kind='hist', 
    ylabel='Frequency (Num of Universities Offering x Amount of Courses)',
    xlabel='Number of Bachelorss Programmes Offered', 
    title="Histogram Showing Frequency of Universities Offering Different Amount of Bachelor Programmes", 
    figsize=(10,6))
plt.show()
most_bachelors_programmers_offered = histogram_values.sort_values(ascending=False).head(1)
histogram_frequencies_postgrad_programmes = (
    fields_of_study_df
    .loc[fields_of_study_df['CREDDESC']
         .isin(["Master's Degree", "Doctoral Degree"])]
    .groupby('INSTNM')['CIPDESC']
    .count()
)
histogram_frequencies_postgrad_programmes.plot(kind = 'hist')
plt.show()
uni_with_highest_num_grad_programmes = (
    histogram_frequencies_postgrad_programmes
    .sort_values(ascending=False)
    .head(1)
)
def bachelors_only(s):
    return (
        s.isin(["Bachelors Degree"]).any()
        and not s.isin(["Doctoral Degree"]).any()
        and not s.isin(["Master's Degree"]).any()
    )
bachelors_only_universities = (
    fields_of_study_df
    .groupby('INSTNM')['CREDDESC']
    .apply(bachelors_only))
bachelors_only_universities_num = bachelors_only_universities.sum() 
def masters_and_doctorates_not_bachelors(s):
    return (
        s.isin(["Master's Degree"]).any()
        and s.isin(["Doctoral Degree"]).any()
        and not s.isin(["Bachelors Degree"]).any()
    )
masters_and_doctorates_not_bachelors_universities = (
    fields_of_study_df
    .groupby('INSTNM')['CREDDESC']
    .apply(masters_and_doctorates_not_bachelors)
)
masters_and_doctorates_not_bachelors_num = masters_and_doctorates_not_bachelors_universities.sum()
def computer_science(s):
    return s[s.str.contains("Computer Science")]
cs_bachelors_series = (
    fields_of_study_df
    .loc[fields_of_study_df['CREDDESC'] == 'Bachelors Degree']
    .groupby('INSTNM')['CIPDESC']
    .apply(computer_science)
)
cs_bachelors_unis_num = cs_bachelors_series.index.get_level_values(0).nunique()
cs_bachelors_institutions = (
    fields_of_study_df
    .loc[(fields_of_study_df['CIPDESC'].str.contains('Computer Science')) &
        (fields_of_study_df['CREDDESC'] == 'Bachelors Degree')])
cs_bachelors_institution_types = (
    cs_bachelors_institutions['CONTROL']
    .value_counts()
)
plt.clf()  # clear previous plots so that the figure isnt glitched for the pie chart
(cs_bachelors_institution_types
 .plot(kind='pie', ylabel="", 
    title="Different Types of Institutions Offering Computer Science Degrees", 
    figsize=(10,6), 
    legend=False, 
    autopct="%1.1f%%"))
plt.show()
cs_bachelors_universities = (
    fields_of_study_df.loc[(fields_of_study_df['CREDDESC'] == 'Bachelors Degree')
    & (fields_of_study_df['CIPDESC'].str.contains('Computer Science'))])
cs_bachelors_universities = cs_bachelors_universities.set_index('OPEID6')[['CIPDESC', 'CONTROL']]
cs_universities_with_tuition = cs_bachelors_universities.join(institution_df.set_index('OPEID6'))
cs_tuition_statistics = cs_universities_with_tuition['TUITIONFEE_OUT'].describe().round(0)
tuition_fee_desc = (
    cs_universities_with_tuition
    .groupby('CONTROL')['TUITIONFEE_OUT']
    .describe()
    .round(0)
    .dropna() 
    .transpose())  # swap columns and rows
correlation_1 = institution_df[['ADM_RATE', 'TUITIONFEE_OUT']].corr().iloc[0]
(institution_df
 .plot(kind='scatter', y='ADM_RATE', x='TUITIONFEE_OUT', 
       ylabel='Admission Rate (Proportion of applicants accepted)', 
        xlabel='Tution Fees Charged by the University (USD)', 
        title='Tution Fee Costs vs Admission Rate, Coloured by Grad Salaries (USD)', 
        c='MD_EARN_WNE_P10',
        cmap='Spectral', 
    figsize=(10,6)))
plt.show()
most_expensive_and_generous_universities = (
    institution_df
    .loc[(institution_df['TUITIONFEE_OUT'] > 
        institution_df['TUITIONFEE_OUT'].quantile(0.75))
        & (institution_df['FTFTPCTPELL'] > 
        institution_df['FTFTPCTPELL'].quantile(0.75)),
        ['INSTNM', 'CITY', 'STABBR', 'TUITIONFEE_OUT', 'FTFTPCTPELL']]
        .sort_values('INSTNM')
        .set_index('INSTNM'))
num_institutions_negative_net_price = (
    institution_df
    .loc[(institution_df['NPT41_PUB'] < 0)
        | (institution_df['NPT41_PRIV'] < 0), 
        'INSTNM']
    .count())
average_net_price_ratio = (
    (institution_df['NPT41_PUB']/institution_df['NPT45_PUB']).mean().round(2))
average_private_net_price_ratio = (
    (institution_df['NPT41_PRIV']/institution_df['NPT45_PRIV'])
    .mean().round(2))
best_roi_public_universities = (
    institution_df.loc[(institution_df['NPT4_PUB'] <= institution_df['NPT4_PUB'].quantile(0.25))
                    & (institution_df['MD_EARN_WNE_P10'] >= institution_df['MD_EARN_WNE_P10'].quantile(0.75)), 
                    'INSTNM'])
best_roi_private_universities = (
    institution_df.loc[(institution_df['NPT4_PRIV'] <= institution_df['NPT4_PRIV'].quantile(0.25))
                    & (institution_df['MD_EARN_WNE_P10'] >= institution_df['MD_EARN_WNE_P10'].quantile(0.75)), 
                    'INSTNM'])
corr_admission_and_completion = (institution_df[['ADM_RATE', 'C100_4']].corr())
joined_df = institution_df.set_index('INSTNM').join(fields_of_study_df.set_index('INSTNM')['CONTROL'], how='left')
highest_earnings_by_type_of_uni = (
    joined_df
    .groupby('CONTROL')['MD_EARN_WNE_P10']
    .mean()
    .sort_values())
elite_universities = [
    "Brown University",
    "Columbia University in the City of New York",
    "Cornell University",
    "Dartmouth College",
    "Harvard University",
    "University of Pennsylvania",
    "Princeton University",
    "Yale University",
    "Massachusetts Institute of Technology",
    "Stanford University",
    "University of Chicago"
]
elite_unis_earnings = (
    institution_df
    .loc[institution_df['INSTNM']
         .isin(elite_universities), 'MD_EARN_WNE_P10']
         .mean()
         .round(0))
difference_in_grad_earnings_elite_and_private = elite_unis_earnings - highest_earnings_by_type_of_uni
postgrad_earnings_by_state = (
    institution_df
    .groupby('STABBR')['MD_EARN_WNE_P10']
    .mean()
    .dropna()
    .sort_values())
postgrad_earnings_by_state.plot(
    kind='bar', figsize=(20,10), xlabel='State', 
    ylabel='Average Salary 10 Years After Graduation (USD)',
    title='Bar Plot Showing Average Salary After Graduation By State', 
    color='purple')
plt.show()
postgrad_earnings_by_state.plot(
    kind='box', xlabel='', 
    ylabel='Average Salary 10 Years After Graduation (USD)', 
    title='Boxplot Showing Salary Statistics Postgraduation in the US', 
    figsize=(10,6))
plt.show()

def print_statements():
    print(f"The state with the greatest number of universities: {state_w_greatest_num_unis}\n")
    print (f"The city (and its associated state) with the greatest number of universities: {city_state_w_greatest_num_unis}")
    print ("Converting City and State columns into categories rather than strings, associated stats (in bytes):")
    print(
    f"\t{memory_before:,}\n"
    f"\t{memory_after:,}\n"
    f"\t{memory_saved:,}\n")
    print(f"University with the highest number of graduate programmes: {uni_with_highest_num_grad_programmes}")
    print(f"The institution offering the most bachelor's programs: {most_bachelors_programmers_offered}")
    print(f"Number of universities offering bachelor's degrees but not master's or doctoral degrees: {bachelors_only_universities_num}")
    print(f"Number of universities offering master's and doctoral degrees but not bachelor's degrees: {masters_and_doctorates_not_bachelors_num}")
    print(f"Number of universities offering bachelor's degrees in Computer Science: {cs_bachelors_unis_num}")
    print(f"Number of institution types offering bachelor's-level Computer Science programs:\n{cs_bachelors_institution_types}")
    print(f"Tuition fees (USD) statistics for undergraduate Computer Science degrees:\n{cs_tuition_statistics}")
    print(f"ADM_RATE vs TUITIONFEE_OUT correlation: {correlation_1['TUITIONFEE_OUT']:.3f}") 
    print("Universities in the top 25% for both tuition fees and Pell Grant recipients:\n")
    f"{most_expensive_and_generous_universities}"
    print("Number of institutions where the bottom quintile receives money:", 
      num_institutions_negative_net_price)
    print("Average net price ratio between the lowest and highest income quintiles:", 
      average_net_price_ratio)
    print("Average proportion paid by the bottom quintile compared to the top quintile at private universities:", 
      average_private_net_price_ratio)
    print(f"Public universities with the best ROI (lowest cost and highest earnings): {best_roi_public_universities}")
    print(f"Private universities with the best ROI (lowest cost and highest earnings): {best_roi_private_universities}")
    print(f"Correlation between admission rate and completion rate: \n{corr_admission_and_completion}")
    print(f"Average earnings 10 years after graduation by institution type:\n{highest_earnings_by_type_of_uni}")
