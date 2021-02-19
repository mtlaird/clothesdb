def add_item_form():
    form_html = "<form method=post>\n"\
                "<p>Create a new item of clothing with the following tags:</p>\n"\
                "<div id=tagFieldsContainer></div>\n"\
                "<input type=submit></form>"

    return form_html


def add_tags_form():
    form_html = "<form method=post>\n"\
                "<p>Add new tags:</p>\n"\
                "<div id=tagFieldsContainer></div>\n"\
                "<input type=submit></form>"

    return form_html


def replace_tag_form():
    form_html = "<form method=post>\n" \
                "<p>Replace current tag with new tag:</p>\n" \
                "<p>Type: <input type=text name='tag-type' size=10 autocomplete=off>\n" \
                "Value: <input type=text name='tag-value' size=10 autocomplete=off></p>\n" \
                "<input type=submit></form>"
    return form_html


def item_tag_list_table(taglist):
    html = "Tags for item:<br>\n<table border=0>"
    for tag in taglist:
        html += "<tr><td><a href='/tags/types/{}'>{}</a></td><td>{}</td></tr>".format(tag[0], tag[0], tag[1])
    html += "</table>"
    return html


def full_tag_list_table(taglist):
    html = "Tags:<br>\n<table border=0>"
    for tag in taglist:
        html += "<tr><td><a href='/tags/types/{}'>{}</a></td>" \
                "<td>{}</td><td><a href='/tags/{}/items'>{}</a></td></tr>".format(tag[0], tag[0], tag[1], tag[2],
                                                                                  tag[3])
    html += "</table>"
    return html


def item_summary_table(item_summaries):
    html = "<table border=0>\n" \
           "<tr><th>Type</th><th>Color</th><th>Tags</th></tr>\n"
    for i in item_summaries:
        html += "<tr><td>{}</td><td>{}</td><td><a href='/items/{}'>{}</a></td></tr>\n".format(i[1], i[2], i[0], i[3])
    html += "</table>"
    return html


def include_javascript_header():
    header = "<header>\n"\
             "<script src=/webapp.js></script>\n"\
             "</header>\n"

    return header
