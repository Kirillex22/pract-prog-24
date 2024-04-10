from enum import Enum
from pprint import pprint 
     
class Color(Enum):
    RED = 'red'
    BLACK = 'black'


class Node:
    def __init__(self, key, value, color = Color.RED):
        self.color = color
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = None


    def __eq__(self, other):
        if isinstance(other, Node):
            return (
                (other.key == self.key) &
                (other.value == self.value) &
                (other.color == self.color)
            )
        return NotImplemented


    def print_myself(self):
        print(f'''
            color:{self.color}\n
            key:{self.key}\n
            value:{self.value}\n
            left_key: {self.left.key if self.left != None else 'None'}\n
            right_key: {self.right.key if self.right != None else 'None'}\n
        ''')
        

class Tree:
    def __init__(self):
       self.NIL = Node(None, None, color = Color.BLACK)
       self.root = self.NIL
       self.logging = False
    

    def node_exists(self, node):
        return node != self.NIL


    def swap(self, node1, node2):
        key = node1.key
        node1.key = node2.key
        node2.key = key

        value = node1.value
        node1.value = node2.value
        node2.value = value
        
            
    def right_rotate(self, node):
        self.swap(node, node.left)
        buffer = node.right
        node.right = node.left
        node.left = node.right.left
        node.right.left = node.right.right
        node.right.right = buffer


    def left_rotate(self, node):
        self.swap(node, node.right)
        buffer = node.left
        node.left = node.right
        node.right = node.left.right
        node.left.right = node.left.left
        node.left.left = buffer


    def balance(self, new_node):
        uncle = self.NIL

        while(new_node.parent.color == Color.RED):
            if new_node.parent == new_node.parent.parent.left:
                uncle = new_node.parent.parent.right

                if (uncle.color == Color.RED):
                    new_node.parent.color = Color.BLACK
                    uncle.color = Color.BLACK
                    new_node.parent.parent.color = Color.RED
                    new_node = new_node.parent.parent
                
                else:
                    if (new_node == new_node.parent.right):
                        new_node = new_node.parent
                        self.left_rotate(new_node)

                    new_node.parent.color = Color.BLACK
                    new_node.parent.color = Color.RED
                    self.right_rotate(new_node.parent.parent)

            else:
                uncle = new_node.parent.parent.left
                if (uncle.color == Color.RED):
                    new_node.parent.color = Color.BLACK
                    uncle.color = Color.BLACK
                    new_node.parent.parent.color = Color.RED
                    new_node = new_node.parent.parent
                
                else:
                    if (new_node == new_node.parent.left):
                        new_node = new_node.parent
                        self.right_rotate(new_node)

                    new_node.parent.color = Color.BLACK
                    new_node.parent.parent.color =Color.RED
                    self.left_rotate(new_node.parent.parent)

        self.root.color = Color.BLACK
    

    def makeup_node(self, node):
        node.left = self.NIL
        node.right = self.NIL
        node.parent = self.NIL

        return node

    def insert(self, key, value):
        current_node = self.root
        parent = self.NIL

        while(self.node_exists(current_node)):
            parent = current_node
            if (value < current_node.value):
                current_node = current_node.left
            else:
                current_node = current_node.right
        
        new_node = Node(key, value)
        new_node = self.makeup_node(new_node)
        new_node.parent = parent

        if not self.node_exists(parent):
            self.root = new_node
        elif value < parent.value:
            parent.left = new_node
        else:
            parent.right = new_node

        self.balance(new_node)

        if self.logging:
            new_node.print_myself()
    

    def get_max_node(self, node):
        if node == self.NIL:
            return None
        if node.right == self.NIL:
            if node.left == self.NIL:
                return node
            return node.left
        return self.get_max_node(node.right)

    
    def get_min_node(self, node):
        if node == self.NIL:
            return None
        if node.left == self.NIL:
            if node.right == self.NIL:
                return node
            return node.right
        return self.get_min_node(node.left)


    def search_node(self, node, key):
        if node == None:
            return None
        elif node.key == key:
            return node
        else:
            return self.search_node(node.left, key) if key < node.key else self.search_node(node.right, key)


    def get_children_count(self, node):
        count = 0
        if (self.node_exists(node.left)):
            count += 1
        if(self.node_exists(node.right)):
            count += 1

        return count


    def get_children(self, node):
        return node.left if self.node_exists(node.left) else node.right 


    def transplant_node(self, destination, start):
        if destination == self.root:
            self.root = start  
        elif destination == destination.parent.left:
            destination.parent.left = start    
        else:
            destination.parent.right = start
        
        start.parent = destination.parent


    def fix_rules(self, node):
        while(node != self.root and node.color == Color.BLACK):
            brother = None
            if node == node.parent.left:
                brother = node.parent.left
                if brother.color == Color.RED:
                    brother.color = Color.BLACK
                    node.parent.color = Color.RED
                    self.left_rotate(node.parent)
                    brother = node.parent.right
                
                if (brother.left.color == Color.BLACK and brother.right.color == Color.BLACK):
                    brother.color = Color.RED
                    node = node.parent
                else:
                    if brother.right.color == Color.BLACK:
                        brother.left.color = Color.BLACK
                        brother.color = Color.RED
                        self.right_rotate(brother)
                        brother = node.parent.right

                    brother.color = node.parent.color
                    node.parent.color = Color.BLACK
                    brother.right.color = Color.BLACK
                    self.left_rotate(node.parent)
                    node = tree.root
            else:
                brother = node.parent.left
                if brother.color == Color.RED:
                    brother.color = Color.BLACK
                    node.parent.color = Color.RED
                    self.right_rotate(node.parent)
                    brother = node.parent.left
                if (brother.left.color == Color.BLACK and brother.right.color == Color.BLACK):
                    self.right_rotate(node.parent)
                    brother = node.parent.left
                else:
                    if brother.left.color == Color.BLACK:
                        brother.right.color = Color.BLACK
                        brother.color = Color.RED
                        self.left_rotate(brother)
                        brother = node.parent.left

                    brother.color = node.parent.color
                    node.parent.color = Color.BLACK
                    brother.left.color = Color.BLACK
                    self.right_rotate(node.parent)
                    node = self.root

        node.color = Color.BLACK


    def delete_node(self, key):
        node_to_delete = self.search_node(self.root, key)
        deleted_color = node_to_delete.color
        child = self.NIL
        if self.get_children_count(node_to_delete) < 2:
            child = self.get_children(node_to_delete)
            self.transplant_node(node_to_delete, child)
        else:
            min_node = self.get_min_node(node_to_delete.right)
            node_to_delete.key = min_node.key
            node_to_delete.value = min_node.value
            deleted_color = min_node.color
            child = self.get_children(min_node)
            self.transplant_node(min_node, child)
        
        if deleted_color == Color.BLACK:
            self.fix_rules(child)


    # def print_tree(self, node, step=0, sep = ' '):
    #     if not self.node_exists(node):
    #         return None
    #     step += 5
    #     self.print_tree(node.right, step)
    #     print(sep*step + str(node.key))
    #     self.print_tree(node.left, step)


    def build_tree(self, node):
        if node == self.NIL:
            return 'NIL'
        tree = {
            'node_key' : node.key,
            'left_child' :  self.build_tree(node.left),
            'right_child' : self.build_tree(node.right)
        }
        return tree

    def print_tree(self, tree):
        pprint(tree)


