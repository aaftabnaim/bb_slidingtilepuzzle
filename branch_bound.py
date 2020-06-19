import numpy as np
import sys
import copy

def reached_goal(a, b):
    return np.array_equal(a, b)

def arr_in_list(myarr, list_arrays):
    return next((True for elem in list_arrays if np.array_equal(elem, myarr)), False)



class Matrix(np.ndarray):

    def __new__(cls, input_array, depth="None"):
        obj = np.asarray(input_array).view(cls)
        return obj


class Node:

    def __init__(self,matrix,tDistance=0,path=[]):
        self.matrix = matrix
        self.tDistance = tDistance
        self.path = path.copy()
        self.children = []

    def extend(self):
        self.path.append(self.matrix)
        path_copy = self.path
        for next_move in moves:
            temp_matrix = self.matrix.copy()
            space_cor = [(x,y) for (y,x),val in np.ndenumerate(self.matrix) if val == ''][0]

            
            if next_move[0]=='x':
                
                if 0 <= space_cor[0]+next_move[1] < 3:
                    
                    temp_matrix[space_cor[1]][space_cor[0]],temp_matrix[space_cor[1]][space_cor[0]+next_move[1]]=\
                    temp_matrix[space_cor[1]][space_cor[0]+next_move[1]],temp_matrix[space_cor[1]][space_cor[0]]
                    all_matrices_in_path = [matrix for matrix in self.path ]
                    if not(arr_in_list(temp_matrix,all_matrices_in_path)) and not(arr_in_list(temp_matrix,extended_list)):

                        child_node = Node(temp_matrix,self.tDistance+1,path_copy)
                        self.children.append(child_node)
                        active_nodes.append(child_node)
                        #print('\nMade \n',child_node.matrix,' from \n',self.matrix,'\n\n')
                        #print(child_node.matrix)


            if next_move[0]=='y':
                if 0 <= space_cor[1]+next_move[1] < 3:
                    
                    temp_matrix[space_cor[1]][space_cor[0]],temp_matrix[space_cor[1]+next_move[1]][space_cor[0]]=\
                    temp_matrix[space_cor[1]+next_move[1]][space_cor[0]],temp_matrix[space_cor[1]][space_cor[0]]
                    all_matrices_in_path = [matrix for matrix in self.path ]
                    if not(arr_in_list(temp_matrix,self.path)) and not(arr_in_list(temp_matrix,extended_list)):

                        child_node = Node(temp_matrix,self.tDistance+1,path_copy)
                        self.children.append(child_node)
                        active_nodes.append(child_node)
                        #print('Made \n',child_node.matrix,' from \n',self.matrix,'\n\n')
                        #print(child_node.matrix)



count = 0

def solve(current,goal_):
    global count
    # if you have reached the goal move to safe mode
    if reached_goal(current.matrix,goal_.matrix) or count >= sys.getrecursionlimit():
        print('C matrix \n\n', current.matrix, '\nlength', current.tDistance)
        print('Has Path ')
        
        for matrix in current.path:
            print(matrix,'\n')

        print('Debug : Length of Solution ', len(current.path))        
        print('\nActive Nodes : ',len(active_nodes),'\n\n')
        print('Exit status :',end='')
        print('Reached goal') if reached_goal(current.matrix,goal_.matrix) else print('Max recursion limit reached')
        print('No of Extensions ', len(extended_list))
        #print(current.path[-1].matrix)
        
        
    # if no goal is found yet keep extending
    else:
        s_track = {}
        for index, node in enumerate(active_nodes):
            s_track[index] = node.tDistance

        min_distance = min(list(s_track.values()))
        for key,val in s_track.items():
            if min_distance == val:
                next_extension = key
        #print(active_nodes[next_extension].matrix,'\n\nGot Extended')
        active_nodes[next_extension].extend()

        try:
            x = active_nodes.pop(next_extension)
            extended_list.append(x)
        except:
            print('101')
        #print('Removed ', x.matrix,'\n\n')
        s_track = {}
        for index, nodes in enumerate(active_nodes):
            s_track[index] = node.tDistance

        min_distance = min(list(s_track.values()))
        for key,val in s_track.items():
            if min_distance == val:
                next_extension = key
        count += 1
        try:
            solve(active_nodes[next_extension],goal_)
        except IndexError:
            print('AN ',active_nodes)
            print(current.matrix)
            print(len(active_nodes),'/',next_extension)


moves = [('x',-1),('x',+1),('y',-1),('y',+1)]    

goal = Node(Matrix([1, 2, 3, 5, 8, 6, '', 7, 4]).reshape([3, 3]))

start = Node(Matrix([1, 2, 3, 5, 6, '', 7, 8, 4]).reshape([3, 3]))

active_nodes = [start]
extended_list = []
solve(start,goal)

#print(x.children)

