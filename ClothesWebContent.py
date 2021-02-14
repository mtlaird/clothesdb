def add_item_form():
    form_html = "<form method=post>\n"\
                "<p>Create a new item of clothing with the following tags:</p>\n"\
                "<div id=tagFieldsContainer></div>\n"\
                "<input type=submit></form>"

    return form_html


def include_javascript_header():
    header = "<header>\n"\
             "<script src=webapp.js></script>\n"\
             "</header>\n"

    return header
