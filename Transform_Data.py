import pandas as pd
import json

with open("config.json", 'r') as json_file:
  config = json.load(json_file)

def Genre():
    infilepath = config['infilepath']
    outfilepath = config['outfilepath']
    object=config['tablelist']
    filename = object[0]['Name']
    
    # Read CSV file
    data = pd.read_csv(infilepath + "IMDb_movies.csv", usecols=[0,5])
    
    # Split multiple values in different rows and remove spaces
    data["genre"] = data["genre"].str.split(", ")
    data = data.apply(pd.Series.explode )
    
    # Write to CSV and read again to avoid index issues
    data.to_csv(outfilepath + filename + ".csv", index=False)
    data = pd.read_csv(outfilepath + filename + ".csv", usecols=[1])
    
    # Get unique values from the field
    data["Genre_Description"] = data["genre"].drop_duplicates()
    data["Genre_Description"] = data["Genre_Description"].fillna(value=0)
    data = data[data.Genre_Description!=0]
    
    # Create genre type field by extracting first 3 letters from genre
    data["Genre_Type"] = data["Genre_Description"].str[0:3]
    data["Genre_Type"] = data["Genre_Type"].str.upper()
    
    # Dropping old columns
    data.drop(columns =["genre"], inplace = True) 
    
    # Reorder columns
    data = data[['Genre_Type', 'Genre_Description']]

    # Write to CSV
    data.to_csv(outfilepath + filename + ".csv", index=False)

def Movie_Genre():
    header_list_1 = ["Movie_ID", "Date_Published", "genre", "users_reviews", "critics_reviews"]
    header_list_2 = ["Movie_ID","avg_rating","total_votes","allgenders_0age_rating","allgenders_0age_votes",
                     "allgenders_18age_rating","allgenders_18age_votes","allgenders_30age_rating","allgenders_30age_votes",
                     "allgenders_45age_rating","allgenders_45age_votes","males_allages_rating","males_allages_votes",
                     "males_0age_rating","males_0age_votes","males_18age_rating","males_18age_votes","males_30age_rating","males_30age_votes",
                     "males_45age_rating","males_45age_votes","females_allages_rating","females_allages_votes","females_0age_rating",
                     "females_0age_votes","females_18age_rating","females_18age_votes","females_30age_rating","females_30age_votes",
                     "females_45age_rating","females_45age_votes","top1000_rating","top1000_votes","us_rating","us_votes","non_us_rating","non_us_votes"]
    infilepath = config['infilepath']
    outfilepath = config['outfilepath']
    object=config['tablelist']
    filename = object[1]['Name']

    # Read CSV file
    ratings = pd.read_csv(infilepath + "IMDb_ratings.csv",
                              usecols=[0,1,2,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,
                                       31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48], header=None, names=header_list_2, skiprows=1)
    movies = pd.read_csv(infilepath + "IMDb_movies.csv", usecols=[0,4,5,20,21], header=None, names=header_list_1, skiprows=1)

    #data_1 = pd.melt(ratings, id_vars=["imdb_title_id"], var_name="total_votes", value_name="Value")
    new = movies["genre"].str.split(", ", n=3, expand = True)
    movies["Genre_1"] = new[0]
    movies["Genre_2"] = new[1]
    movies["Genre_3"] = new[2]
    
    # Dropping old columns
    movies.drop(columns =["genre"], inplace = True) 
    
    # Merge CSVs using common column
    data = movies.merge(ratings, on='Movie_ID')

    # Replace Genre with short form code
    genre = pd.read_csv(outfilepath + "Genre.csv")
    data['Genre_1'] = data['Genre_1'].replace(genre.set_index('Genre_Description')['Genre_Type'])
    data['Genre_2'] = data['Genre_2'].replace(genre.set_index('Genre_Description')['Genre_Type'])
    data['Genre_3'] = data['Genre_3'].replace(genre.set_index('Genre_Description')['Genre_Type'])
    
    # Write data to CSV
    data.to_csv(outfilepath + filename + ".csv", 
                index=False)

def Movie():
    # Provide header to rename columns
    header_list = ["Movie_ID", "Title", "Original_Title", "Year", "Duration", "Country",
                       "Language", "Description", "USA_Gross_Income", "World_Gross_Income", "Budget", "Metascore"]
    infilepath = config['infilepath']
    outfilepath = config['outfilepath']
    object=config['tablelist']
    filename = object[2]['Name']

    # Read CSV file
    data = pd.read_csv(infilepath + "IMDb_movies.csv", usecols=[0,1,2,3,6,7,8,13,16,17,18,19], header=None, names=header_list, skiprows=1)
    
    # Write data to CSV
    data.to_csv(outfilepath + filename + ".csv", header=header_list, index=False)
    
def Occupation():
    infilepath = config['infilepath']
    outfilepath = config['outfilepath']
    object=config['tablelist']
    filename = object[3]['Name']
    Role_ID=[]

    # Read CSV file
    data = pd.read_csv(infilepath + "IMDb_title_principals.csv", usecols=[3])
    
    # Get unique values from the field
    data["Role_Description"] = data["category"].drop_duplicates()
    data["Role_Description"] = data["Role_Description"].fillna(value=0)
    data = data[data.Role_Description!=0]
    n = len(data["Role_Description"])
    i = 0
    
    # Create role_id field
    while(n > i):
        i = i+1
        Role_ID.append("role0" + str(i))
    data["Role_ID"] = Role_ID    

    # Dropping old columns
    data.drop(columns =["category"], inplace = True) 
    
    # Reorder columns
    data = data[['Role_ID', 'Role_Description']]

    # Write data to CSV
    data.to_csv(outfilepath + filename + ".csv", index=False)
    
