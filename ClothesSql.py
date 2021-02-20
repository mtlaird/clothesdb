import sqlite3


def create_schema(conn):
    create_items_table_sql = "create table if not exists items (item_id integer primary key)"
    create_tags_table_sql = "create table if not exists tags (tag_id integer primary key, type, value, " \
                            "unique(type, value))"
    create_item_tag_links_table_sql = "create table if not exists items_tags (item_id, tag_id, unique(item_id, tag_id))"

    c = conn.cursor()
    c.execute(create_items_table_sql)
    c.execute(create_tags_table_sql)
    c.execute(create_item_tag_links_table_sql)
    c.close()


def initialize_db():
    conn = sqlite3.connect("clothes.db")
    create_schema(conn)
    return conn


def add_new_item(conn):
    insert_item_sql = "insert into items default values"
    c = conn.cursor()
    c.execute(insert_item_sql)
    row_id = c.execute("select last_insert_rowid()").fetchone()[0]
    conn.commit()
    c.close()
    return row_id


def add_new_tag(conn, tag_type, value):
    insert_tag_sql = "insert into tags (type, value) VALUES (?, ?)"
    c = conn.cursor()
    c.execute(insert_tag_sql, (tag_type, value))
    row_id = c.execute("select last_insert_rowid()").fetchone()[0]
    conn.commit()
    c.close()
    return row_id


def add_item_tag_link(conn, item_id, tag_id):
    insert_link_sql = "insert into items_tags (item_id, tag_id) values (?, ?)"
    c = conn.cursor()
    c.execute(insert_link_sql, (item_id, tag_id))
    try:
        row_id = c.execute("select last_insert_rowid()").fetchone()[0]
        conn.commit()
    except sqlite3.IntegrityError:
        # Failed unique constraint, attempt to add a link that already exists, so just ignore it
        # We don't use the row_id, so we can just drop it on the floor
        row_id = None
    c.close()
    return row_id


def add_taglist_to_item(conn, item_id, tag_list):
    for tag_type, value in tag_list:
        tag_id = get_tag_id(conn, tag_type, value)
        add_item_tag_link(conn, item_id, tag_id)
    return item_id


def create_new_item_with_tags(conn, tag_list):
    item_id = add_new_item(conn)
    for tag_type, value in tag_list:
        tag_id = get_tag_id(conn, tag_type, value)
        add_item_tag_link(conn, item_id, tag_id)
    return item_id


def get_tag_id(conn, tag_type, value):
    select_tag_sql = "select tag_id from tags where type = ? and value = ?"
    c = conn.cursor()
    c.execute(select_tag_sql, (tag_type, value))
    res = c.fetchall()
    if len(res) == 1:
        c.close()
        return res[0][0]
    c.close()
    return add_new_tag(conn, tag_type, value)


def get_tag_data(conn, tag_id):
    select_tag_sql = "select type, value from tags where tag_id = ?"
    c = conn.cursor()
    c.execute(select_tag_sql, (tag_id,))
    res = c.fetchall()
    if len(res) == 1:
        c.close()
        return res[0][0], res[0][1]
    c.close()
    return False


def get_items_by_tag_id(conn, tag_id):
    select_items_sql = "select item_id from items_tags where tag_id = ?"
    c = conn.cursor()
    c.execute(select_items_sql, (tag_id,))
    res = c.fetchall()
    item_ids = []
    for row in res:
        item_ids.append(row[0])
    c.close()
    return item_ids


def get_summary_for_item(conn, item_id):
    summary = [item_id]
    select_tag_value_sql = "select t.value from items_tags it inner join tags t on it.tag_id = t.tag_id " \
                           "where t.type = ? and item_id = ? limit 1"
    c = conn.cursor()
    c.execute(select_tag_value_sql, ("Type", item_id))
    res = c.fetchall()
    if len(res) != 1:
        return None
    summary.append(res[0][0])
    c.close()
    c = conn.cursor()
    c.execute(select_tag_value_sql, ("Color", item_id))
    res = c.fetchall()
    if len(res) != 1:
        return None
    summary.append(res[0][0])
    c.close()
    summary.append(count_tags_by_item(conn, item_id))
    return summary


