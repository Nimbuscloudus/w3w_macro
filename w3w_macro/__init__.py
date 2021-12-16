import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

airport_kw = ('school','university', 'hotel', 'hostel', 'bank', 'hospital',  'museum',
            'School','University', 'Hotel', 'Hostel', 'Bank', 'Jospital',  'Museum')
museum_kw = ('school','university', 'hotel', 'hostel', 'bank', 'hospital', 'airport',
          'School','University', 'Hotel', 'Hostel', 'Bank', 'Hospital',  'Airport')
hospital_kw = ('school','university', 'hotel', 'hostel', 'bank', 'museum', 'airport',
            'School','University', 'Hotel', 'Hostel', 'Bank', 'Museum', 'Airport')
hotel_kw = ('school','university','hostel','bank', 'hospital','museum','airport',
          'School','University','Hostel','Bank', 'Hospital','Museum','Airport',)
school_kw = ('hotel', 'hostel', 'bank', 'hospital',  'museum', 'airport',
          'Hotel', 'Hostel', 'Bank', 'Hospital',  'Museum', 'Airport')
list_of_words = ('school','university', 'hotel', 'hostel', 'bank', 'hospital',  'museum','airport',
              'School','University', 'Hotel', 'Hostel', 'Bank', 'Hospital',  'Museum', 'Airport')

def cleaner(df):
    """
    This function drops all the useless columns, nan values and rows that contains certain words which are listed in the 
    "word_list" list.
    
    Arguments:
    df - csv file that is downloaded from "search robot" search platform
    
    Return:
    The function returns the cleaned data and export it in csv format
    """
    word_list = ("data", "privacy", "gdpr", "test", "example", "hiring", "careers", "jobs", "freedomofinformation",
                "freedom.information", "freedominformation", "abuse", "career", "youremail", "you@", "email.com", 
                "foi@", "foia@")
    df = df[['name', 'scraped email', 'search keywords']]
    # Keeping three columns that would be needed
    df = df.dropna().reset_index().drop(columns="index", axis=1)
    # Dropping rows that contains nan values
    df = df[~df['name'].str.contains('|'.join(word_list))]
    df = df[~df['scraped email'].str.contains('|'.join(word_list))]
    # Dropping rows that contains words listed in the "word_list" list
    df['state'] = df['search keywords'].str.split(" ").str[-1]
    # Creating a new column that contains the state name of the each row result
    df = df.drop(columns="search keywords", axis=1)
    # Dropping no longer needed column
    return df
    
def df_NAN_dropper(df):
    """
    Takes a dataframe as an argument and only assigns the useful two columns to
    df and removes null values, resets index, then changes the name column into
    a more appropriate one. This all assumes that the data given is uniform.
    """
    df = df[['name', 'scraped email']]
    df = df.copy(deep=True)
    df = df.dropna()
    df = df.drop_duplicates(subset=['scraped email'])
    df = df.reset_index().drop(columns="index", axis=1)
    df = df.rename(columns={'name': 'CompanyName'})
    df = df.sort_values('CompanyName',ascending=True)
    df = df.reset_index().drop(columns="index", axis=1)
    return df

def df_COUNTIF(df):
    """
    Takes a dataframe as an argument and uses iterrows to essentially perform
    COUNTIF function from excel. It matches one row to the next one, and if they
    are the same, adds one to the counter and keeps adding until the next row
    stops matching names, assigns it to a new column called 'Column Count', thus 
    counting company names duplicates in a way that we can modify and later 
    retrieve the required emails (up to 4 duplicates)
    """
    df = df.copy(deep=True)
    counter = 1
    counter_list = []
    length = df.shape[0]
    for index, item in df.iterrows():
        if index + 1 == length:
            counter = 1
        elif item['CompanyName'] == df.iloc[index+1]['CompanyName']:
            counter += 1
        else:
            counter = 1
        counter_list.append(counter)
    df['ColumnCount'] = pd.DataFrame(counter_list)
    return df

