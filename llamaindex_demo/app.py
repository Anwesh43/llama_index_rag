from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext 
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb 
import sys 
from dotenv import load_dotenv

load_dotenv()

def load_data(folder : str):
    documents = SimpleDirectoryReader(folder).load_data()
    return documents 

def createStorageContext(dbpath : str, collection : str):
    db = chromadb.PersistentClient(path = dbpath)
    chroma_collection = db.get_or_create_collection(collection)
    vector_store = ChromaVectorStore(chroma_collection = chroma_collection)
    return StorageContext.from_defaults(vector_store=vector_store)

def create_index(documents : any, storage_context : any):
    index = VectorStoreIndex.from_documents(documents, storage_context = storage_context)
    return index.as_query_engine()

def query(queryEngine : any, queryStr : str):
    return queryEngine.query(queryStr)

if __name__ == "__main__" and len(sys.argv) == 4:
    print("loading documents")
    documents = load_data(sys.argv[1])
    print("storing documents")
    storage_context = createStorageContext(sys.argv[2], sys.argv[3])
    print("creating index")
    query_engine = create_index(documents, storage_context)

    print("Enter your queries here. type exit to stop")
    for line in sys.stdin:
        queryStr = line.rstrip()
        if line == "exit":
            break
        print(query(query_engine, queryStr))

else:
    print("Please enter folder dbpath collection")
        