def get_tags_by_item_id(conn, item_id):
    select_tags_sql = "select t.type, t.value from items_tags it " \
                      "inner join tags t on it.tag_id = t.tag_id where item_id = ?"
    c = conn.cursor()
    c.execute(select_tags_sql, (item_id,))
    res = c.fetchall()
    tags = []
    for row in res:
        tags.append(row)
    c.close()
    return tags


def get_all_tags_with_item_count(conn):
    select_tags_sql = "select type, value, t.tag_id, count(it.item_id) from tags t " \
                      "inner join items_tags it on t.tag_id = it.tag_id " \
                      "group by it.tag_id order by type, value"
    c = conn.cursor()
    c.execute(select_tags_sql)
    res = c.fetchall()
    tags = []
    for row in res:
        tags.append(row)
    c.close()
    return tags


def count_tags_by_type(conn, tag_type):
    count_tags_sql = "select count(value) from tags where type = ?"
    c = conn.cursor()
    c.execute(count_tags_sql, (tag_type,))
    res = c.fetchone()
    c.close()
    return res[0]


def count_tags_by_item(conn, item_id):
    count_tags_sql = "select count(*) from items_tags where item_id = ?"
    c = conn.cursor()
    c.execute(count_tags_sql, (item_id,))
    res = c.fetchone()
    c.close()
    return res[0]


def count_items_by_tag(conn, tag_id):
    count_items_sql = "select count(*) from items_tags where tag_id = ?"
    c = conn.cursor()
    c.execute(count_items_sql, (tag_id,))
    res = c.fetchone()
    c.close()
    return res[0]


def get_item_summaries(conn, item_id_list):
    summaries = []
    for item_id in item_id_list:
        summary = get_summary_for_item(conn, item_id)
        if summary:
            summaries.append(summary)
    return summaries


def get_all_item_ids(conn, limit=None, offset=None):
    get_ids_sql = "select item_id from items "
    if offset:
        get_ids_sql += "where item_id > {} ".format(offset)
    if limit:
        get_ids_sql += "limit {}".format(limit)
    c = conn.cursor()
    c.execute(get_ids_sql)
    res = c.fetchall()
    c.close()
    item_ids = []
    for row in res:
        item_ids.append(row[0])
    return item_ids


def get_all_tag_types(conn, limit=None):
    get_types_sql = "select DISTINCT(tag_type) from tags "
    if limit:
        get_types_sql += "limit {} ".format(limit)
    get_types_sql += "order by tag_type"
    c = conn.cursor()
    c.execute(get_types_sql)
    res = c.fetchall()
    c.close()
    types = []
    for row in res:
        types.append(row[0])
    return types


def get_tags_by_type_with_count(conn, tag_type):
    get_tags_sql = "select type, value, t.tag_id, count(it.item_id) from tags t " \
                   "inner join items_tags it on t.tag_id = it.tag_id " \
                   "where type = ? group by it.tag_id order by type, value"
    c = conn.cursor()
    c.execute(get_tags_sql, (tag_type,))
    res = c.fetchall()
    c.close()
    return res


def replace_tag(conn, new_tag_id, old_tag_id):
    replace_tags_sql = "update items_tags set tag_id = ? where tag_id = ?"
    c = conn.cursor()
    c.execute(replace_tags_sql, (new_tag_id, old_tag_id))
    c.execute("select changes()")
    res = c.fetchone()
    num_changes = res[0]
    c.close()
    return num_changes


def delete_tag(conn, tag_id):
    delete_tag_sql = "delete from tags where tag_id = ?"
    if count_items_by_tag(conn, tag_id) > 0:
        return False
    c = conn.cursor()
    c.execute(delete_tag_sql, (tag_id,))
    c.close()
    return True
