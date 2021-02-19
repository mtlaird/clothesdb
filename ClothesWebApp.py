from bottle import route, run, get, post, static_file, request
import ClothesWebContent as Web
import ClothesSql as Sql


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
    return Web.include_javascript_header() + "<body onload='createNewTagFieldSet()'>" + Web.add_item_form() + "</body>"


@post('/add_item')
def add_item_post():
    tags = extract_tags_from_request(request)

    conn = Sql.initialize_db()
    new_row_id = Sql.create_new_item_with_tags(conn, tags)

    html = "<p><a href='/items/{}'>New item created</a> with {} tags.</p>".format(new_row_id, len(tags))
    html += "<p><a href='/add_item'>Add another item.</a></p>"

    return html


@route('/items/<item_id>', method=['GET', 'POST'])
def get_item(item_id=None):
    conn = Sql.initialize_db()

    if request.method == "POST":
        add_tags = extract_tags_from_request(request)
        Sql.add_taglist_to_item(conn, int(item_id), add_tags)

    taglist = Sql.get_tags_by_item_id(conn, int(item_id))

    return Web.include_javascript_header() + "<body onload='createNewTagFieldSet()'>" + \
        Web.item_tag_list_table(taglist) + Web.add_tags_form() + "</body>"


@get('/items')
def get_all_items():
    conn = Sql.initialize_db()

    item_ids = Sql.get_all_item_ids(conn)
    item_summaries = Sql.get_item_summaries(conn, item_ids)

    return Web.item_summary_table(item_summaries) + "<br><a href='/add_item'>Add an item</a> to the database."


@get('/tags')
def get_all_tags():
    conn = Sql.initialize_db()

    taglist = Sql.get_all_tags_with_item_count(conn)

    return Web.full_tag_list_table(taglist)


@get('/tags/<tag_id>/items')
def get_items_by_tags(tag_id):
    conn = Sql.initialize_db()

    item_ids = Sql.get_items_by_tag_id(conn, int(tag_id))
    item_summaries = Sql.get_item_summaries(conn, item_ids)

    return Web.item_summary_table(item_summaries)


@route('/tags/<tag_id>/manage', method=['GET', 'POST'])
def manage_tag(tag_id):
    conn = Sql.initialize_db()
    html = ""
    current_tag = Sql.get_tag_data(conn, tag_id)
    if request.method == "GET":
        html += "<p>Replace tag {} - {}:</p>".format(current_tag[0], current_tag[1])
        html += Web.replace_tag_form()

    if request.method == "POST":
        new_tag = request.forms.get("tag-type"), request.forms.get("tag-value")
        new_tag_id = Sql.add_new_tag(conn, new_tag[0], new_tag[1])
        html += "<p>Replacing tag {} - {} with {} - {} ...</p>".format(current_tag[0], current_tag[1],
                                                                   new_tag[0], new_tag[1])
        tags_replaced = Sql.replace_tag(conn, new_tag_id, tag_id)
        html += "<p>Replaced {} tags.</p>".format(tags_replaced)

    return html


@get('/tags/types/<tag_type>')
def get_tags_by_type(tag_type):
    conn = Sql.initialize_db()

    taglist = Sql.get_tags_by_type_with_count(conn, tag_type)

    return Web.full_tag_list_table(taglist)


@get('/webapp.js')
def send_js():
    return static_file('webapp.js', 'static')


run(host="localhost", port=5566)
