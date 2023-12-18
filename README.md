# PyHarm

**Polyharmonic spline interpolation in PyTorch**

---

PyHarm is a PyTorch module designed for efficient [polyharmonic spline interpolation](https://en.wikipedia.org/wiki/Polyharmonic_spline). Leveraging GPU acceleration, this implementation excels in performance, making it well-suited for large-scale interpolation tasks.

## Installation

Install PyHarm using the following command:

```bash
pip install pyharm
```

PyHarm has minimal dependencies, requiring only PyTorch and NumPy.

If you're interested in contributing or want to use PyHarm in developer/editable mode with test dependencies, install it as follows:

```bash
pip install -e pyharm[test]
```

To run the tests, simply execute:

```bash
pytest <path-to-pyharm>
```

## Explore

Check out the [examples](https://github.com/ivanZanardi/pyharm/tree/main/examples) provided in the repository to see PyHarm in action.

## License

PyHarm is distributed under the [MIT license](https://github.com/ivanZanardi/pyharm/blob/main/LICENSE). Feel free to use, modify, and contribute to this project within the terms of the license.
