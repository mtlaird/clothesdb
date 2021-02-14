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
    row_id = c.execute("select last_insert_rowid()").fetchone()[0]
    conn.commit()
    c.close()
    return row_id


def create_new_item_with_tags(conn, tag_list):
    item_id = add_new_item(conn)
    for tag_type, value in tag_list:
        tag_id = add_new_tag(conn, tag_type, value)
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


def get_tags_by_item_id(conn, item_id):
    select_tags_sql = "select tag_id from items_tags where item_id = ?"
    c = conn.cursor()
    c.execute(select_tags_sql, (item_id,))
    res = c.fetchall()
    tag_ids = []
    for row in res:
        tag_ids.append(row[0])
    c.close()
    return tag_ids


def count_tags_by_type(conn, tag_type):
    count_tags_sql = "select count(value) from tags where type = ?"
    c = conn.cursor()
    c.execute(count_tags_sql, (tag_type,))
    res = c.fetchone()
    c.close()
    return res[0]
