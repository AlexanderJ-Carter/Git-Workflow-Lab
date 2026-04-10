#!/usr/bin/env python3
"""Compatibility wrapper for importing the site build script as a module."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


_SOURCE_PATH = Path(__file__).with_name("build-site.py")
_SPEC = spec_from_file_location("build_site_legacy", _SOURCE_PATH)

if _SPEC is None or _SPEC.loader is None:
    raise ImportError(f"Unable to load build script from {_SOURCE_PATH}")

_MODULE = module_from_spec(_SPEC)
_SPEC.loader.exec_module(_MODULE)

extract_title = _MODULE.extract_title
get_lesson_id = _MODULE.get_lesson_id
convert_markdown_to_html = _MODULE.convert_markdown_to_html
get_output_rel_path = _MODULE.get_output_rel_path
rewrite_markdown_links = _MODULE.rewrite_markdown_links
process_lesson_file = _MODULE.process_lesson_file
process_public_page = _MODULE.process_public_page
get_lesson_info = _MODULE.get_lesson_info
build_site = _MODULE.build_site


if __name__ == "__main__":
    build_site()
