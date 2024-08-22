from numpy import ndarray
from typing import Protocol
from src.data_types import Cluster, Embedding

class SimilarityMetric(Protocol):
    @staticmethod
    def measure(left: ndarray, right: ndarray) -> ndarray:
        ...


class ClusterMap(Protocol):
    def classify(self, cluster_centers: ndarray, emebdding: ndarray, metric: SimilarityMetric) -> Cluster:
        ...
