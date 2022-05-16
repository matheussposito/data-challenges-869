from nbresult import ChallengeResultTestCase
import numpy as np


class TestFeatureUnionCustomTransformers(ChallengeResultTestCase):
    def test_solution(self):
        truth_train = np.array([[-1.22474487, -1.22474487, -1.22474487,  0.57142857],
                                [ 0.        ,  0.        ,  0.        ,  0.625     ],
                                [ 1.22474487,  1.22474487,  1.22474487,  0.66666667]])


        truth_test = np.array([[-1.22474487, -3.67423461, -6.12372436,  0.57142857],
                               [ 0.        , -2.44948974, -4.89897949,  0.625     ],
                               [ 1.22474487, -1.22474487,  2.44948974,  0.66666667]])

        self.assertTrue(np.allclose(self.result.X_train_transformed, truth_train))
        self.assertTrue(np.allclose(self.result.X_test_transformed, truth_test))
