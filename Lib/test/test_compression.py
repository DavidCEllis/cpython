import unittest

from test import support
from test.support.import_helper import import_fresh_module

import compression


@support.requires_bz2()
@support.requires_gzip()
@support.requires_lzma()
@support.requires_zlib()
@support.requires_zstd()
class TestAvailableModules(unittest.TestCase):
    def test_all_modules_available(self):
        # To some extent this is checking the support decorators work correctly
        expected = {
            "bz2",
            "gzip",
            "lzma",
            "zlib",
            "zstd",
        }
        self.assertEqual(compression.AVAILABLE_MODULES, expected)

    @support.thread_unsafe("Modifies global import state")
    def test_all_modules_unavailable(self):
        # Test no formats are listed if all c implementations are blocked
        expected = set()
        new_compression = import_fresh_module(
            "compression",
            blocked=("_bz2", "_lzma", "zlib", "_zstd"),
            cleared=("bz2", "gzip", "lzma", "compression", "compression.zstd"),
        )

        assert new_compression is not None

        self.assertEqual(new_compression.AVAILABLE_MODULES, expected)

    @support.thread_unsafe("Modifies global import state")
    def test_bz2_unavailable(self):
        expected = {"gzip", "lzma", "zlib", "zstd"}
        new_compression = import_fresh_module(
            "compression",
            blocked=("_bz2",),
            cleared=(
                "bz2",
                "gzip",
                "lzma",
                "compression",
                "compression.zstd",
                "_bz2",
                "_lzma",
                "zlib",
                "_zstd"
            ),
        )

        assert new_compression is not None

        self.assertEqual(new_compression.AVAILABLE_MODULES, expected)

    @support.thread_unsafe("Modifies global import state")
    def test_lzma_unavailable(self):
        expected = {"bz2", "gzip", "zlib", "zstd"}
        new_compression = import_fresh_module(
            "compression",
            blocked=("_lzma",),
            cleared=(
                "bz2",
                "gzip",
                "lzma",
                "compression",
                "compression.zstd",
                "_bz2",
                "_lzma",
                "zlib",
                "_zstd"
            ),
        )

        assert new_compression is not None

        self.assertEqual(new_compression.AVAILABLE_MODULES, expected)

    @support.thread_unsafe("Modifies global import state")
    def test_zlib_unavailable(self):
        expected = {"bz2", "lzma", "zstd"}
        new_compression = import_fresh_module(
            "compression",
            blocked=("zlib",),
            cleared=(
                "bz2",
                "gzip",
                "lzma",
                "compression",
                "compression.zstd",
                "_bz2",
                "_lzma",
                "zlib",
                "_zstd"
            ),
        )

        assert new_compression is not None

        self.assertEqual(new_compression.AVAILABLE_MODULES, expected)

    @support.thread_unsafe("Modifies global import state")
    def test_zstd_unavailable(self):
        expected = {"bz2", "gzip", "lzma", "zlib"}
        new_compression = import_fresh_module(
            "compression",
            blocked=("_zstd",),
            cleared=(
                "bz2",
                "gzip",
                "lzma",
                "compression",
                "compression.zstd",
                "_bz2",
                "_lzma",
                "zlib",
                "_zstd"
            ),
        )

        assert new_compression is not None

        self.assertEqual(new_compression.AVAILABLE_MODULES, expected)
