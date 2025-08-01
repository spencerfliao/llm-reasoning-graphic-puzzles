import torch
from transformers import AutoTokenizer, AutoModel
import nltk
from nltk.tokenize import sent_tokenize
import pickle
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


class ReflectionsEmbedder:
    def __init__(self, model_name="bert-base-uncased"):
        nltk.download("punkt")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.model.eval()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    def tokenize_reflections(self, text):
        """Tokenize the reflections text into sentences."""
        return sent_tokenize(text)

    def generate_embeddings(self, text):
        """Generate embeddings for a piece of text."""
        inputs = self.tokenizer(
            text, padding=True, truncation=True, max_length=512, return_tensors="pt"
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        with torch.no_grad():
            outputs = self.model(**inputs)
        # Get the embeddings from the last hidden state
        embeddings = outputs.last_hidden_state.mean(dim=1)
        return embeddings.cpu().numpy()

    def aggregate_embeddings(self, sentences):
        """Aggregate sentence embeddings by averaging."""
        embeddings = [self.generate_embeddings(sentence) for sentence in sentences]
        aggregated_embedding = np.mean(embeddings, axis=0)
        return aggregated_embedding

    def process_dataset(self, file_path, save_path="embeddings.pkl"):
        """Process the reflections from a TSV file and save embeddings."""
        data = pd.read_csv(file_path, sep="\t", usecols=["Filename", "Reflections"])
        embeddings = {}
        for _, row in data.iterrows():
            sentences = self.tokenize_reflections(row["Reflections"])
            aggregated_embedding = self.aggregate_embeddings(sentences)
            embeddings[row["Filename"]] = aggregated_embedding
        with open(save_path, "wb") as f:
            pickle.dump(embeddings, f)


class ContextSearch:
    def __init__(self, embeddings_path, model_name="bert-base-uncased"):
        with open(embeddings_path, "rb") as f:
            self.embeddings = pickle.load(f)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.model.eval()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    def generate_embedding(self, text):
        """Generate embedding for the given text."""
        inputs = self.tokenizer(
            text, padding=True, truncation=True, max_length=512, return_tensors="pt"
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        with torch.no_grad():
            outputs = self.model(**inputs)
        embedding = outputs.last_hidden_state.mean(dim=1)
        return embedding.cpu().numpy()

    def search(self, query_text, num_results=5):
        """Search for the most similar reflections based on the query text."""
        query_embedding = self.generate_embedding(query_text)
        similarities = {}
        for filename, embedding in self.embeddings.items():
            sim = cosine_similarity(query_embedding, embedding.reshape(1, -1))[0][0]
            similarities[filename] = sim
        sorted_filenames = sorted(
            similarities.items(), key=lambda item: item[1], reverse=True
        )
        top_filenames = [filename for filename, _ in sorted_filenames[:num_results]]
        return top_filenames


# How to use the context search
# embeddings_path = "<Path to the embeddings.pkl file>"
# context_search = ContextSearch(embeddings_path)

# query_text = "Tasks that involve changing the size of the objects"
# top_filenames = context_search.search(query_text, num_results=5)
# This will return the top 5 filenames that are most similar to the query text.

# Note: For the dashboard, you do now need to use the ReflectionsEmbedder class. You can directly use
# the ContextSearch class to search for similar reflections based on the query text.
# ReflectionsEmbedder was used to generate the embeddings for the reflections and save them to a file.
# The ContextSearch class can be used to load the embeddings and search for similar reflections based on the query text.
