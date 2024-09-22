from vector_utils import build_index,add_to_index,save_index,load_index,store_to_db,search_index,retrieve
from data_utils import extract_from_pdfs
from data_schema import IndexData
from embed import embed_docs
import sqlite3
import numpy as np
from tqdm import tqdm
import argparse
from faiss import IndexIDMap2
import traceback,sys


sqlite3.register_adapter(np.int64, int)

def process_query(query:str,connection:sqlite3.Connection,index:IndexIDMap2):
    embeddings = embed_docs([query])
    #vector => ids
    D,I =search_index(index=index,query=embeddings,k=2)
    print("distances and ids:",D,I)
    #sql => ids => text/metadata
    res = retrieve(index_name="demo",ids=I,connection=connection) 
    return [row[1] for row in res]

# a small pipeline
def preprocess_data(root:str)->None:
    try:
        index = build_index(dimension=512)
        print("initialized index")
    except:
        print("index initialization failed")
        traceback.print_exc(file=sys.stdout)
        return
    try:
        connection = sqlite3.Connection("demo.db",isolation_level=None,check_same_thread=False)
        id=0
        for batch,chunk in extract_from_pdfs(root=root,chunk_size=3):  
            try:
                embeddings = embed_docs(batch)
                all_points = [] 
                for i in range(len(batch)):
                    point = IndexData(vector=embeddings[i],content=batch[i],id=id)
                    id+=1
                    all_points.append(point)
                #add to index
                add_to_index(index=index,data=all_points)
                store_to_db(data=all_points,connection=connection,index_name="demo")
            except:
                print("failed to add following files",chunk)
                traceback.print_exc(file=sys.stdout)
            
        print("added data to index and db")  
        save_index(index=index,index_name="demo")
        print("saved index")  
        connection.close()
    except:
        print("adding data to index/db failed.")
        connection.close()
        traceback.print_exc(file=sys.stdout)
        return
    try:
        connection = sqlite3.Connection("demo.db",isolation_level=None,check_same_thread=False)
        index = load_index(index_name="demo")
        query = "experince is more than 10 years"
        print("searching for query: ",query)
        res = process_query(query=query,connection=connection,index=index)
        print("result:",res)
        print("index tested")
        connection.close()
    except:
        print('Could not complete testing.')
        traceback.print_exc(file=sys.stdout)
        connection.close()
        

    
    
            
if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Process data.')
    parser.add_argument("-p","--path",type=str)
    args = parser.parse_args()
    preprocess_data(args.path)
    





