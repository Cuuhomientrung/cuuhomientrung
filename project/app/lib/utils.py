import codecs
import sys
import traceback

def check_contain_filter(topic, contain_filter):
    '''
    function
    --------
    check if topic satisfiy contain_filters in format "a;b;c" means (a or b or c)
    :input:
        topic (string|list): string|list to search
    '''
    if isinstance(topic, list):
        content_string = [x.lower() for x in topic]
    else:
        content_string = topic.lower()
    search_string = contain_filter.lower()

    or_term_satisfy = False
    for or_term in search_string.split(';'):
        if or_term.strip() != '':
            if or_term.strip() in content_string: # current or_term is in search_string
                or_term_satisfy = True
                break

    return or_term_satisfy

def check_keyword_filter(document, main_keyword, support_keyword=None, exclude_keyword=None):
    """Filter document with keywords"""
    main_filter = check_contain_filter(document, main_keyword)

    if support_keyword:
        support_filter = check_contain_filter(document, support_keyword)
    else:
        support_filter = True
    
    if exclude_keyword:
        exlude_filter = check_contain_filter(document, exclude_keyword)
    else:
        exclude_filter = False
    
    return main_filter and support_filter and (not exclude_filter)




def open_utf8_file_to_read(filename):
    try:
        return codecs.open(filename, "r", "utf-8")
    except:
        return None


def open_utf8_file_to_write(filename):
    try:
        return codecs.open(filename, "w+", "utf-8")
    except:
        return None

def print_exception():
    # Print error message in try..exception
    exec_info = sys.exc_info()
    traceback.print_exception(*exec_info)

