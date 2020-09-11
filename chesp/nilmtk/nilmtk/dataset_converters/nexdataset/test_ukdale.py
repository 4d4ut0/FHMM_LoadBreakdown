






from nilmtk.dataset_converters import convert_ukdale
convert_ukdale('nexdataset', 'nexdataset.h5')









"""
import numpy as np
from hmmlearn import hmm
hmm.GaussianHMM(n_components=2)
modelo= hmm.GaussianHMM(algorithm='viterbi', covariance_type='full', covars_prior=0.01,
      covars_weight=1, init_params='stmc', means_prior=0, means_weight=0,
      min_covar=0.001, n_components=3, n_iter=10, params='stmc',
      random_state=None, startprob_prior=1.0, tol=0.01, transmat_prior=1.0,
      verbose=False)

X=np.asarray([
            [1.0e+02, 2.0e+02, 3.0e+02, 3.0e+02],
            [3.0e+02, 2.0e+02, 3.0e+02, 3.0e+02],
            [3.0e+02, 3.0e+02, 3.0e+02, 3.0e+02]
        ])
modelo.fit(X)

h = hmm.GaussianHMM(3)
h.fit(X)

"""