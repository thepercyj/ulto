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

# The URL prefix the generated pages are served under, which search uses to
# build links and to fetch pages when summarising a result.
DOCS_ROOT = '/docstrings/'

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

    # Links between pages name a route. Any anchor on the end is kept. This has
    # to cover the search form's action as well as ordinary links: the form on
    # every page posts to search.html, which is not a URL the site answers on.
    def page_link(match):
        attribute, page, anchor = match.group(1), match.group(2), match.group(3)
        route = PAGE_ROUTES.get(page)
        if route is None:
            return match.group(0)
        return f'{attribute}="{{{{ url_for(\'{route}\') }}}}{anchor or ""}"'

    html = re.sub(r'(href|action)="([a-z_-]+\.html)(#[^"]*)?"', page_link, html)

    # Search builds URLs from this root at runtime. Left as "./" it resolves
    # against whichever page is open, which is not where the pages are served.
    html = html.replace('data-content_root="./"', f'data-content_root="{DOCS_ROOT}"')

    # Sphinx stamps the build year into the footer, which would then age until
    # the next rebuild. These pages are rendered as templates, so the range is
    # left to the same context the rest of the site uses and stays current
    # without one. Matches a single year or a range, whichever was stamped.
    html = re.sub(r'(&#169; Copyright )\d{4}(?:[-–]\d{4})?(,)',
                  r'\1{{ copyright_years }}\2', html)
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

    # Search appends these suffixes when turning an indexed page name into a
    # URL. The pages are served by route rather than by filename, so the
    # suffixes are cleared and "interpreter" resolves to /docstrings/interpreter
    # instead of a .html file that does not exist.
    options = STATIC / 'documentation_options.js'
    text = options.read_text(encoding='utf-8')
    for key in ('FILE_SUFFIX', 'LINK_SUFFIX'):
        # Anchored, or LINK_SUFFIX would also match inside SOURCELINK_SUFFIX.
        text = re.sub(rf"\b{key}: '[^']*',", f"{key}: '',", text)
    options.write_text(text, encoding='utf-8')

    print(f'  installed {installed} pages into {TEMPLATES.relative_to(ROOT)}')
    print(f'  installed assets into {STATIC.relative_to(ROOT)}')
    print('  cleared search URL suffixes in documentation_options.js')


def check():
    """
    Reports anything left that would not resolve once served.
    """
    problems = []
    for page in sorted(TEMPLATES.glob('*.html')):
        text = page.read_text(encoding='utf-8')
        # `action` is checked alongside the link attributes, since the search
        # form pointing at a file rather than a route is exactly the kind of
        # reference that renders fine and then 404s when used.
        for match in re.findall(r'(?:href|src|action)="(?!\{\{|#|http|mailto:)([^"]+)"', text):
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
