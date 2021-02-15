from bottle import route, run, get, post, static_file, request
from ClothesWebContent import *
import ClothesSql as sql


def extract_tags_from_request(r):
    tag_number = 0
    tags = []
    while True:
        tag_type = r.forms.get('tag-type-' + str(tag_number))
        tag_value = r.forms.get('tag-value-' + str(tag_number))
        if tag_type == "" or tag_value == "":
            break
        tags.append((tag_type, tag_value))
        tag_number += 1
    return tags


@route('/')
def index():
    html = "Welcome!<br>" \
           "<a href='/tags'>View all tags</a>.<br>" \
           "<a href='/items'>View all items</a>.<br>" \
           "<a href='/add_item'>Add an item</a> to the database."
    return html


@get('/add_item')
def add_item_get():
    return include_javascript_header() + "<body onload='createNewTagFieldSet()'>" + add_item_form() + "</body>"


@post('/add_item')
def add_item_post():
    tags = extract_tags_from_request(request)

    conn = sql.initialize_db()
    new_row_id = sql.create_new_item_with_tags(conn, tags)

    html = "<p><a href='/items/{}'>New item created</a> with {} tags.</p>".format(new_row_id, len(tags))
    html += "<p><a href='/add_item'>Add another item.</a></p>"

    return html


@route('/items/<item_id>', method=['GET', 'POST'])
def get_item(item_id=None):
    conn = sql.initialize_db()

    if request.method == "POST":
        add_tags = extract_tags_from_request(request)
        sql.add_taglist_to_item(conn, int(item_id), add_tags)

    taglist = sql.get_tags_by_item_id(conn, int(item_id))

    return include_javascript_header() + "<body onload='createNewTagFieldSet()'>" + item_tag_list_table(taglist) + \
        add_tags_form() + "</body>"


@get('/items')
def get_all_items():
    conn = sql.initialize_db()

    item_ids = sql.get_all_item_ids(conn)
    item_summaries = sql.get_item_summaries(conn, item_ids)

    return item_summary_table(item_summaries) + "<br><a href='/add_item'>Add an item</a> to the database."


@get('/tags')
def get_all_tags():
    conn = sql.initialize_db()

    taglist = sql.get_all_tags_with_item_count(conn)

    return full_tag_list_table(taglist)


@get('/tags/<tag_id>/items')
def get_items_by_tags(tag_id):
    conn = sql.initialize_db()

    item_ids = sql.get_items_by_tag_id(conn, int(tag_id))
    item_summaries = sql.get_item_summaries(conn, item_ids)

    return item_summary_table(item_summaries)


@get('/tags/types/<tag_type>')
def get_tags_by_type(tag_type):
    conn = sql.initialize_db()

    taglist = sql.get_tags_by_type_with_count(conn, tag_type)

    return full_tag_list_table(taglist)


@get('/webapp.js')
def send_js():
    return static_file('webapp.js', 'static')


run(host="localhost", port=5566)
