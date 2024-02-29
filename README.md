# grl_amod_with_pt
This repository contains the codebase of my master's thesis. It is about the use of graph-based reinforcement learning for integrating autonomous on-demand services with regular public transportation.

## Technology Choices

It was decided to develop the framework in Python. The Graph Convolutional Networks are developed using PyTorch in combination with PyTorch Geometric. Possible multithreading can be implemented with the `multiprocessing` package, taking care to ensure that only inputs and outputs (e.g., `Queue`) are visible in the main process. Overall, the framework is designed in an object-oriented manner, where type annotations must be attached, and type safety is ensured by `mypy`.

### Important Documentation Links

- **PyTorch Geometric (PyG)**: An extension library for PyTorch, specially designed for deep learning on graphs and other irregular structures.
  - [PyTorch Geometric Documentation](https://pytorch-geometric.readthedocs.io/en/latest/)

- **`multiprocessing`**: A package for concurrent execution using processes, providing an easy way to parallelize Python code.
  - [Multiprocessing Documentation](https://docs.python.org/3/library/multiprocessing.html)

- **`mypy`**: A static type checker for Python, ensuring that type annotations are correct and consistent throughout the codebase.
  - [Mypy Documentation](http://mypy-lang.org/)
