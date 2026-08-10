import pickle

with open("vector_db/chunks.pkl","rb") as f:
    chunks = pickle.load(f)

for i in range(3):
    print("\nCHUNK",i)
    print(chunks[i][:500])
    