import requests
 
def charsets(res):
    _charset = requests.utils.get_encoding_from_headers(res.headers)
    if _charset == 'ISO-8859-1':
        __charset = requests.utils.get_encodings_from_content(res.text)
        if __charset:
            _charset = __charset[0]
        else:
            _charset = res.apparent_encoding
 
    return _charset