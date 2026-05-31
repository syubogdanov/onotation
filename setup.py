from setuptools import Extension, setup


trie_extension = Extension(
    "onotation.internal.trie.c_trie",
    sources=[
        "onotation/internal/trie/c_trie.c",
    ],
)

setup(
    ext_modules=[trie_extension],
)