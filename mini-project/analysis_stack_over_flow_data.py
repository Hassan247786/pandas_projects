import pandas as pd

# read in the files 
python_survey_df = (pd.read_csv("E:/Syllabus/pandas_practise/2020_sharing_data_outside.csv", 
                    low_memory=False))  # pandas is free to use more memory to allocate dtypes
stack_overflow_df = pd.read_csv("E:/Syllabus/pandas_practise/so_2021_survey_results.csv", low_memory=False)
oecd_countries_df = (pd.read_csv("E:/Syllabus/pandas_practise/oecd_locations.csv", 
                    header=None, names=["abbreviation", "Country"])
                     .set_index("Country")) #index to be used later for a join

# cleaning and analysis of the Python Survey dataframe
column_names = (python_survey_df
                .columns
                .to_list())  # current column names/structure confusing, goal is to create a multi-index
special_columns = ['age','are.you.datascientist','is.python.main','company.size',
                   'country.live','employment.status','first.learn.about.main.ide',
                   'how.often.use.main.ide','is.python.main','main.purposes',
                   'missing.features.main.ide','nps.main.ide','python.version.most',
                   'python.years','python2.version.most','python3.version.most',
                   'several.projects','team.size','use.python.most','python.years']
tuple_list = [] 
for item in column_names:    
    if item in special_columns:
        tuple_list.append(f"general {item}".split())  # columns under a new 'general' column in our hierarchy
        continue
    if item.count(".") >= 1:
        tuple_list.append((item.rsplit(".", 1)))  #e.g. 'other.lang.Java' goes to 'other.lang', 'Java'
python_survey_df.columns = pd.MultiIndex.from_tuples(tuple_list)  # order of values within each tuple dictates the hierarchy, only unique values picked out
python_survey_df = python_survey_df.sort_index(axis=1)  # sort multi-indexed columns by alphabetical order
most_popular_ides = (python_survey_df[("ide", "main")] 
                     .value_counts(ascending=False) 
                     .head(10))  # the top 10 values in the sorted list 
most_popular_languages = (python_survey_df["other.lang"]
                          .notnull().sum()  # num.non-null entries under each language column = num.of users for that language
                          .sort_values(ascending=False)
                          .head(10))
ten_most_common_countries_survey_takers = (python_survey_df
                                           [("general", 'country.live')]
                                           .value_counts()
                                           .sort_values(ascending=False)
                                           .head(10))
country_with_highest_python_exp = (python_survey_df
                                    .loc[python_survey_df[("general", "python.years")] == "11+ years", 
                                    ("general", "country.live")]
                                    .value_counts()
                                    .sort_values(ascending=False)
                                    .head(1))
# 'proportion' calculates which country has greatest proportion of 11+ years devs
sample_sizes = (python_survey_df[("general", "country.live")]
                .value_counts()  # len(country data) = number of devs 
                .sort_index())
eleven_years_values = (python_survey_df
                    .loc[python_survey_df[("general", "python.years")] == "11+ years", 
                         ("general", "country.live")]
                    .value_counts()
                    .sort_index())
proportion = (((eleven_years_values/sample_sizes) * 100)
              .round(3)
              .sort_values(ascending=False)
              .dropna()
              .head(1))
# proportion of devs for each level of experience 
proportion_of_developers_years_of_experience = (
    (python_survey_df[("general", "python.years")]
    .value_counts(normalize=True)  # each entry is divided by the total value_counts()
    *100)  # convert to percentages
    .round(2))

# cleaning and analysis of the Stack Overflow dataframe
average_salary_by_employment_type = ((stack_overflow_df.
                                     groupby("Employment")["ConvertedCompYearly"]
                                     .mean()
                                     .round(-2)
                                     .sort_values(ascending=False)
                                     .dropna()
                                     .astype("Int64")))  # removes the .0 for each float
table_avg_salaries = (stack_overflow_df  # avg salaries by country and education level
                      .set_index("Country")
                      .pivot_table(index="Country", columns= 'EdLevel', values="ConvertedCompYearly")
                      .round(-3)
                      .astype("Int64"))
table_avg_salaries_2 = oecd_countries_df.join(table_avg_salaries)  # only include oecd_countries via matching indexes
top_associate_country, top_associate_salary = (table_avg_salaries_2["Associate degree (A.A., A.S., etc.)"]
                                               .agg(["idxmax", "max"]))
top_phd_country, top_phd_salary = (table_avg_salaries_2['Other doctoral degree (Ph.D., Ed.D., etc.)']
                                   .agg(["idxmax", "max"]))
# begin cleaning the stackoverflow df - columns to clean: 'LanguageHaveWorkedWith', "YearsCode"
stack_overflow_df = stack_overflow_df.dropna(subset=["LanguageHaveWorkedWith"])
stack_overflow_df = (stack_overflow_df.                             
                    loc[(stack_overflow_df['LanguageHaveWorkedWith']
                    .str.contains("Python"))])  # filter so we ONLY have Python developers
stack_overflow_df = stack_overflow_df.dropna(subset=["YearsCode"]) 
stack_overflow_df.loc[stack_overflow_df["YearsCode"] == "Less than 1 year", "YearsCode"] = '0'
stack_overflow_df.loc[stack_overflow_df["YearsCode"] == "More than 50 years", "YearsCode"] = '51'
stack_overflow_df["YearsCode"] = stack_overflow_df["YearsCode"].astype("int64")
stack_overflow_df['experience'] = (pd.cut(stack_overflow_df['YearsCode'],
                                    bins=[-1, 1, 2, 5, 10, 100],
                                    labels=['Less than 1 year','1-2 years',
                                    '3-5 years','6-10 years','11+ years'])) 
proportions_survey_two = ((stack_overflow_df["experience"]
                           .value_counts(normalize=True)  # how many times each experience level label appears = num.devs with that level of exp
                           .round(3)*100))


def print_statements():
    """Print all summary statistics computed from the two surveys."""
    print("\nThe top 10 most popular IDE'S -")
    print(most_popular_ides)
    print("\nThe top 10 most popular programming languages -")
    print(most_popular_languages)
    print("\nThe 10 most common countries of the people that took the survey - ")
    print(ten_most_common_countries_survey_takers)
    print("\nCountry with the greatest number of Python developers with 11+ years of experience - ")
    print(country_with_highest_python_exp)
    print("\nCountry with the highest PROPORTION (%) of developers with 11+ years of experience ")
    print(proportion)
    print("\nThe average annual compensation for each type of type of employment - ")
    print(average_salary_by_employment_type)
    print("\nCountry with the highest associate degree earners on average - ")
    print(top_associate_country, top_associate_salary)
    print("\nCountry with the highest doctoral degree earners on average - ")
    print(top_phd_country, top_phd_salary)
    print("\nProportions (%) of Python developers with specific level of experience (Python Survey) - ")
    print(proportion_of_developers_years_of_experience) 
    print("\nProportions (%) of Python developers with specific level of experience (Stack Overflow Survey) - ")
    print(f"{proportions_survey_two}\n")
print_statements()
