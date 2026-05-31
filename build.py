from setuptools.command.build_ext import build_ext
from setuptools.extension import Extension
from warnings import warn
import sysconfig

EXTENSIONS = [
    Extension(
        name="onotation.internal.avl_tree.c_avl_tree",
        sources=["onotation/internal/avl_tree/c_avl_tree.c"],
        include_dirs=[sysconfig.get_path('include')],
        extra_compile_args=["-03"] if sysconfig.get_platform().startswith("linux") else [],
    ),
]

class Builder(build_ext):
    """Custom builder to suppress compile errors during development."""
    def build_extension(self, ext: Extension) -> None:
        """Build the extension.

        Notes
        -----
        * Suppresses build errors.
        """
        try:
            build_ext.build_extension(self, ext)
        except Exception as e:
            warn(f"Failed to build extension {ext.name}: {e}. Python fallback will be used.",
                 RuntimeWarning, stacklevel=2)


def build(setup_kwargs: dict) -> None:
    """Update the setup settings.

    Notes
    -----
    * Updates the builder;
    * Updates the extensions.
    """
    setup_kwargs.update({
        "cmdclass": {"build_ext": Builder},
        "ext_modules": EXTENSIONS,
    })