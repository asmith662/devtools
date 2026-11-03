import sys
sys.path.insert(0, 'C:\\Users\\recoveryadmin\\Workspace\\tools\\devtools\\src')
sys.path.insert(0, 'C:\\Users\\recoveryadmin\\Workspace\\tools\\devtools')
import pytest
raise SystemExit(pytest.main(['tests/live_native_markdown_hash_public.py', 'tests/resources/filesystem/models/markdown/test_file.py', 'tests/resources/filesystem/models/markdown/test_heading.py', 'tests/resources/filesystem/models/markdown/test_section.py', 'tests/resources/filesystem/codecs/test_markdown.py', '--no-cov', '--import-mode=importlib', '-q']))
