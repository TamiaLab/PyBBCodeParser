"""
SkCode tag tokenizer code.
"""

from .parser import parse_tag


# Token types
TOKEN_DATA = 0
TOKEN_NEWLINE = 1
TOKEN_OPEN_TAG = 2
TOKEN_CLOSE_TAG = 3
TOKEN_SELF_CLOSE_TAG = 4


def tokenize_newline(data):
    """
    Given a string that does not contain any tags, this function will
    yield a list of ``TOKEN_NEWLINE`` and ``TOKEN_DATA`` tokens in such way
    that if you concatenate their data, you will have the original string.
    N.B. Newline must have been normalized to ``\n`` before calling this function.
    :param data: Input data string to be tokenize.
    """
    lines = data.split('\n')
    last_line_num = len(lines) - 1
    for num, line in enumerate(lines):
        if line:
            yield TOKEN_DATA, None, None, line
        if num < last_line_num:
            yield TOKEN_NEWLINE, None, None, '\n'


def tokenize_tag(text, opening_tag_ch='[', closing_tag_ch=']',
                 allow_tagvalue_attr=True, allow_self_closing_tags=True):
    """
    Split the given text into tokens (generator function).
    :param text: The input text to be tokenize.
    :param opening_tag_ch: The opening tag char (must be one char long, default '[').
    :param closing_tag_ch: The closing tag char (must be one char long, default ']').
    :param allow_tagvalue_attr: Set to ``True`` to allow the BBcode ``tagname=tagvalue`` syntax shortcut
    (default ``True``).
    :param allow_self_closing_tags: Set to ``True`` to allow the self closing tags syntax (default ``True``).
    """
    assert text, "No text input given (mandatory)."
    assert len(opening_tag_ch) == 1, "Opening tag character must be one char long exactly."
    assert len(closing_tag_ch) == 1, "Closing tag character must be one char long exactly."

    # Normalize newlines
    text = text.replace('\r\n', '\n').replace('\r', '\n')

    # Search an opening tag
    start = text.find(opening_tag_ch)
    pos = 0

    # Process the whole text until no more tag can be found
    # N.B. string.find(s, beg) return -1 if beg >= len(string)
    while start >= 0:

        # Run the parser to get the tag
        try:
            tag = parse_tag(text, start,
                            opening_tag_ch, closing_tag_ch,
                            allow_tagvalue_attr, allow_self_closing_tags)
        
        except (IndexError, ValueError):

            # Continue searching if not a valid tag
            start = text.find(opening_tag_ch, start + 1)
            continue

        # Get the text before the tag, if any
        if start > pos:
            text_before_tag = text[pos:start]
            yield from tokenize_newline(text_before_tag)

        # Unpack the tag structure
        tag_name, is_closing_tag, is_self_closing_tag, tag_attrs, offset = tag
        tag_source = text[start:offset]

        # Yield the tag token
        if is_self_closing_tag:
            yield TOKEN_SELF_CLOSE_TAG, tag_name, tag_attrs, tag_source
        elif is_closing_tag:
            yield TOKEN_CLOSE_TAG, tag_name, tag_attrs, tag_source
        else:
            yield TOKEN_OPEN_TAG, tag_name, tag_attrs, tag_source
            
        # Store the current position in text for next loop
        pos = offset

        # Search the next tag if any
        start = text.find(opening_tag_ch, offset)

    # Yield the remaining piece of text if any
    remaining_text = text[pos:]
    if remaining_text:
        yield from tokenize_newline(remaining_text)
