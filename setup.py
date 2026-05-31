from setuptools.command.build_ext import build_ext
from setuptools.extension import Extension
from warnings import warn
import sysconfig
import sys

EXTENSIONS = [
    Extension(
        name="onotation.internal.avl_tree.c_avl_tree",
        sources=["onotation/internal/avl_tree/c_avl_tree.c"],
        include_dirs=[sysconfig.get_path('include')],
        extra_compile_args=["-O3", "-Wall"],
    ),
]

class Builder(build_ext):
    def build_extension(self, ext):
        try:
            build_ext.build_extension(self, ext)
            print(f"Successfully built C extension: {ext.name}")
        except Exception as e:
            print(f"Failed to build {ext.name}: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    from setuptools import setup
    setup(
        name="onotation",
        ext_modules=EXTENSIONS,
        cmdclass={"build_ext": Builder},
    )
