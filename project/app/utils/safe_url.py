from django.utils.html import format_html

# Tuple of default safe schemes.
SAFE_SCHEMES = ('http', 'https')

# An innocuous URL to use is an unsafe URL is passed in.
INNOCULOUS_URL = 'about:invalid'

def make_url_clickable(url):
    """Sanitizes the given url and makes it clickable.

    """
    return format_html("<a href='{url}'>{url}</a>", url=sanitize_url(url))

def sanitize_url(url):
    """Sanitizes the given url.

    It validates that the input string matches a pattern of commonly used safe
    URLs. If the url fails validation, this method returns an innocuous url.

    Specifically, the url may be a URL with any of the known safe schemes
    (http, https), or a relative URL (i.e., a URL without a scheme;
    specifically, a scheme-relative, absolute-path-relative, or path-relative
    URL).

    Logic is copied from Google SafeHtml library.

    Args:
      url: string with the URL to create a SafeURL of.
    Returns:
      The given URL, or a generic innocuous URL if the URL did not pass the
      sanitization checks.
    """

    url = url if is_safe_url(url) else INNOCULOUS_URL
    return url

def is_safe_url(url):
    """Checks if a URL is safe to be turned into a SafeUrl object.

    A URL is safe if it starts with a default safe protocol or it contains no
    protocol.

    Logic is copied from Google SafeHtml library.

    Args:
    url: string with the URL to check.
    Returns:
    Boolean denoting if the URL is safe or not.
    """
    lower_url = url.lower()
    for scheme in SAFE_SCHEMES:
        if lower_url.startswith(scheme + ':'):
          return True

    for char in url:
        if char in ('/', '?', '#'):
          return True
        if char in ('&', ':'):
          return False

    return True
