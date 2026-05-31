from setuptools.command.build_ext import build_ext
from setuptools.extension import Extension
from warnings import warn
import sysconfig

EXTENSIONS = [
    Extension(
        name="onotation.internal.trie.c_trie",
        sources=["onotation/internal/trie/c_trie.c"],
        include_dirs=[sysconfig.get_path("include")],
        extra_compile_args=["-O3"],
    ),
]


class Builder(build_ext):
    def build_extension(self, ext):
        try:
            super().build_extension(ext)
        except Exception as e:
            warn(f"Build failed {ext.name}: {e}")


def build(setup_kwargs: dict):
    setup_kwargs.update(
        {
            "cmdclass": {"build_ext": Builder},
            "ext_modules": EXTENSIONS,
        }
    )