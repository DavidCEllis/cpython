def _get_available_modules() -> frozenset[str]:
    # Test that the internal C implementations are present for support
    formats = set()
    try:
        import _bz2
        del _bz2
    except ImportError:
        pass
    else:
        formats.add("bz2")

    try:
        import _lzma
        del _lzma
    except ImportError:
        pass
    else:
        formats.add("lzma")

    try:
        import zlib
        del zlib
    except ImportError:
        pass
    else:
        formats.add("gzip")
        formats.add("zlib")

    try:
        import _zstd
        del _zstd
    except ImportError:
        pass
    else:
        formats.add("zstd")

    return frozenset(formats)

AVAILABLE_MODULES: frozenset[str] = _get_available_modules()
