from typedefs import VideoPresentation
from typing import List
import qdrant_client
from llama_index.vector_stores import QdrantVectorStore
from llama_index import VectorStoreIndex, StorageContext, ServiceContext
from llama_index.llms import Gemini
from llama_index.embeddings import GeminiEmbedding
from llama_index.schema import TextNode
from llama_index.retrievers import QueryFusionRetriever
import os

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

class BaseStorage:
    """An abstract base class for retrival data storage and retrival."""

    def __init__(self, videos: List[VideoPresentation]):
        pass

    def retrieve(self, q: str) -> List[VideoPresentation]:
        """Retrieve data from the storage section with the given id that are similar to the user's query."""
        pass


class LlamaIndexQdrantStorage:
    """A storage class for LlamaIndex + Qdrant storage."""

    def __init__(self, storage_path: str, videos: List[VideoPresentation]):
        self.index_transcript = self.create_index(storage_path + '_transcript', "transcript", videos)
        self.index_summary = self.create_index(storage_path + '_summary', "summary", videos)

    def create_index(self, storage_path: str, key: str, videos: List[VideoPresentation]) -> VectorStoreIndex:
        """Create a vector store index."""
        if os.path.exists(storage_path):
            os.system(f"rm -rf {storage_path}")
        client = qdrant_client.QdrantClient(path=storage_path)
        vector_store = QdrantVectorStore(client=client, collection_name=f"collection-{key}")
        embed_model = GeminiEmbedding(
            model_name="models/embedding-001", api_key=GOOGLE_API_KEY
        )
        service_context = ServiceContext.from_defaults(
            llm=Gemini(api_key=GOOGLE_API_KEY), embed_model=embed_model
        )
        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        nodes = []
        for video in videos:
            text_node = TextNode()
            metadata = {}
            metadata["path"] = video.path
            metadata["transcription"] = video.transcript
            metadata["summary"] = video.summary
            metadata['title'] = video.title
            metadata['url'] = video.url
            # if key == "transcript":
            #     text_node.text = video.transcript
            # elif key == "summary":
            #     text_node.text = video.summary
            # else:
            #     raise ValueError(f"Invalid key: {key}")
            text_node.metadata = metadata
            nodes.append(text_node)

        index = VectorStoreIndex(
            nodes=nodes,  # nodes will be added later
            service_context=service_context,
            storage_context=storage_context,
        )
        return index
    
    def retrieve(self, q: str, top_k: int) -> List[VideoPresentation]:
        """Retrieve data from the storage section with the given id that are similar to the user's query."""
        retriever = QueryFusionRetriever(
            retrievers=[
                self.index_transcript.as_retriever(similarity_top_k=top_k),
                self.index_summary.as_retriever(similarity_top_k=top_k),
            ],
            similarity_top_k=top_k*10,
            num_queries=top_k,
            use_async=False,
            verbose=True)
        # import pdb; pdb.set_trace()
        results = retriever.retrieve(q)
        output = []
        path_set = set()  # this is for deduplication
        for res in results:
            metadata = res.metadata
            path = metadata["path"]
            if path in path_set:
                continue
            transcript = metadata["transcription"]
            summary = metadata["summary"]
            output.append(
                VideoPresentation(
                    summary=summary, 
                    transcript=transcript, 
                    path=path,
                    title = metadata['title'],
                    url = metadata['url']))
            path_set.add(path)
        return output[:top_k]
