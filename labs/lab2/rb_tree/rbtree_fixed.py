from pydot import *
from graphviz import *
from enum import Enum


class Color(Enum):
    RED = 'red'
    BLACK = 'black'

class Node():
    def __init__(self, key):
        self.key = key
        self.parent = None
        self.left = None
        self.right = None
        self.color = Color.BLACK

    def __eq__(self, other):
        if isinstance(other, Node):
            return (
                (other.key == self.key) &
                (other.color == self.color)
            )
        return NotImplemented

class Tree():
    def __init__(self):
        self.NIL = Node("NIL")
        self.root = self.NIL
        

    def left_rotate(self, node): 
        buffer = node.right
        node.right = buffer.left
        if buffer.left != self.NIL:
            buffer.left.parent = node

        buffer.parent = node.parent
        if node.parent == None:
            self.root = buffer
        elif node == node.parent.left:
            node.parent.left = buffer
        else:
            node.parent.right = buffer
        buffer.left = node
        node.parent = buffer
        
    def right_rotate(self, node):
        buffer = node.left
        node.left = buffer.right
        if buffer.right != self.NIL:
            buffer.right.parent = node
        buffer.parent = node.parent
        if node.parent == None:
            self.root = buffer
        elif node == node.parent.right:
            node.parent.right = buffer
        else:
            node.parent.left = buffer
        buffer.right = node
        node.parent = buffer
        
    
    def search_node(self, node, key):
        if node == None or node == self.NIL:
            return None
        elif node.key == key:
            return node
        else:
            return self.search_node(node.left, key) if key < node.key else self.search_node(node.right, key)


    def __rb_transplant(self, u, v):
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent


    def insert(self, key):
        if self.search_node(self.root, key) is not None:
            raise Exception(f'Value {key} not exists in tree')

        node = Node(key)
        node.parent = None
        node.key = key
        node.left = self.NIL
        node.right = self.NIL
        node.color = Color.RED

        parent = None
        current_node = self.root

        while current_node != self.NIL:
            parent = current_node
            if node.key < current_node.key:
                current_node = current_node.left
            else:
                current_node = current_node.right

        node.parent = parent

        if parent == None:
            self.root = node
        elif node.key < parent.key:
            parent.left = node
        else:
            parent.right = node
            
        if node.parent == None:
            node.color = Color.BLACK
            return

        if node.parent.parent == None:
            return

        self.fix_insert(node)

    def fix_insert(self, node):
        while node.parent.color == Color.RED:
            if node.parent == node.parent.parent.right:
                u = node.parent.parent.left
                if u.color == Color.RED:
                    u.color = Color.BLACK
                    node.parent.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self.right_rotate(node)
                    node.parent.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    self.left_rotate(node.parent.parent)
            else:
                u = node.parent.parent.right

                if u.color == Color.RED:
                    u.color = Color.BLACK
                    node.parent.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self.left_rotate(node)
                    node.parent.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    self.right_rotate(node.parent.parent)
            if node == self.root:
                break
        self.root.color = Color.BLACK

        
    def delete_node(self, node, key):
        if self.search_node(self.root, key) is None:
            raise Exception(f'Value {key} not exists in tree')

        z = self.NIL
        while node != self.NIL:
            if node.key == key:
                z = node

            if node.key <= key:
                node = node.right
            else:
                node = node.left
        y = z
        y_original_color = y.color
        if z.left == self.NIL:
            x = z.right
            self.__rb_transplant(z, z.right)
        elif (z.right == self.NIL):
            x = z.left
            self.__rb_transplant(z, z.left)
        else:
            y = z.left
            while y.right != self.NIL:
                y = y.right
            y_original_color = y.color
            x = y.left
            if y.parent == z:
                x.parent = y
            else:
                self.__rb_transplant(y, y.left)
                y.left = z.left
                y.left.parent = y

            self.__rb_transplant(z, y)
            y.right = z.right
            y.right.parent = y
            y.color = z.color
        if y_original_color == Color.BLACK:
            self.delete_fix(x)
            
    def delete_fix(self, x):
        while x != self.root and x.color == Color.BLACK:
            if x == x.parent.left:
                s = x.parent.right
                if s.color == Color.RED:
                    s.color = Color.BLACK
                    x.parent.color = Color.RED
                    self.left_rotate(x.parent)
                    s = x.parent.right

                if s.left.color == Color.BLACK and s.right.color == Color.BLACK:
                    s.color = Color.RED
                    x = x.parent
                else:
                    if s.right.color == Color.BLACK:
                        s.left.color = Color.BLACK
                        s.color = Color.RED
                        self.right_rotate(s)
                        s = x.parent.right

                    s.color = x.parent.color
                    x.parent.color = Color.BLACK
                    s.right.color = Color.BLACK
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == Color.RED:
                    s.color = Color.BLACK
                    x.parent.color = Color.RED
                    self.right_rotate(x.parent)
                    s = x.parent.left

                if s.right.color == Color.BLACK and s.right.color == Color.BLACK:
                    s.color = Color.RED
                    x = x.parent
                else:
                    if s.left.color == Color.BLACK:
                        s.right.color = Color.BLACK
                        s.color = Color.RED
                        self.left_rotate(s)
                        s = x.parent.left

                    s.color = x.parent.color
                    x.parent.color = Color.BLACK
                    s.left.color = Color.BLACK
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = Color.BLACK

    
    def visualize_binary_tree_dot(self, node, dot):
            dot.node(str(node.key), str(node.key), style='filled', fillcolor=node.color.value)
            if node.left is not None:
                if node.left.key != "NIL":
                    dot.edge(str(node.key), str(node.left.key))
                    self.visualize_binary_tree_dot(node.left, dot)
            if node.right is not None:
                if node.right.key != "NIL":
                    dot.edge(str(node.key), str(node.right.key))
                    self.visualize_binary_tree_dot(node.right, dot)
