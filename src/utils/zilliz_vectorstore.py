# from pymilvus import Collection, CollectionSchema, FieldSchema, DataType, connections
# import os
# COLLECTION_NAME = "research_docs"
# EMBED_DIM = 1536  # Match your embedding model dimension

# ZILLIZ_CLOUD_URI = os.getenv("Zilliz_endpoint")  # e.g., "https://your-cluster.zillizcloud.com"
# ZILLIZ_CLOUD_TOKEN = os.getenv("Zilliz_Token")  # Your Zilliz Cloud API token

# class ZillizVectorStore:
#     def __init__(self):
#         # Connect to Zilliz Cloud using API token auth
#         connections.connect(
#             alias="default",
#             uri=ZILLIZ_CLOUD_URI,
#             token=ZILLIZ_CLOUD_TOKEN,
#             secure=True,
#         )
#         # Define schema
#         fields = [
#             FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
#             FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=EMBED_DIM),
#             FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=2048),
#         ]
#         schema = CollectionSchema(fields=fields, description="Research documents")
#         # Create or load the collection
#         self.collection = Collection(
#             name=COLLECTION_NAME,
#             schema=schema,
#             using="default"
#         )

#         # Load collection into memory before searching
#         self.collection.load()

#     def insert_documents(self, embeddings, texts):
#         data = [embeddings, texts]
#         self.collection.insert(data)
#         self.collection.flush()

#     def search(self, query_embedding, top_k=5):
#         search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
#         results = self.collection.search(
#             data=[query_embedding],
#             anns_field="embedding",
#             param=search_params,
#             limit=top_k,
#             output_fields=["text"]
#         )
#         hits = results[0] if results else []
#         return [hit.entity.get("text") for hit in hits]


from pymilvus import Collection, CollectionSchema, FieldSchema, DataType, connections
import os
from pymilvus import Index

COLLECTION_NAME = "research_docs"
EMBED_DIM = 1536  # Match your embedding model dimension

ZILLIZ_CLOUD_URI = os.getenv("Zilliz_endpoint")  # e.g., "https://your-cluster.zillizcloud.com"
ZILLIZ_CLOUD_TOKEN = os.getenv("Zilliz_Token")  # Your Zilliz Cloud API token

class ZillizVectorStore:
    def __init__(self):
        # Connect to Zilliz Cloud using API token auth
        connections.connect(
            alias="default",
            uri=ZILLIZ_CLOUD_URI,
            token=ZILLIZ_CLOUD_TOKEN,
            secure=True,
        )
        # Define schema
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=EMBED_DIM),
            FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=2048),  
        ]
        schema = CollectionSchema(fields=fields, description="Research documents")
        # Create or load the collection
        self.collection = Collection(
            name=COLLECTION_NAME,
            schema=schema,
            using="default"
        )


    def insert_documents(self, embeddings, texts):
        data = [embeddings, texts]
        self.collection.insert(data)
        self.collection.flush()

    def search(self, query_embedding, top_k=5):
        search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
        results = self.collection.search(
            data=[query_embedding],
            anns_field="embedding",
            param=search_params,
            limit=top_k,
            output_fields=["text"]
        )
        hits = results[0] if results else []
        return [hit.entity.get("text") for hit in hits]


    def create_index(self):
        index_params = {
            "index_type": "IVF_FLAT",  # or HNSW, depending on what you prefer
            "metric_type": "L2",
            "params": {"nlist": 128}
        }
        self.collection.create_index(field_name="embedding", index_params=index_params)

    def load_collection(self):
        self.collection.load()



def store_in_vector_store(texts):
    embeddings = AzureOpenAIEmbeddings(
        deployment="text-embedding-3-small",
        model="text-embedding-3-small",
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        openai_api_key=AZURE_OPENAI_KEY,
        openai_api_version="2024-05-01-preview",
        openai_api_type="azure",
        chunk_size=2048,
    )
    vector_store = ZillizVectorStore()
    doc_embeddings = embeddings.embed_documents(texts)
    vector_store.insert_documents(doc_embeddings, texts)
    vector_store.create_index()
    vector_store.load_collection()

def search_in_vector_store(user_input, top_k=5):
    embeddings = AzureOpenAIEmbeddings(
        deployment="text-embedding-3-small",
        model="text-embedding-3-small",
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        openai_api_key=AZURE_OPENAI_KEY,
        openai_api_version="2024-05-01-preview",
        openai_api_type="azure",
        chunk_size=2048,
    )
    vector_store = ZillizVectorStore()
    query_embedding = embeddings.embed_query(user_input)
    similar_docs = vector_store.search(query_embedding)
    return similar_docs