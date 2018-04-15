import sys
sys.path.append ( "./ijson" )
import json
import ijson
from collections import Counter

melbgrid_json = './melbGrid.json'
instagram_json = './tinyInstagram.json'


def load_grid(grid_filename):
    melbgrid = json.load ( open ( grid_filename ) )
    grid = list ()
    for g in melbgrid[ 'features' ]:
        grid.append ( g[ 'properties' ] )
    return grid


#
# def parse_json(json_filename):
#     with open(json_filename, 'rb') as input_file:
#         # load json iteratively
#         parser = ijson.parse(input_file)
#         for prefix, event, value in parser:
#             print('prefix={}, event={}, value={}'.format(prefix, event, value))

# parse_json(instagram_json)

def parse_grid(json_filename):
    # input_file = open(instagram_json, 'rb')
    with open ( json_filename, 'rb' ) as input_file:
        # load json iteratively
        rows = ijson.items ( input_file, 'rows.item.doc' )
        locations = (r for r in rows if r[ 'location' ] == 'melbourne')

        post_counter = Counter ()
        row_counter = Counter ()
        col_counter = Counter ()
        for loc in locations:
            if loc.get ( 'coordinates' ) is not None:
                found_grid ( grid, loc, post_counter, row_counter, col_counter )

        display_counter ( post_counter, 'grid' )
        display_counter ( row_counter, 'row' )
        display_counter ( col_counter, 'column' )


def found_grid(grid, locations, counter, row_counter, col_counter):
    for g in grid:
        if not (not (g[ 'ymin' ] < locations[ 'coordinates' ][ 'coordinates' ][ 0 ] <= g[ "ymax" ])
                or not (g[ 'xmin' ] < locations[ 'coordinates' ][ 'coordinates' ][ 1 ] <= g[ 'xmax' ])):
            counter.update ( [ g[ 'id' ] ] )
            row_counter.update ( g[ 'id' ][ 0 ] )
            col_counter.update ( g[ 'id' ][ 1 ] )


def display_counter(counter, data_type):
    print ( '\nRank by {0}'.format ( data_type ) )
    for key, value in counter.most_common ():
        print ( '{0}: {1} posts'.format ( key, value ) )


if __name__ == '__main__':
    grid = load_grid ( melbgrid_json )
    parse_grid ( instagram_json )
