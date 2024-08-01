#!/use/bin/env python3
'''logging by hiding secure data'''
import re


def filter_datum(fields, redaction, message, separator):
    '''filter dataum'''
    for field in fields:
        match = re.match(rf".*{field}=([^{separator}]+){separator}.*", message)
        message = re.sub(f"{match.group(1)}", redaction, message)
    return message
