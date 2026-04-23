
# metadata = {
#     "text": content,
#     "chunk_index": len(chunks),
#     "original_type": "pdf",
#     "title": title,
#     "id": title+str(len(chunks))
# }
# Document(
#     page_content=text,
#     metadata={
#         **metadata, 
#         'source': file_path,
#         'chunk_size': chunk_size,
#         'overlap': overlap
# }