#!/usr/bin/env python

import sys
sys.path.append("./ijson")
import json
import ijson
from collections import Counter
# from mpi4py import MPI
# import time

# comm = MPI.COMM_WORLD
# rank = comm.Get_rank()
# size_mpi = comm.Get_size()
#
# global start_time
# start_time = time.time()


melbgrid_json = './melbGrid.json'
tiny_instagram_json = './tinyInstagram.json'

def load_grid(grid_filename):
    melbgrid = json.load(open(grid_filename))
    grid = list ()
    for g in melbgrid[ 'features' ]:
        grid.append ( g[ 'properties' ] )
    return grid

def parse_grid(json_filename):
    # input_file = open(tiny_instagram_json, 'rb')
    with open(json_filename, 'rb') as input_file:
        #load json iteratively
        # this needs to be more carefully
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

def display_counter(counter, data_type):
    print('\nRank by {0}'.format(data_type))
    for key, value in counter.most_common():
        print('{0}: {1} posts'.format(key, value))



if __name__ == '__main__':
    grid = load_grid(melbgrid_json)
    parse_grid(tiny_instagram_json)

