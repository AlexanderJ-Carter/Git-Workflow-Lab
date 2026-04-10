#!/usr/bin/env python3
"""Compatibility wrapper for importing the quote fixer as a module."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


_SOURCE_PATH = Path(__file__).with_name("fix-quotes.py")
_SPEC = spec_from_file_location("fix_quotes_legacy", _SOURCE_PATH)

if _SPEC is None or _SPEC.loader is None:
    raise ImportError(f"Unable to load quote fixer from {_SOURCE_PATH}")

_MODULE = module_from_spec(_SPEC)
_SPEC.loader.exec_module(_MODULE)

fix_quotes = _MODULE.fix_quotes
main = _MODULE.main


if __name__ == "__main__":
    main()
