import numpy as np
import contextlib
import warnings
import torch
import math


class PolyHarmInterpolator(torch.nn.Module):
    """
    Polyharmonic spline interpolator.
    See https://en.wikipedia.org/wiki/Polyharmonic_spline.

    @param y: (n, d) tensor of data point coordinates
    @param d: (n, m) tensor of data vectors at y
    @param neighbors (optional): int [CURRENTLY UNIMPLEMENTED] specifies the
        number of neighbors to use for each interpolation point. If
        None, all points are used.
        Default is None.
    @param smoothing (optional): float or (n,) tensor of smoothing parameters
        Default is 0.0.
    @param kernel (optional): str, kernel function to use; one of
        ['linear', 'thin_plate_spline', 'cubic', 'quintic', 'gaussian'
        'multiquadric', 'inverse_multiquadric', 'inverse_quadratic']
        Default is 'thin_plate_spline'.
    @param epsilon (optional): float, shape parameter for the kernel function.
        If kernel is 'linear', 'thin_plate_spline', 'cubic', or
        'quintic', then default is 1.0 and can be ignored. Must be
        specified otherwise.
    @param degree (optional): int, degree of the polynomial added to the
        interpolation function. See scipy.interpolate.RBFInterpolator
        for more details.
    @param device (optional): str, specifies the default device to store tensors
        and perform interpolation.

    Returns a callable Torch Module that interpolates the data at given points.
    """

    def __init__(
        self,
        y,
        d,
        neighbors=None,
        smoothing=0.0,
        kernel="thin_plate_spline",
        epsilon=None,
        degree=None,
        device="cpu",
    ):
        super().__init__()



  """Polyharmonic interpolant.
  See https://en.wikipedia.org/wiki/Polyharmonic_spline.
  """

  # Initialization
  # ===================================
  def __init__(
    self,
    x,
    y,
    order=3,
    smoothing=0.0,
    xform=None,
    *args,
    **kwargs
  ):
    # Set data
    self.x, self.y = x, y
    # Get tensor ranks
    self.ranks = {"x": len(self.x.shape), "y": len(self.y.shape)}
    # Set order and smoothing
    self.order = int(np.clip(order, 1.0, 3.0))
    self.smoothing = float(smoothing)
    # Set transformation
    if (xform in (None, "lin")):
      self.xform = None
    elif (xform == "log"):
      self.xform = (ops.log, ops.exp)
    else:
      utils.raise_err(
        ValueError,
        "Input 'xform' not recognized. Valid options: [None, 'lin', 'log']"
      )
    # Set axis order for rank reduction/expansion
    self.axis = (-1,-1) if (_cfg.method == "stacked") else (0,-1)
    # Set default rank of input/output tensors
    self.rank = 3
    # Fit the interpolant to the observed data
    self._build()

  # Class methods - Public
  # ===================================
  def __call__(self, x):
    # Reshape
    x = self._to_rank(x, self.rank)
    # Apply interpolation
    y = self._apply(x)
    # Transform
    if (self.xform is not None):
      y = self.xform[1](y)
    # Reshape
    y = self._to_rank(y, self.ranks["y"])
    return y

  # Class methods - Public
  # ===================================
  def _build(self):
    # Transform
    y = self.y
    if (self.xform is not None):
      y = self.xform[0](y)
    # Reshape
    self.train = {
      "x": self._to_rank(self.x, self.rank),
      "y": self._to_rank(y, self.rank)
    }
    # Compute coefficients
    self.w, self.v = self._solve()

  def _apply(
    self,
    x
  ):
    """Apply polyharmonic interpolation model to data.

    Given coefficients w and v for the interpolation model, we evaluate
    interpolated function values at query points 'x'.

    Args:
      x: `[b, m, d]` x values to evaluate the interpolation at.

    Returns:
      Polyharmonic interpolation evaluated at points defined in `query_points`.
    """
    # First, compute the contribution from the rbf term.
    pairwise_dists = self._cross_squared_distance_matrix(x, self.train["x"])
    phi_pairwise_dists = self._phi(pairwise_dists, self.order)
    rbf_term = ops.matmul(phi_pairwise_dists, self.w)
    # Then, compute the contribution from the linear term.
    # Pad query_points with ones, for the bias term in the linear model.
    x_pad = ops.concat([x, ops.ones_like(x[..., :1])], 2)
    linear_term = ops.matmul(x_pad, self.v)
    return rbf_term + linear_term

  def _solve(
    self
  ):
    """Solve for interpolation coefficients.

    Computes the coefficients of the polyharmonic interpolant for the
    'training' data defined by `(train_points, train_values)` using the kernel
    $\phi$.

    Returns:
      w: `[b, n, k]` weights on each interpolation center
      v: `[b, d, k]` weights on each input dimension
    Raises:
      ValueError: if d or k is not fully specified.
    """
    # First, rename variables so that the notation (c, f, w, v, A, B, etc.)
    # follows https://en.wikipedia.org/wiki/Polyharmonic_spline.
    # To account for python style guidelines we use
    # matrix_a for A and matrix_b for B.
    c, f = self.train["x"], self.train["y"]
    # Get dimensions
    b, n, d = list(c.shape)
    k = f.shape[-1]
    # Construct the linear system
    matrix_a = self.phi(
      self._pairwise_squared_distance_matrix(c), self.order
    )
    if (self.smoothing > 0):
      batch_identity_matrix = torch.unsqueeze(torch.eye(n), dim=0)
      matrix_a += self.smoothing * batch_identity_matrix
    # Append ones to the feature values for the bias term in the linear model
    ones = ops.ones_like(c[..., :1])
    matrix_b = ops.concat([c, ones], 2)
    left_block = ops.concat([matrix_a, ops.transpose(matrix_b, [0, 2, 1])], 1)
    num_b_cols = matrix_b.shape[2]
    lhs_zeros = ops.zeros([b, num_b_cols, num_b_cols])
    right_block = ops.concat([matrix_b, lhs_zeros], 1)
    lhs = ops.concat([left_block, right_block], 2)
    # > Right hand side
    rhs_zeros = ops.zeros([b, d + 1, k])
    rhs = ops.concat([f, rhs_zeros], 1)
    # Solve the linear system and unpack the results
    w_v = ops.solve(lhs, rhs)
    w = w_v[:, :n, :]
    v = w_v[:, n:, :]
    return w, v
