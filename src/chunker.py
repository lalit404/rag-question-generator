def chunk_text(text,chunk_index,metadatas,current_chapter,chunk_size = 500, overlap = 100):
    chunks=[]
    for i in range(0,len(text),chunk_size-overlap):
        chunks.append(text[i:i+chunk_size])
        chunk_index+=1
        metadatas.append({"c_index":chunk_index,"chapter": current_chapter})
        
    return chunks
        
def hierarchical_chunk(text):
    lines = text.splitlines()
    chunks = []
    metadatas = []
    txt_lines = []
    chunk_index = 1
    current_chapter = "Unknown"
    for line in lines:
        if line.startswith("#"):
            current_chapter = line.strip("#")
            if txt_lines: 
                chunk_index=build_chunk(txt_lines,chunks,chunk_index,metadatas,current_chapter)
            txt_lines = []
        txt_lines.append(line +  "\n")
        
    chunk_index=build_chunk(txt_lines,chunks,chunk_index,metadatas,current_chapter)
    
    return chunks,metadatas

def build_chunk(txt_lines,chunks,chunk_index,metadatas,current_chapter):
    txt = ''.join(txt_lines)
    if len(txt) > 1000:
        chunks.extend(chunk_text(txt,chunk_index,metadatas,current_chapter))
    else:
        chunks.append(txt)
        chunk_index+=1
        metadatas.append({"c_index":chunk_index,"chapter": current_chapter})
    
    return chunk_index