# Ulto - Imperative Reversible Programming Language
#
# refresh-docs.py
#
# Aman Thapa Magar <at719@sussex.ac.uk>

"""
Rebuilds the docstring pages and installs them where the site serves them from.

The /docstrings pages are Sphinx output, but they are not served as static
files. They are rendered as Jinja templates, so every asset path and every link
between pages has to be rewritten to go through Flask's url_for. Doing that by
hand is why the built copy under docs/ and the served copy under templates/html
drifted apart. This script performs the rewrite, so refreshing the pages after a
docstring change is one command.

Usage:
    python refresh-docs.py
"""

import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BUILD = ROOT / 'docs' / 'build' / 'html'
TEMPLATES = ROOT / 'templates' / 'html'
STATIC = ROOT / 'static' / '_static'

# Each generated page is reachable through a route in ulto.py rather than by
# filename, so links between pages are rewritten to name the route instead.
PAGE_ROUTES = {
    'index.html': 'docstrings',
    'genindex.html': 'genindex',
    'search.html': 'search',
    'core.html': 'core',
    'lexer.html': 'lexer',
    'parser.html': 'parser',
    'semantic_analyser.html': 'semantic_analyser',
    'interpreter.html': 'interpreter',
    'lazyeval.html': 'lazyeval',
    'malloc.html': 'malloc',
    'logstack.html': 'logstack',
    'trace.html': 'trace',
}


def build():
    """
    Runs Sphinx over docs/source, failing loudly if it reports a problem.
    """
    print('building docs...')
    if BUILD.exists():
        shutil.rmtree(BUILD)
    result = subprocess.run(
        [sys.executable, '-m', 'sphinx', '-b', 'html',
         str(ROOT / 'docs' / 'source'), str(BUILD), '-q'],
        capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stdout + result.stderr)
        sys.exit('sphinx build failed')
    warnings = (result.stdout + result.stderr).strip()
    print(f'  built {len(list(BUILD.glob("*.html")))} pages'
          + (f', with warnings:\n{warnings}' if warnings else ', no warnings'))


def rewrite(html):
    """
    Turns one generated page into a template the site can render.

    Args:
        html (str): The page as Sphinx produced it.

    Returns:
        str: The page with asset paths and page links routed through url_for.
    """
    # "View page source" points at the .rst that produced the page, which is not
    # published, so the link is dropped rather than left to 404.
    html = re.sub(r'<a href="_sources/[^"]*"[^>]*>.*?</a>', '', html)

    # Assets live under the Flask static directory. Sphinx appends a cache
    # busting query, which url_for does not take, so it is dropped.
    html = re.sub(
        r'(href|src)="_static/([^"?]+)(\?[^"]*)?"',
        lambda m: f'{m.group(1)}="{{{{ url_for(\'static\', filename=\'_static/{m.group(2)}\') }}}}"',
        html)

    # Links between pages name a route. Any anchor on the end is kept.
    def page_link(match):
        route = PAGE_ROUTES.get(match.group(1))
        if route is None:
            return match.group(0)
        # A page linked without an anchor leaves group(2) unset.
        anchor = match.group(2) or ''
        return f'href="{{{{ url_for(\'{route}\') }}}}{anchor}"'

    html = re.sub(r'href="([a-z_-]+\.html)(#[^"]*)?"', page_link, html)
    return html


def install():
    """
    Writes the rewritten pages and their assets into the served locations.
    """
    # Both directories are rebuilt from scratch, so a page that is no longer
    # generated does not linger and get served.
    for target in (TEMPLATES, STATIC):
        if target.exists():
            shutil.rmtree(target)
    TEMPLATES.mkdir(parents=True)

    installed = 0
    for page in sorted(BUILD.glob('*.html')):
        if page.name not in PAGE_ROUTES:
            # No route serves it, so publishing it would only add a dead end.
            print(f'  skipping {page.name} (no route)')
            continue
        (TEMPLATES / page.name).write_text(
            rewrite(page.read_text(encoding='utf-8')), encoding='utf-8')
        installed += 1

    # Carried over for parity with how the pages were previously published.
    # The .rst sources are not, since the links to them have been removed.
    for extra in ('searchindex.js', 'objects.inv'):
        if (BUILD / extra).exists():
            shutil.copy2(BUILD / extra, TEMPLATES / extra)

    shutil.copytree(BUILD / '_static', STATIC)

    print(f'  installed {installed} pages into {TEMPLATES.relative_to(ROOT)}')
    print(f'  installed assets into {STATIC.relative_to(ROOT)}')


def check():
    """
    Reports anything left that would not resolve once served.
    """
    problems = []
    for page in sorted(TEMPLATES.glob('*.html')):
        text = page.read_text(encoding='utf-8')
        for match in re.findall(r'(?:href|src)="(?!\{\{|#|http|mailto:)([^"]+)"', text):
            problems.append(f'{page.name}: {match}')
    if problems:
        print('  unrouted references left behind:')
        for p in problems[:10]:
            print(f'    {p}')
    else:
        print('  no unrouted references')


if __name__ == '__main__':
    build()
    install()
    check()
