try:
    from tempfile import TemporaryDirectory
except ImportError:
    from ._tempdir import TemporaryDirectory
