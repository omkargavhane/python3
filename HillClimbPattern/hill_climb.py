#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  hill_climb.py
#  
#  Copyright 2020 omkar gavhane <omkar.g.1998@gmail.com>
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
#####################################
#HILL CLIMBING PATTERN
#####################################


class coordinate:
    def __init__(self,x,y,char):
        self.x=x
        self.y=y
        self.char=char

class hill_climb:
    def __init__(self,inpt):
        self.inpt=inpt
        self.copy_inpt=[]
        self.coordinates={}
        self.x_cnt=1
        self.y_cnt=1
        self.edge={1:'/',0:'\\'}
        self.pattern=""
    
    def setter(self,inpt):
        self.inpt=inpt
        self.copy_inpt=[]
        self.coordinates={}
        self.x_cnt=1
        self.y_cnt=1
        self.edge={1:'/',0:'\\'}
        self.pattern=""

    def __find_coordinates(self):
        '''
        Find the coordinates for each forward and backward slash and store it in format of (x,y,1|0)
        where 1->forward slash 0->backward slash in coordinates dictionary where key is the line number
        '''
        self.setter(self.inpt)
        for i in range(len(self.inpt)):
            for j in range(1,self.inpt[i]+1):
                if i%2==0:
                    if j==1:
                        if self.y_cnt not in self.coordinates:self.coordinates[self.y_cnt]=[]
                        self.coordinates[self.y_cnt].append(coordinate(self.x_cnt,self.y_cnt,1))
                    else:
                        self.y_cnt+=1
                        if self.y_cnt not in self.coordinates:self.coordinates[self.y_cnt]=[]
                        self.coordinates[self.y_cnt].append(coordinate(self.x_cnt,self.y_cnt,1))
                else:
                    if j==1:
                        if self.y_cnt not in self.coordinates:self.coordinates[self.y_cnt]=[]
                        self.coordinates[self.y_cnt].append(coordinate(self.x_cnt,self.y_cnt,0))
                    else:
                        self.y_cnt-=1
                        if self.y_cnt not in self.coordinates:self.coordinates[self.y_cnt]=[]
                        self.coordinates[self.y_cnt].append(coordinate(self.x_cnt,self.y_cnt,0))
                self.x_cnt+=1
        self.__shift_on_x()

    def __shift_on_x(self):
        "Shifts the coordinates on x by 1 after persons position"
        for e in self.coordinates[max(self.coordinates)][::-1]:
            if e.char==1:
                person_stand=e.x
        new_coordinates={}
        for k,v in self.coordinates.items():
            new_coordinates[k]=[]
            for e in self.coordinates[k]:
                if e.x>person_stand:
                    new_coordinates[k].append(coordinate(e.x+1,e.y,e.char))
                else:
                    new_coordinates[k].append((e))
        self.coordinates=new_coordinates
        self.__filter_negative_y()

    def __filter_negative_y(self):
        "Function pushes the pattern to positive y axis if any y is negative or 0"
        min_coord=min(self.coordinates)
        if min_coord < 1:
            new_coordinates={}
            for k,v in self.coordinates.items():
                new_coordinates[k+abs(min_coord)+1]=v
            self.coordinates=new_coordinates
        self.copy_inpt=self.inpt


    def print_pattern(self):
        "print actual pattern"
        if self.copy_inpt!=self.inpt:
            self.__find_coordinates()
            max_coord=max(self.coordinates)
            self.pattern+=' '+' '*(self.coordinates[max_coord][0].x-1)+'o\n'
            self.pattern+=' '+' '*(self.coordinates[max_coord][0].x-2)+'/|\\\n'
            self.pattern+=' '+' '*(self.coordinates[max_coord][0].x-2)+'< >\n'
            for line in range(max_coord,0,-1):
                linedata=self.coordinates[line]
                self.pattern+=' '*( linedata[0].x-1 ) +self.edge[linedata[0].char]
                for i in range(1,len(linedata)):
                    self.pattern+=' '*( linedata[i].x-linedata[i-1].x-1 )+self.edge[linedata[i].char]
                self.pattern+="\n"
        return self.pattern


if __name__=="__main__":
    obj=hill_climb([int(e) for e in input('Enter input string:\n').split()])
    print(obj.print_pattern(),end="")
