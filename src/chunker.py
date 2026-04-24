def chunk_text(text,chunk_size = 500, overlap = 100):
    chunks=[]
    for i in range(0,len(text),chunk_size-overlap):
        chunks.append(text[i:i+chunk_size])
        
    return chunks
        
def hierarchical_chunk(text):
    lines = text.splitlines()
    chunks = []
    txt = ""
    for line in lines:
        if line.startswith("#"):
            if txt:  
                if len(txt) > 500:
                    chunks.extend(chunk_text(txt))
                else:
                    chunks.append(txt)
            txt = ""
        txt += line + "\n"
    
    if len(txt) > 1000:
        chunks.extend(chunk_text(txt))
    else:
        chunks.append(txt)
    
    return chunks
        
            
            
        
    