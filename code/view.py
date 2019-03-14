class HTMLWrapper(object):
    '''A callable that converts a string to an HTML-formatted string.
    
    The returned HTML string does NOT currently support XHTML formatting.
    
    Instance initializer arguments:
    tag     -- The full opening tag to wrap the string within.
               Example: '<div class="eggs">'
    compact -- Whether to join the opening tag, the content and the closing
               tag to form a single line.
               Example: '<div class="eggs">These are poached eggs.</div>'
    indent  -- The string used for content indentation if the compact
               parameter above is False. Example, for indent=('\x20' * 4):
               '<select id="knight">
                    <option>black</option>
                    <option>white</option>
                </select>'
    
    The callable produced by HTMLWrapper() accepts the following arguments:
    content -- A string containing the content to be wrapped.
    escape  -- If the HTML special characters within the content should be
               converted to entities. If the content is the result of a
               previous HTMLWrapper callable, escape must be False, or the
               HTML format already applied will be lost (to entities).
    strip   -- Whether each line in a multiline content should be stripped.
               If the content is the result of a previous HTMLWrapper and
               strip=True and indent is not None, the previous indentation
               will be lost (stripped).
    '''

    _entities = {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}
    _empty_elements = ('area', 'base', 'br', 'col', 'embed', 'hr', 'img', \
        'input', 'meta', 'param', 'source', 'track', 'wbr')

    def __init__(self, tag=None, compact=True, indent=None):
        super(HTMLWrapper, self).__init__()
        self.compact = compact
        self.indent = indent
        name = tag.split(None, 1)[0] if tag else None
        self._tag_name = name or name.lower()
        self._empty = (self._tag_name in self._empty_elements) if name \
            else False
        self._closing_tag = '</%s>' % name if (name and not self._empty) \
            else None
        self._opening_tag = '<%s>' % tag if tag else None

    @property
    def closing_tag(self):
        '''Returns the closing HTML tag. Example: '</div>'.'''
        return self._closing_tag
    
    @property
    def opening_tag(self):
        '''Returns the opening HTML tag. Example: '<div class="special">'.'''
        return self._opening_tag
    
    @property
    def tag_name(self):
        '''Returns only the tag name in lowercase. Example: 'div'.'''
        return self._tag_name

    @property
    def empty(self):
        '''Returns True for the empty elements that take no content.'''
        return self._empty
    
    def __call__(self, content=None, escape=False, strip=False):
        parts = []
        separator = '' if self.compact else '\n'
        if self._opening_tag:
            parts.append(self._opening_tag)
        if (not self._empty):
            if content:
                if escape:
                    content = ''.join(self._entities.get(c, c) \
                        for c in content)
                if self.compact:
                    content = ''.join(s.strip() for s in content.splitlines())
                else:
                    indent = self.indent or ''
                    content = separator.join('%s%s' % (indent, (s.strip() \
                        if strip else s)) for s in content.splitlines())
                parts.append(content)
            if self._closing_tag:
                parts.append(self._closing_tag)
        return separator.join(parts)
    
    def __repr__(self):
        tag = self._opening_tag[1:-1] if self._opening_tag else None
        return '%s.%s(tag=%r, compact=%r, indent=%r)' % (self.__class__.__module__, \
            self.__class__.__name__, tag, self.compact, self.indent)
