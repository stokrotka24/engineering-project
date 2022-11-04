from enum import Enum


class SimilarityType(str, Enum):
    cosine_binary = "cosine_binary"
    cosine = "cosine"
    jaccard = "jaccard"
    centered_cosine = "centered_cosine"
