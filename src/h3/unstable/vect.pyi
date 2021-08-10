from typing import Optional

import numpy as np
from numpy.typing import NDArray

def h3_to_parent(
    h: NDArray[np.uint64], res: Optional[int] = None
) -> NDArray[np.uint64]: ...
def h3_get_resolution(h: NDArray[np.uint64]) -> NDArray[np.intc]: ...
def geo_to_h3(
    lats: NDArray[np.number], lngs: NDArray[np.number], res: int
) -> NDArray[np.uint64]: ...
def cell_haversine(
    a: NDArray[np.uint64], b: NDArray[np.uint64]
) -> NDArray[np.float64]: ...
