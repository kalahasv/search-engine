import os
import json
from posixpath import splitext
from nltk.stem.porter import *
from urllib.parse import urlparse
from pprint import pprint

# intersection function based on the pseudocode from class notes
def intersection(x: list, y: list) -> list:
    answer = list()
    cur_x_index = 0
    cur_y_index = 0
    while cur_x_index < len(x) and cur_y_index < len(y):
        if x[cur_x_index] == y[cur_y_index]:
            answer.append(x[cur_x_index])
            cur_x_index += 1
            cur_y_index += 1
        elif x[cur_x_index] < y[cur_y_index]:
            cur_x_index += 1
        else:
            cur_y_index += 1
    return answer


def find_urls(docPath,index_list) -> list: #returns a list of urls associated with the given fids 
    urls = []
    counter = 1 #count the current index of where we are in the files
   
    for root, dirs, files in os.walk(docPath): #go through the files again 
        dirs.sort() #sort dirs so they are in the same order every time
        for page in files:
            
            with open(os.path.join(root, page)) as json_file:
                data = json.load(json_file)
            
            extension = splitext(urlparse(data["url"]).path)[1] #gets the extension, esentially just making sure we're traversing the same .jsons in the same order
            if(extension != '.txt' and extension != '.php'):
                #print("Hi we're here at the file")
                #print(counter)
                #print("Index list:",index_list[0])
                if str(counter) in index_list[0]:
                   #print("counter was found in url")
                   urls.append(data["url"])
                   
                
                counter+=1
            if(len(urls) == len(index_list[0])):
                pprint(urls)
                return urls
    pprint(urls)
    return urls

# Steps:
# 1. Search for EACH search term from the inverted index
# 2. Fetch the documents for each search term
# 3. Find intersection between the retrieved sets of documents

if __name__ == "__main__":
    INDEX_PATH = 'indexes/index1.json'

    with open(INDEX_PATH) as f:
        index = json.load(f)

    # Array containing each word of the query
    queries = list(input("Search Query: ").split())

    docs = list()
    stemmer = PorterStemmer()
    # For each individual word, find the entry in the index, should implement boolean logic here too.
    
    for query in queries:
        stemmed = stemmer.stem(query)
        if query in index: #if the search is valid 
            
        # Append this query word's locations to the big list of documents
             docs.append(list(index[stemmed]['locations'].keys()))
        else:
            print("This query is not found in the search index") #quit if the query isn't in the index
            quit()

    # run the intersection function if more than one query word
    if len(docs) > 1:
        while len(docs) > 1:
            same = intersection(docs.pop(), docs.pop())
            docs.append(same)
        print(docs[0]) #note: remove later
    else:
        print(docs[0]) #note: remove later



    #find the urls of the list of docs 
    docPath ="DEV_TEST"
    urls = find_urls(docPath,docs)
    
   
