def decode_modified_utf7(encoded_string):
    """
    Decodes a modified UTF-7 encoded string to UTF-8.
    """
    return encoded_string.replace(b'&', b'+').decode('utf-7')

def encode_modified_utf7(string):
    """
    Encodes a string to modified UTF-7 encoding used by IMAP.
    """
    utf7 = string.encode('utf-7')
    return utf7.replace(b'+', b'&')
