class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None


    @staticmethod
    def insert(node, key, value):
        if key < node.key:
            if node.left == None:
                node.left = Node(key, value)
            else:
                Node.insert(node.left, key, value)
        else:
            if node.right == None:
                node.right = Node(key, value)
            else:
                Node.insert(node.right, key, value)

    @staticmethod
    def get_max_node(node):
        if node == None:
            return None
        if node.right == None:
            if node.left == None:
                return node
            return node.left
        return Node.get_max_node(node.right)

    
    @staticmethod
    def get_min_node(node):
        if node == None:
            return None
        if node.left == None:
            if node.right == None:
                return node
            return node.right
        return Node.get_min_node(node.left)


    @staticmethod
    def search_node(node, key):
        if node == None:
            return None
        elif node.key == key:
            return node
        else:
            return Node.search_node(node.left, key) if key < node.key else Node.search_node(node.right, key)


    @staticmethod
    def delete_node(node, key):
        if node == None:
            return None
        elif key < node.key:
            node.left = Node.delete_node(node.left, key)
        elif key > node.key:
            node.right = Node.delete_node(node.right, key)
        else:
            if (node.left == None) or (node.right == None):
                node = node.left if node.right == None else node.right
            else:
                left_max_node = Node.get_max_node(node.left) 
                node.key = left_max_node.key
                node.value = left_max_node.value
                node.left = Node.delete_node(node.left, left_max_node.key)

        return node


    @staticmethod
    def in_walk_print(node):
        if node == None:
            return None
        Node.printTree(node.left)
        print(node.key) 
        Node.printTree(node.right)

    @staticmethod
    def print_tree(node, step=0, sep = ' '):
        if node is None:
            return None
        step += 5
        Node.print_tree(node.right, step)
        print(sep*step + str(node.key))
        Node.print_tree(node.left, step)
            