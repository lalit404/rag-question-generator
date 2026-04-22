def embed_chunks(chunks,model):
    # embbed_chunks =[]
    # for chunk in chunks:
    #     embbed_chunks.append(model.encode(chunk))
    # embbed_chunks.appned(model.encode(chunks))
        
    return model.encode(chunks) 

#The library handles the loop internally. It takes your list, encodes each string one by one inside its own code, and returns all embeddings together as a 2D array.
#You don't need to write the loop because the library already wrote it for you.