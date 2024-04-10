from red_black_tree import Node
from red_black_tree import Tree
import os

tree = Tree()
#tree.logging = False
tree.logging = True

tree.insert(10, 10)
tree.insert(9, 9)
tree.insert(5, 5)
tree.insert(11, 11)
tree.insert(4, 4)
tree.insert(3, 3)
tree.insert(1, 1)

#tree.logging = True

# tree_dict = tree.build_tree(tree.root)
# tree.print_tree(tree_dict)

# input()
# print('\n' + 'DELETE 1')
# tree.delete_node(1)

# tree_dict = tree.build_tree(tree.root)
# tree.print_tree(tree_dict)

# input()
# print('\n' + 'DELETE 10')
# tree.delete_node(10)

# tree_dict = tree.build_tree(tree.root)
# tree.print_tree(tree_dict)

stop = False
while(not stop):
    print('1 - вставка')
    print('2 - удаление')
    print('3 - вывод')
    print('4 - выход')

    key = input()

    if key == '1':
        print('введите ключ и значение')
        key = input()
        value = input()
        tree.insert(int(key), int(value))
        input()
        os.system('cls||clear')

    if key == '2':
        print('введите ключ')
        key = input()
        tree.delete_node(int(key))
        tree.print_tree(tree.build_tree(tree.root))
        input()
        os.system('cls||clear')

    if key == '3':
        tree.print_tree(tree.build_tree(tree.root))
        input()
        os.system('cls||clear')

    if key == '4':
        stop = True
    





    
