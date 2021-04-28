from django.shortcuts import render
from django.shortcuts import redirect

# Create your views here.

import pandas as pd
from sklearn.cluster import KMeans
import random
from sklearn.neighbors import NearestNeighbors

#Importing both the file using pandas
data1 = pd.read_csv('movies data.csv')
data2 = pd.read_csv('ratings data.csv')

#Deleting unnecessary columns
data1 = data1.drop('Unnamed: 0',axis = 1)
data2 = data2.drop(['Unnamed: 0','Timestamp'],axis = 1)

data1.head()
data2.head()

#Merging both the dataframes
data = pd.merge(data2 , data1 , how='outer', on='MovieID')

data.head()

#Merging both the dataframes
data = pd.merge(data2 , data1 , how='outer', on='MovieID')


# Data Processing
# Converting Genres into different columns
# Here we just create columns and put there initial value as 0
x = data.Genres
a = list()
for i in x:
    abc = i
    a.append(abc.split('|'))
a = pd.DataFrame(a)
b = a[0].unique()
for i in b:
    data[i] = 0
data.head(2)


# we assign 1 to all the columns which are present in the Genres
for i in b:
    data.loc[data['Genres'].str.contains(i), i] = 1

# Now there is no use of genre
# Since we have movie id so there is no need for movie names as well
data = data.drop(['Genres','Title'],axis =1)
data.head()


# Because of merging some null values are created
data.isnull().sum()

#WE simply drop the null values coz the are not treatable
data.dropna(inplace= True )

data.isnull().sum()

#By different meathods I found 8 cluster are better
kmeanModel = KMeans(n_clusters=8)
kmeanModel.fit(data)

# Creating an extra column in data for storing the cluster values
data['Cluster'] = kmeanModel.labels_
data['Cluster'].sample(n=10)

data['Cluster'].value_counts()

data.head()


# When we merge the dataframe for a single movie multiple rows were created so a single movie is allotted
# to many clusters so here we allot a single cluster to a movie
# the Cluster which occurs maximum number of times is alloted to the movie
e = []
def fi(group):
    a = pd.DataFrame(group)
    b = pd.DataFrame(a['Cluster'].value_counts())
    d = a.index
    c = [a['MovieID'][d[0]],int(b.idxmax())]
    e.append(c)

data.groupby("MovieID").apply(lambda x: fi(x))

e = pd.DataFrame(e)
e.head()

# I Dont know why always the column name shift according to its will :(
# Here just the column names are swapped
e.rename(columns = {0:'MovieID',1:'Cluster'},inplace=True)
e.drop_duplicates(inplace=True)

e.head(10)


data1 = pd.read_csv('movies data.csv')
new_data = pd.merge(e , data1 , how='outer', on='MovieID')


# These were the movies we deleted while merging the file
new_data.isnull().sum()

# We can delete the movies but I just label them randomly :)
new_data.fillna(random.randint(0,8),inplace=True)

new_data.isnull().sum()

mn = pd.read_csv('movies data.csv')
mn = mn.drop('Unnamed: 0',axis = 1)
mn = mn.drop(['Genres'],axis =1)

nea = [[],[],[],[],[],[],[],[]]
nem = [[],[],[],[],[],[],[],[]]
dt = pd.read_csv('ratings data.csv')
dt = dt.drop(['Unnamed: 0', 'Timestamp', 'UserID'], axis=1)
dt = dt.groupby('MovieID').mean().reset_index()

def temp():
    for i in range(0,8,1):
        for j in new_data['MovieID'][new_data.Cluster == int(i)]:
            #print(dt['Rating'][dt.MovieID == int(j)])
            if len(dt['Rating'][dt.MovieID == int(j)]) == 1:
                nea[i].append([int(i), float(dt['Rating'][dt.MovieID == int(j)])])
            else:
                nea[i].append([int(i), float(2.5)])
            nem[i].append(int(j))
temp()

kn = [NearestNeighbors(n_neighbors=10).fit(nea[0]),NearestNeighbors(n_neighbors=10).fit(nea[1]),NearestNeighbors(n_neighbors=10).fit(nea[2]),NearestNeighbors(n_neighbors=10).fit(nea[3]),NearestNeighbors(n_neighbors=10).fit(nea[4]),NearestNeighbors(n_neighbors=10).fit(nea[5]),NearestNeighbors(n_neighbors=10).fit(nea[6]),NearestNeighbors(n_neighbors=10).fit(nea[7])]

def cl(a):
    if a==0:
        return 'A'
    elif a==1:
        return 'B'
    elif a==2:
        return 'C'
    elif a==3:
        return 'D'
    elif a==4:
        return 'E'
    elif a==5:
        return 'F'
    elif a==6:
        return 'G'
    else:
        return 'H'

def forrec(mid):
    op = kn[int(new_data['Cluster'][new_data.MovieID == mid])].kneighbors(
        [[int(new_data['Cluster'][new_data.MovieID == mid]), float(dt['Rating'][dt.MovieID == mid])]],
        return_distance=False)
    ml = []
    for i in op[0]:
        ml.append([nem[int(new_data['Cluster'][new_data.MovieID == mid])][i], new_data['Title'][nem[int(new_data['Cluster'][new_data.MovieID == mid])][i]]])
    return ml

def forlike():
    l = []
    m = []
    m.append([1, new_data['Title'][1]])
    for i in range(9):
        l.append(random.randint(0, 3883))
    for i in l:
        m.append([i, new_data['Title'][i]])
    return m

def login(request):
    if request.method == 'POST':
        return redirect('home/')
    return render(request, 'login.html')

def forre(mid):
    l = new_data['Cluster'][new_data.MovieID == mid]
    ml = []
    for i in new_data['Title'][new_data.Cluster == int(l)].sample(n=10).tolist():
        ml.append([int(mn.loc[mn['Title'] == i]['MovieID']), i])
    return ml

def home(request):
    if request.method == 'POST':
        text = 'Recommended movies on what u liked! And u belong to group '
        mid= int(request.POST['movieid'])
        l = new_data['Cluster'][new_data.MovieID == mid]
        text = text + cl(int(l))
        if request.POST['like'] == 'yes':
            ml = forrec(mid)
        else:
            ml = forre(mid)
        return render(request, 'rectable.html', {'movies':ml, 'text':text, 'mid':int(request.POST['movieid'])})
    m=forlike()
    text = 'Select a movie that u liked!'
    return render(request, 'table.html', {'movies':m, 'text':text})

def creator(request):
    return render(request, "creator.html")
