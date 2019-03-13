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
        '''The closing HTML tag, like in </div>.'''
        return self._closing_tag
    
    @property
    def opening_tag(self):
        '''The opening HTML tag, like in <div class="special">.'''
        return self._opening_tag
    
    @property
    def tag_name(self):
        '''The tag name without attributes, like in "div".'''
        return self._tag_name

    @property
    def empty(self):
        '''True if this is an empty element, accepting no content.'''
        return self._empty
    
    def __call__(self, content=None, escape=False, strip=False):
        parts = []
        separator = '' if self.compact else '\n'
        if self._opening_tag:
            parts.append(self._opening_tag)
        if (not self._empty):
            if content:
                if not isinstance(content, str):
                    content = str(content)
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

class TableWrapper(HTMLWrapper):
    
    def __init__(self, attributes=None, compact=False, indent=None):
        tag = 'table'
        if attributes:
            tag = '%s %s' % (tag, attributes)
        super(TableWrapper, self).__init__(tag, compact, indent)
        self.attributes = attributes
        
    def __call__(self, records, labels=None):
        headers = []
        keys = tuple(records[0].keys())
        # callables must be created here to take in account changes of the
        # instance attributes
        tr = HTMLWrapper('tr', self.compact, self.indent)
        th = HTMLWrapper('th')
        td = HTMLWrapper('td')
        thead = HTMLWrapper('thead', self.compact, self.indent)
        tbody = HTMLWrapper('tbody', self.compact, self.indent)
        for (i, s) in enumerate(keys):
            if labels and (i < len(labels)) and labels[i]:
                s = labels[i]
            headers.append(th(s, True, True))
        headers = thead(tr('\n'.join(headers)))
        datarows = []
        for r in records:
            datarows.append(tr('\n'.join(td(r[k], True, True) \
                for k in keys)))
        datarows = tbody('\n'.join(datarows))
        return super(TableWrapper, self).__call__('%s\n%s' % (headers, datarows))