def Cast():
    # Provide header to rename columns
    header_list = ["Cast_ID", "Cast_Name", "Birth_Name", "Height", "Bio", "Birth_Year", "Date_of_Birth",
                        "place_of_birth", "Death_Year", "Date_of_Death", "place_of_death", "Reason_of_Death",
                            "Spouses", "Divorces", "Children"]
    infilepath = config['infilepath']
    outfilepath = config['outfilepath']
    object=config['tablelist']
    filename = object[4]['Name']

    # Read CSV file
    data = pd.read_csv(infilepath + "IMDb_names.csv", usecols=[0,1,2,3,4,6,7,8,10,11,12,13,14,15,17], header=None, names=header_list, skiprows=1)

    # new data frame with split value columns 
    new = data["place_of_birth"].str.split(",", n=3, expand = True)
    n = len(new[0])
    new_1 = data["place_of_death"].str.split(",", n=3, expand = True)

    for i in range(0,n):
        # Matching birth city, state and country correctly with the columns from new data frame
        if new.loc[i][1]==None and new.loc[i][2]==None and new.loc[i][3]==None:
            new.loc[i][3]=new.loc[i][0]
            new.loc[i][2]=''
            new.loc[i][1]=''
        
        elif new.loc[i][2]==None and new.loc[i][3]==None:
            new.loc[i][3]=new.loc[i][1]
            new.loc[i][2]=new.loc[i][0]
            new.loc[i][1]=''        
        
        elif new.loc[i][3]==None:
            new.loc[i][3]=new.loc[i][2]
            new.loc[i][2]=new.loc[i][1]
            new.loc[i][1]=new.loc[i][0]
        
        else:
            new.loc[i][3]=new.loc[i][3]
            new.loc[i][2]=new.loc[i][2]
            new.loc[i][1]=new.loc[i][1]

      
    for j in range(0,n):
        # Matching death city, state and country correctly with the columns from new data frame
        if new_1.loc[j][1]==None and new_1.loc[j][2]==None and new_1.loc[j][3]==None:
            new_1.loc[j][3]=new_1.loc[j][0]
            new_1.loc[j][2]=''
            new_1.loc[j][1]=''
        
        elif new_1.loc[j][2]==None and new_1.loc[j][3]==None:
            new_1.loc[j][3]=new_1.loc[j][1]
            new_1.loc[j][2]=new_1.loc[j][0]
            new_1.loc[j][1]=''
        
        elif new_1.loc[j][3]==None:
            new_1.loc[j][3]=new_1.loc[j][2]
            new_1.loc[j][2]=new_1.loc[j][1]
            new_1.loc[j][1]=new_1.loc[j][0]
        
        else:
            new_1.loc[j][3]=new_1.loc[j][3]
            new_1.loc[j][2]=new_1.loc[j][2]
            new_1.loc[j][1]=new_1.loc[j][1]

    # Assigning values to new columns
    data["Birth_City"]= new[1] 
    data["Birth_State"]= new[2]
    data["Birth_Country"]= new[3]
    data["Death_City"]= new_1[1] 
    data["Death_State"]= new_1[2]
    data["Death_Country"]= new_1[3]

    # Dropping old columns
    data.drop(columns =["place_of_birth","place_of_death"], inplace = True) 
    data["Death_Country"] = data["Death_Country"].str.replace(r' [^\w\s]+', '')

    # Reorder columns
    data = data[["Cast_ID", "Cast_Name", "Birth_Name", "Height", "Bio", "Date_of_Birth", "Birth_Year",
                     "Birth_City", "Birth_State", "Birth_Country", "Spouses", "Divorces", "Children",
                         "Date_of_Death", "Death_Year", "Death_City", "Death_State", "Death_Country", "Reason_of_Death"]]

    # Write to CSV
    data.to_csv(outfilepath + filename + ".csv", index=False)
    
    
def Movie_Cast():
    header_list_1 = ["Movie_ID", "Date_Published"]
    header_list_2 = ["Movie_ID", "Cast_ID", "Role_ID"]
    infilepath = config['infilepath']
    outfilepath = config['outfilepath']
    object=config['tablelist']
    filename = object[5]['Name']

    # Read CSV file
    movies = pd.read_csv(infilepath + "IMDb_movies.csv", usecols=[0,4], header=None, names=header_list_1, skiprows=1)
    titles = pd.read_csv(infilepath + "IMDb_title_principals.csv", usecols=[0,2,3], header=None, names=header_list_2, skiprows=1)
    occupation = pd.read_csv(outfilepath + "Occupation.csv")

    # Merge CSVs using common column
    data = movies.merge(titles, on='Movie_ID')
    data['Role_ID'] = data['Role_ID'].replace(occupation.set_index('Role_Description')['Role_ID'])
    
    # Reorder columns
    data = data[['Movie_ID', 'Cast_ID', 'Role_ID', 'Date_Published']]

    # Write to CSV
    data.to_csv(outfilepath + filename + ".csv", index=False)

def main():
    Genre()
    Movie_Genre()
    Movie()
    Occupation()
    Cast()
    Movie_Cast()
    
if __name__ == "__main__":
    main()