from enum import Enum


class SimilarityType(str, Enum):
    cosine_binary = "cosine_binary"
    cosine = "cosine"
    jaccard = "jaccard"
    cosine_normalized = "cosine_normalized"
