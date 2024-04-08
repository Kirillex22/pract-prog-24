class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.heigth = 0
        self.left = None
        self.right = None

    @staticmethod
    def update_heigth(node):
        node.heigth = max(Node.get_heigth(node.left), Node.get_heigth(node.right)) + 1

    @staticmethod
    def get_balance(node):
        return 0 if node == None else Node.get_heigth(node.right) - Node.get_heigth(node.left)


    @staticmethod 
    def swap(node1, node2):
        key = node1.key
        node1.key = node2.key
        node2.key = key

        value = node1.value
        node1.value = node2.value
        node2.value = value

        
            
    @staticmethod
    def right_rotate(node):
        Node.swap(node, node.left)
        buffer = node.right
        node.right = node.left
        node.left = node.right.left
        node.right.left = node.right.right
        node.right.right = buffer
        Node.update_heigth(node.right)
        Node.update_heigth(node)


    @staticmethod
    def left_rotate(node):
        Node.swap(node, node.right)
        buffer = node.left
        node.left = node.right
        node.right = node.left.right
        node.left.right = node.left.left
        node.left.left = buffer
        Node.update_heigth(node.left)
        Node.update_heigth(node)


    @staticmethod
    def balance(node):
        blc = Node.get_balance(node)

        if blc == -2:
            if Node.get_balance(node.left) == 1:
                Node.left_rotate(node.left)
            Node.right_rotate(node)

        elif blc == 2:
            if (Node.get_balance(node.right) == -1):
                Node.right_rotate(node.right)
            Node.left_rotate(node)


    @staticmethod
    def get_heigth(node):
        return -1 if node == None else node.heigth

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

        Node.update_heigth(node)
        Node.balance(node)

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

        if node != None:
            Node.update_heigth(node)
            Node.balance(node)

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
            