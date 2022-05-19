# import numpy as np

# # Avoid checking for import-error here because cython_example may not have
# # been compiled yet.
# try:
#     from .cython_example import geo_to_h3_vect  # pylint: disable=import-error
# except ImportError:
#     geo_to_h3_vect = None

# np.random.seed(0)


# def test_cython_api():
#     if geo_to_h3_vect is None:
#         print("Not running Cython test because cython example was not compiled")
#         return

#     N = 100000

#     lats, lngs = np.random.uniform(0, 90, N), np.random.uniform(0, 90, N)
#     res = 9

#     lats = np.array(lats, dtype=np.float64)
#     lngs = np.array(lngs, dtype=np.float64)
#     out = np.zeros(len(lats), dtype="uint64")
#     geo_to_h3_vect(lats, lngs, res, out)

#     assert out[0] == 617284541015654399
