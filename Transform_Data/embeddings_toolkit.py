import logging
from sentence_transformers import SentenceTransformer

import numpy as np

# logging, Warning level, to file
logging.basicConfig(level=logging.INFO)

sentences = ["The device: PDX-RO details\n Hostname: PDX-RO\n Location: Global/OR/PDX/Floor-2\n Device Role: BORDER ROUTER"]

print('\n\n' + sentences[0] + '\n')

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
embeddings = model.encode(sentences)[0]
print(embeddings)

# Save to a text file
np.savetxt("output.txt", embeddings)