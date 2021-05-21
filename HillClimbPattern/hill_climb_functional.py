#####################################
#HILL CLIMBING PATTERN
#####################################

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  hill_climb_functional.py
#
#  Copyright 2021 omkar gavhane <omkar.g.1998@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

import pprint  

coordinates={}
x_cnt=1
y_cnt=1

def find_coordinates():
    '''
    Find the coordinates for each forward and backward slash and store it in format of (x,y,1|0)
    where 1->forward slash 0->backward slash in coordinates dictionary where key is the line number
    '''
    global coordinates
    global x_cnt
    global y_cnt
    for i in range(len(inpt)):
        for j in range(1,inpt[i]+1):
            if i%2==0:
                if j==1:
                    if y_cnt not in coordinates:coordinates[y_cnt]=[]
                    coordinates[y_cnt].append((x_cnt,y_cnt,1))
                else:
                    y_cnt+=1
                    if y_cnt not in coordinates:coordinates[y_cnt]=[]
                    coordinates[y_cnt].append((x_cnt,y_cnt,1))
            else:
                if j==1:
                    if y_cnt not in coordinates:coordinates[y_cnt]=[]
                    coordinates[y_cnt].append((x_cnt,y_cnt,0))
                else:
                    y_cnt-=1
                    if y_cnt not in coordinates:coordinates[y_cnt]=[]
                    coordinates[y_cnt].append((x_cnt,y_cnt,0))
            x_cnt+=1

def shift_on_x():
    "Shifts the coordinates on x by 1 after persons position"
    global coordinates
    for e in coordinates[max(coordinates)][::-1]:
        if e[2]==1:
            person_stand=e[0]
    new_coordinates={}
    for k,v in coordinates.items():
        new_coordinates[k]=[]
        for e in coordinates[k]:
            if e[0]>person_stand:
                new_coordinates[k].append((e[0]+1,e[1],e[2]))
            else:
                new_coordinates[k].append((e))
    coordinates=new_coordinates


def filter_negative_y():
    "Function pushes the pattern to positive y axis if any y is negative or 0"
    global coordinates
    min_coord=min(coordinates)
    if min_coord < 1:
        new_coordinates={}
        for k,v in coordinates.items():
            new_coordinates[k+abs(min_coord)+1]=v
        coordinates=new_coordinates



def print_pattern():
    "prints actual pattern"
    global coordinates
    max_coord=max(coordinates)
    print(' '+' '*(coordinates[max_coord][0][0]-1)+'o')
    print(' '+' '*(coordinates[max_coord][0][0]-2)+'/|\\')
    print(' '+' '*(coordinates[max_coord][0][0]-2)+'< >')
    edge={1:'/',0:'\\'}
    for line in range(max_coord,0,-1):
        linedata=coordinates[line]
        print(' '*( linedata[0][0]-1 ) +edge[linedata[0][2]],end='')
        for i in range(1,len(linedata)):
            print(' '*( linedata[i][0]-linedata[i-1][0]-1 )+edge[linedata[i][2]],end='')
        print()

if __name__=="__main__":
    global inpt
    inpt=[int(e) for e in input('Enter input string:\n').split()]
    find_coordinates()
    #pprint.pprint(coordinates)
    shift_on_x()
    #pprint.pprint(coordinates)
    filter_negative_y()
    #pprint.pprint(coordinates)
    print_pattern()
