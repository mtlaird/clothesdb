from bottle import route, run, get, post, static_file, request
from ClothesWebContent import *
from ClothesSql import initialize_db, create_new_item_with_tags


@route('/')
def index():
    return "Welcome!"


@get('/add_item')
def add_item_get():
    return include_javascript_header() + "<body onload='createNewTagFieldSet()'>" + add_item_form() + "</body>"


@post('/add_item')
def add_item_post():
    tag_number = 0
    tags = []
    while True:
        tag_type = request.forms.get('tag-type-' + str(tag_number))
        tag_value = request.forms.get('tag-value-' + str(tag_number))
        if tag_type == "" or tag_value == "":
            break
        tags.append((tag_type, tag_value))
        tag_number += 1

    conn = initialize_db()
    new_row_id = create_new_item_with_tags(conn, tags)

    html = "<p>New item created with id {} and {} tags.</p>".format(new_row_id, len(tags))
    html += "<p><a href='/add_item'>Add another item.</a></p>"

    return html


@get('/webapp.js')
def send_js():
    return static_file('webapp.js', 'static')


run(host="localhost", port=5566)