def df_WORD_dropper(df, x=list_of_words):
    """
    Chooses from a library of words assigned to a key variable and drops
    rows containing said words. Essentially a filter function. Depending on
    what the user wants to do, they can change the "list of words" on the
    str.contains line to filter out a different set of keywords.
    """
    airport_kw = ('school','university', 'hotel', 'hostel', 'bank', 'hospital',  'museum',
                'School','University', 'Hotel', 'Hostel', 'Bank', 'Jospital',  'Museum')
    museum_kw = ('school','university', 'hotel', 'hostel', 'bank', 'hospital', 'airport',
              'School','University', 'Hotel', 'Hostel', 'Bank', 'Hospital',  'Airport')
    hospital_kw = ('school','university', 'hotel', 'hostel', 'bank', 'museum', 'airport',
                'School','University', 'Hotel', 'Hostel', 'Bank', 'Museum', 'Airport')
    hotel_kw = ('school','university','bank', 'hospital','museum','airport',
              'School','University','Bank', 'Hospital','Museum','Airport',)
    school_kw = ('hotel', 'hostel', 'bank', 'hospital',  'museum', 'airport',
              'Hotel', 'Hostel', 'Bank', 'Hospital',  'Museum', 'Airport')
    list_of_words = ('school','university', 'hotel', 'hostel', 'bank', 'hospital',  'museum', 'airport',
                  'School','University', 'Hotel', 'Hostel', 'Bank', 'Hospital',  'Museum', 'Airport')
    df = df[~df['CompanyName'].str.contains('|'.join(x))] #VARIABLE
    df = df.reset_index().drop(columns="index", axis=1)
    return df

def df_EXPORTER(df, csvname):
    """
    After all the cleaning and exports CSVs with Column Counts below 4. Resets
    the index, drops the useless columns and sorts alphabetically and finally
    exports the CSV.
    """
    for i in range(4):
        name = str(csvname)
        csvname1 = csvname.split("_")[0] + "_" + csvname.split("_")[1] + "_" + csvname.split("_")[2] + "_"
        csvname2 = "_" + csvname.split("_")[-3] + "_" + csvname.split("_")[-2] + "_" + csvname.split("_")[-1]
        below_4_df = df[df['ColumnCount']==i+1]
        below_4_df = below_4_df.reset_index()
        below_4_df = below_4_df.drop(columns=["ColumnCount", "index"], axis=1)
        below_4_df = below_4_df.sort_values('CompanyName', ascending=True)
        below_4_df.to_csv(csvname1 + str(i+1) + csvname2 +'.csv', index=False)
        
def df_snippet_adder(df):
    """
    This funtions adds two more columns in the dataframe, one contains the intro snippets and the other contains the outro snippets.
    """
    df = df.reset_index().drop(columns="index")
    condition_s1 = [
    df.index % 11 == 0,
    df.index % 11 == 1,
    df.index % 11 == 2,
    df.index % 11 == 3,
    df.index % 11 == 4,
    df.index % 11 == 5,
    df.index % 11 == 6,
    df.index % 11 == 7,
    df.index % 11 == 8,
    df.index % 11 == 9,
    df.index % 11 == 10]
    
    output_s1 = [
    "I hope you are well.",
    "How are things going?",
    "How's your week been?",
    "I hope everything is ok on your side.",
    "Hope this email finds you well.",
    "I hope you're doing well.",
    "I hope you're having a great week.",
    "I hope you're having a wonderful day.",
    "How are you today?",
    "I hope your week is going smoothly.",
    "Hope you are having a great week."]
    
    condition_s2 = [
    df.index % 8 == 0,
    df.index % 8 == 1,
    df.index % 8 == 2,
    df.index % 8 == 3,
    df.index % 8 == 4,
    df.index % 8 == 5,
    df.index % 8 == 6,
    df.index % 8 == 7]
    
    output_s2 = [
    "Thanks,",
    "Many thanks,",
    "Kind regards,",
    "Best regards,",
    "Best,",
    "Cheers,",
    "Warm regards,",
    "Thank you,"]
    
    df['Snippet_1'] = pd.Series(np.select(condition_s1, output_s1))
    df['Snippet_2'] = pd.Series(np.select(condition_s2, output_s2))
    
    return df