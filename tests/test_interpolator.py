import torch
import unittest
import numpy as np

from pyharm import PolyHarmInterpolator


class TestInterpolator(unittest.TestCase):

  def setUp(self):
    # Setup common variables for tests
    self.batch_size = 2
    self.nb_points = 10
    self.dim = 3
    self.nb_features = 4
    self.order = 2
    self.smoothing = 0.001
    self.device = 'cpu'
    self.dtype = torch.float
    self.nb_query_points = 5
    # Create random input data
    self.train_points = np.random.rand(
      self.batch_size,
      self.nb_points,
      self.dim
    )
    self.train_values = np.random.rand(
      self.batch_size,
      self.nb_points,
      self.nb_features
    )
    self.query_points = np.random.rand(
      self.batch_size,
      self.nb_query_points,
      self.dim
    )
    self.query_values_shape = (
      self.batch_size,
      self.nb_query_points,
      self.nb_features
    )

  def test_class_construction(self):
    interpolator = PolyHarmInterpolator(
      c=self.train_points,
      f=self.train_values,
      order=self.order,
      smoothing=self.smoothing,
      device=self.device,
      dtype=self.dtype
    )
    self.assertIsInstance(interpolator, PolyHarmInterpolator)

  def test_forward_pass(self):
    interpolator = PolyHarmInterpolator(
      c=self.train_points,
      f=self.train_values,
      order=self.order,
      smoothing=self.smoothing,
      device=self.device,
      dtype=self.dtype
    )
    result = interpolator.forward(self.query_points)
    self.assertEqual(result.shape, self.query_values_shape)

  def test_interpolation_consistency(self):
    # Test that interpolating at training points gives the same values
    interpolator = PolyHarmInterpolator(
      c=self.train_points,
      f=self.train_values,
      order=self.order,
      smoothing=self.smoothing,
      device=self.device,
      dtype=self.dtype
    )
    result = interpolator.forward(self.train_points)
    np.testing.assert_allclose(result.numpy(), self.train_values, rtol=1e-5)

if __name__ == '__main__':
  unittest.main()
