class HTMLWrapper(object):

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
        '''The closing HTML tag, like </div>'''
        return self._closing_tag
    
    @property
    def opening_tag(self):
        '''The opening HTML tag, like <div class="special">'''
        return self._opening_tag
    
    @property
    def tag_name(self):
        '''The tag name without attributes, like "div"'''
        return self._tag_name

    @property
    def empty(self):
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
