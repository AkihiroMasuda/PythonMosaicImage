# -*- coding:utf-8 -*-
#! /usr/bin/env python  
  
"""
éQçlÅFhttp://blog.liris.org/2011/10/python-usrbinenv-pythonimport.html
"""
import mimetypes  
import os.path  
import random  
import sys  
import urllib  
import urllib2  
  
OS_FILESYSTEM_ENCODING = sys.getfilesystemencoding()  
  
FORMENCODE_HEADERS = {  
     "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",  
     "Accept-Language": "ja",  
     "Accept-Charset": "utf-8"}  
  
MULTIPART_HEADERS = {  
     "Content-Type": 'multipart/form-data; boundary=',  
     "Accept-Language": "ja",}  
  
  
          
def is_multipart(postdata):  
    for value in postdata.values():  
        if isinstance(value, file):  
            return True  
    return False  
  
def encode_postdata(postdata):  
    getRandomChar = lambda: chr(random.choice(range(97, 123)))  
    randomChar = [getRandomChar() for x in xrange(20)]  
    boundary = "----------%s" % ("".join(randomChar))  
    lines = ["--" + boundary]  
    for key, value in postdata.iteritems():  
        header = 'Content-Disposition: form-data; name="%s"' % key  
        if hasattr(value, "name"):  
            name = value.name  
            if isinstance(name, str):  
                name = name.decode(OS_FILESYSTEM_ENCODING)  
            header += '; filename="%s"' % os.path.split(name.encode("utf-8"))[-1]  
            lines.append(header)  
            mtypes = mimetypes.guess_type(value.name)  
            if mtypes:  
                contentType = mtypes[0]  
                header = "Content-Type: %s" % contentType  
                lines.append(header)  
            lines.append("Content-Transfer-Encoding: binary")  
        else:  
            lines.append(header)  
  
        lines.append("")  
        if hasattr(value, "read"):  
            lines.append(value.read())  
        elif isinstance(value, unicode):  
            lines.append(value.encode("utf-8"))  
        else:  
            lines.append(value)  
        lines.append("--" + boundary)  
    lines[-1] += "--"  
  
    return "\r\n".join(lines), boundary  
  
  
  
def open_url(url, postdata=None, headers = None):  
    encoded = None  
    _headers = None  
    if postdata:  
        if is_multipart(postdata):  
            encoded, boundary = encode_postdata(postdata)  
            _headers = MULTIPART_HEADERS.copy()  
            _headers["Content-Type"] = _headers["Content-Type"] + boundary  
        else:  
            encoded = urllib.urlencode(postdata)  
            _headers = FORMENCODE_HEADERS  
  
    request = urllib2.Request(url, encoded)  
    if _headers:  
        for key, value in _headers.iteritems():  
            request.add_header(key, value)  
    if headers:  
        for key, value in headers.iteritems():  
            request.add_header(key, value)  
    opener = urllib2.build_opener()  
    response = opener.open(request)  
  
    return response  
  