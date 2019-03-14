class HTMLWrapper(object):
    """A callable that converts strings to an HTML-formatted string.
    
    The returned HTML string does NOT currently support XHTML formatting.
    
    Instance initializer arguments:
    
    tag     -- The full opening tag to wrap the string within. If tag is
               None or '', the string will be formatted according to the
               other arguments and returned without any tag.

               Example: '<div class="eggs">'

    compact -- Whether to join the opening tag, the content and the closing
               tag to form a single line. If False, the lines are joined
               using the class-property line_separator (defaults to '\\n').
               
               Example result:

               '<div class="eggs">These are poached eggs.</div>'

    indent  -- The string used for content indentation if the compact
               parameter above is False. 

               Example result, for indent=('\\x20' * 4):

               '<select id="knight">
                    <option>black</option>
                    <option>white</option>
                </select>'
    
    The object returned by HTMLWrapper() accepts the following arguments
    when called as a function:
    
    content -- A string or iterable containing the content to be wrapped.
               If a value in the iterable is not a string object, its
               string equivalent as returned by str() will be used. For the 
               empty elements like <br> the content is ignored.

    escape  -- If the HTML special characters within the content should be
               converted to entities. If the content is the result of a
               previous HTMLWrapper callable, escape must be False, or the
               HTML format already applied will be lost (to entities).

    strip   -- Whether each line in a multiline content should be stripped.
               If the content is the result of a previous HTMLWrapper and
               strip=True and indent is not None, the previous indentation
               will be lost (stripped).
               
    A full example generating a selector is given below:
    
    # obtain a wrapper that doesn't compact its content, and indents it with
    # four spaces.
    make_select = HTMLWrapper('select class="knight"', False, '\\x20' * 4)
    # obtain a wrapper that puts its content and tags on a single line.
    make_option = HTMLWrapper('option')
    
    options = make_select([make_option('Option => %02d' % (i + 1), True, True) \\
        for i in range(16)])
    """
    
    _entities = {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}
    _empty_elements = ('area', 'base', 'br', 'col', 'embed', 'hr', 'img', \
        'input', 'meta', 'param', 'source', 'track', 'wbr')

    line_separator = '\n'
    
    def __init__(self, tag=None, compact=True, indent=None):
        super(HTMLWrapper, self).__init__()
        self.compact = compact
        self.indent = indent
        if not tag:
            # ensure the empty tag propagates None
            tag = None
        name = tag and tag.split(None, 1)[0]
        self._tag_name = name and name.lower()
        self._empty = self._tag_name in self._empty_elements
        self._closing_tag = name and ('</%s>' % name)
        self._opening_tag = tag and ('<%s>' % tag)

    @property
    def closing_tag(self):
        """Returns the closing HTML tag. Example: '</div>'."""
        return self._closing_tag
    
    @property
    def opening_tag(self):
        """Returns the opening HTML tag. Example: '<div class="special">'."""
        return self._opening_tag
    
    @property
    def tag_name(self):
        """Returns only the tag name in lowercase. Example: 'div'."""
        return self._tag_name

    @property
    def empty(self):
        """Returns True for the empty elements that take no content."""
        return self._empty
    
    def __call__(self, content=None, escape=False, strip=False):
        separator = '' if self.compact else self.line_separator
        if self._empty or not content:
            content = []
        if not self._empty:
            if content:
                if isinstance(content, str):
                    content = content.splitlines()
                for (i, s) in enumerate(content):
                    if not isinstance(s, str):
                        s = str(s)
                    if escape:
                        s = ''.join(self._entities.get(c, c) for c in s)
                    content[i] = s    
                if self.compact:
                    content = [''.join(s.strip() for s in content)]
                else:
                    indent = self.indent or ''
                    for (i, s) in enumerate(content):
                        if strip:
                            s = s.strip()
                        content[i] = '%s%s' % (indent, s)
            if self._closing_tag:
                content.append(self._closing_tag)
        if self._opening_tag:
            content.insert(0, self._opening_tag)
        return separator.join(content)
    
    def __repr__(self):
        tag = self._opening_tag[1:-1] if self._opening_tag else None
        return '%s.%s(tag=%r, compact=%r, indent=%r)' % (self.__class__.__module__, \
            self.__class__.__name__, tag, self.compact, self.indent)
