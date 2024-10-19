import chromadb
chroma_client = chromadb.Client()

path_collection = chroma_client.create_collection("path_collection")
alert_collection = chroma_client.create_collection("alert_collection")

path_collection.add(
    documents=[
        "This is a document about pineapple",
        "This is a document about oranges",
        "This is a document about apples",
    ],

    ids=['id_1', 'id_2', 'id_3']
)

alert_collection.add(
    documents=[
        "Alert: House is getting robbed",
        "Alert: Your package has arrived",
        "Alert: A black car passes by",
    ],

    ids=['id_1', 'id_2', 'id_3']
)

results = alert_collection.query(
    query_texts=["package"], # Chroma will embed this for you
    n_results=1 # how many results to return
)

print(results)
