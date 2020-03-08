from __future__ import annotations
from typing import TypeVar, Generic, List, Sequence
from copy import deepcopy
from functools import partial
from random import uniform
from statistics import mean, pstdev
from dataclasses import dataclass
from data_point import DataPoint

def zscore(original: Sequence[float]) -> List[float]:
    avg: float = mean(original)
    std: float = pstdev(original)
    if std == 0: return [0] * len(original)
    return [(x - avg) / std for x in original]

Point = TypeVar('Point', bound = DataPoint)

class KMeans(Generic[Point]):
    @dataclass
    class Cluster:
        points: List[Point]
        centroid: DataPoint

    def __init__(self, k: int, points: List[Point]) -> None:
        if k < 1: raise ValueError("k must be >= 1")
        self._points: List[Point] = points
        self._zscore_normalize()
        self._cluster: List[KMeans.Cluster] = []
        for _ in range(k):
            rand_point: DataPoint = self._rando

    @property
    def _centroids(self) -> List[DataPoint]:
        return [x.centroid for x in self._cluster]

    def _dimension_slice(self, dimension: int) -> List[float]:
        return [x.dimensions[dimension] for x in self._points]

    def _zscore_normalize(self) -> None:
        zscored: List[List[float]] = [[] for _ in range(len(self._points))]
        for dimension in range(self._points[0].num_dimensions):
            dimension_slice: List[float] = self._dimension_slice(dimension)
            for index, zscore in enumerate(zscore(dimension_slice)):
                zscored[index].append(zscore)
        for i in range(len(self._points)):
            self._points[i].dimensions = tuple(zscored[i])

    def _random_point(self) -> DataPoint:
        rand_dimensions: List[float] = []
        for dimension in range(self._points[0].dimensions):
            values: List[float] = self._dimension_slice(dimension)
            rand_value: float = uniform(min(values), max(values))
            rand_dimensions.append(rand_value)
        return DataPoint(rand_dimensions)

    def _generate_centroids(self) -> None:
        for cluster in self.



