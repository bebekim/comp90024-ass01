import sys
sys.path.append("./ijson")
import json
import ijson
from collections import Counter

melbgrid_json = './melbGrid.json'
instagram_json = './tinyInstagram.json'


def load_grid(grid_filename):
    melbgrid = json.load(open(grid_filename))
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
    with open(json_filename, 'rb') as input_file:
        #load json iteratively
        # ijson.items should eliminate items without coordinate entries

        coordinates = ijson.items(input_file, 'rows.item.doc.coordinates.coordinates')
        post_counter = Counter()
        row_counter = Counter()
        col_counter = Counter()
        for coordinate in coordinates:
            if is_melbourne( grid, coordinate, post_counter, row_counter, col_counter ):
                pass
        display_counter(post_counter, 'grid')
        display_counter(row_counter, 'row')
        display_counter(col_counter, 'column')



def is_melbourne(grid, coordinates, counter, row_counter, col_counter):
    for g in grid:
        if not (not (g['ymin'] < coordinates[0] <= g["ymax"]) or not (g['xmin'] < coordinates[1] <= g['xmax'])):
            counter.update([g['id']])
            row_counter.update(g['id'][0])
            col_counter.update(g['id'][1])
            return True

# locations = ijson.items ( input_file, 'rows.item.doc.location' )
# posts_melbourne = (loc for loc in locations if loc[ 'location' ] is 'melbourne')

def display_counter(counter, data_type):
    print('\nRank by {0}'.format(data_type))
    for key, value in counter.most_common():
        print('{0}: {1} posts'.format(key, value))



input_file = open ( instagram_json, 'rb' )
coordinates = ijson.items ( input_file, 'rows.item.doc.coordinates.coordinates' )

rows = ijson.items( input_file , 'rows.item.doc' )
melbourne_rows = (r for r in rows if r['location'] == 'melbourne')
valid_row = 0
invalid_row = 0

for r in melbourne_rows:
    if r.get('coordinates') is not None:
        # print( r.keys() )
        valid_row += 1
    else:
        # r is a dictionary
        print ( r.keys() )
        invalid_row += 1

print(valid_row)
print(invalid_row)


# valid_coord = 0
# invalid_coord = 0
#
# post_counter = Counter()
# row_counter = Counter()
# column_counter = Counter()
#
# for coordinate in coordinates:
#     if coordinate is None:
#         invalid_coord += 1
#     else:
#         valid_coord += 1
#         print(coordinate)
#     # if coordinate is not None:
#     #     for g in grid:
#     #         if not (not (g['ymin'] < coordinate[0] <= g["ymax"]) or not (g['xmin'] < coordinate[1] <= g['xmax'])):
#     #             post_counter.update([g['id']])
#     #             row_counter.update(g['id'][0])
#     #             column_counter.update(g['id'][1])
#         # valid += 1
#     # else:
#         # invalid += 1
# # display_counter(post_counter, 'grid')
# # display_counter(row_counter, 'row')
# # display_counter(column_counter, 'column')
#
#
# print(valid_coord)
# print(invalid_coord)



if __name__ == '__main__':
    grid = load_grid(melbgrid_json)
    parse_grid(instagram_json)

