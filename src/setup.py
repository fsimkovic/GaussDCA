
from Cython.Build import cythonize
from setuptools import setup, Extension


C_COMPILE_FLAGS = ["-O2", "-march=native", "-pipe", "-std=c11"]
C_LINK_FLAGS = ["-O2", "-march=native", "-pipe", "-std=c11"]


EXTENSIONS = [
    Extension('_gaussdca', ['_gaussdca.pyx'], extra_compile_args=C_COMPILE_FLAGS, extra_link_args=C_LINK_FLAGS),
    Extension('_gaussdca_parallel', ['_gaussdca_parallel.pyx'], extra_compile_args=C_COMPILE_FLAGS + ["-fopenmp"], 
        extra_link_args=C_LINK_FLAGS + ["-fopenmp"]),
    Extension('_gaussdca_parallel_opt', ['_gaussdca_parallel_opt.pyx'], extra_compile_args=C_COMPILE_FLAGS + ["-fopenmp"], 
        extra_link_args=C_LINK_FLAGS + ["-fopenmp"]),
]


setup(ext_modules=cythonize(EXTENSIONS))
