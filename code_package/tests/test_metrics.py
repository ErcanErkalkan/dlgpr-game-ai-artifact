import unittest

from dlgpr.metrics import mean_std_ci, paired_cohens_dz, paired_mean_difference_ci, paired_rank_biserial


class TestMetrics(unittest.TestCase):
    def test_small_sample_ci_uses_student_t(self):
        _mean, std, ci = mean_std_ci([0.0, 1.0])
        self.assertGreater(std, 0.0)
        self.assertGreater(ci, 1.96 * std / (2 ** 0.5))

    def test_paired_effect_sizes_follow_difference_direction(self):
        better = [3.0, 4.0, 5.0, 6.0]
        worse = [1.0, 1.0, 2.0, 2.0]
        self.assertGreater(paired_rank_biserial(better, worse), 0.0)
        self.assertGreater(paired_cohens_dz(better, worse), 0.0)

    def test_paired_bootstrap_ci_is_reproducible(self):
        first = paired_mean_difference_ci([2.0, 4.0, 5.0], [1.0, 1.0, 3.0])
        second = paired_mean_difference_ci([2.0, 4.0, 5.0], [1.0, 1.0, 3.0])
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
