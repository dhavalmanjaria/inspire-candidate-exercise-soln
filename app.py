import bottle # https://bottlepy.org/docs/dev/tutorial_app.html
import sqlite3
import json

from request_processing.format_wombat_api import format_post
from validators.validate_wombat import validate_wombat_post

db = sqlite3.connect(':memory:')
db.row_factory = sqlite3.Row
db.executescript('''
    BEGIN TRANSACTION;
    CREATE TABLE wombat(id integer primary key, name varchar(128), dob date);
    INSERT INTO wombat VALUES(1,'Alice','1865-11-26');
    INSERT INTO wombat VALUES(2,'Queen','1951-07-26');
    INSERT INTO wombat VALUES(3,'Johnny','2010-03-05');
    COMMIT;
''')

@bottle.get('/wombats')
def get_wombats():

    cursor = db.cursor()

    results = cursor.execute('select * from wombat')
    retval = {'wombats': []}
    for r in results:
        item = {
            'id': r[0],
            'name': r[1],
            'dob': r[2]
        }
        retval['wombats'].append(item)
    cursor.close()
    return retval


@bottle.post('/wombats')
def create_wombats():
    post_data = bottle.request.body.read()
    post_data = post_data.decode('utf-8')

    post_data = post_data.strip()

    post_data = format_post(post_data)

    validity = validate_wombat_post(post_data)
    if validity.is_error:
        bottle.response.status = 400
        return f'Missing parameter: {validity.message}'

    cursor = db.cursor()
    id = cursor.execute('select id from wombat order by id desc limit 1')

    new_id = [i[0] for i in id]
    new_id = new_id[0] + 1
    cursor.close()
    new_item = {
        'id': new_id,
        'name': post_data['name'],
        'dob': post_data['dob']
    }

    ## Sanitize
    for k in post_data.keys():
        post_data[k] = post_data[k].replace('--', '')
        post_data[k] = post_data[k].replace(';', '')

    cursor = db.cursor()
    insert_query = f"insert into wombat values({new_id}, '{post_data['name']}', '{post_data['dob']}');"
    result = cursor.execute(insert_query)
    result = db.commit()

    return new_item




@bottle.get('/')
def index():
    bottle.response.content_type = 'text/plain'
    return "Inspire Candidate Exercise"

if __name__ == '__main__':
    import sys
    hostname = 'localhost'
    port = '8080'
    if len(sys.argv) >= 2:
        hostname = sys.argv[1]
    if len(sys.argv) >= 3:
        port = sys.argv[2]

    bottle.debug()
    bottle.run(host=hostname, port=int(port), reloader=True)
