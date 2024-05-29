from pydot import *
from graphviz import *
import math
from enum import Enum

class Color(Enum):
    Black = 'black'
    Red = 'red'

class Position:
	def __init__(self, x: int, y: int) -> None:
		self.x = x
		self.y = y

	def __radd__(self, obj):
		if isinstance(obj, Position):
			return Position(self.x + obj.x, self.y + obj.y)
		elif isinstance(obj, tuple):
			return Position(self.x + obj[0], self.y + obj[1])
		raise TypeError(f'unsupported operand type(s) for +: Position and {type(obj)}')
		
	def __repr__(self) -> str:
		return f'<Position{self.value}>'

	@property
	def value(self) -> tuple:
		return (self.x, self.y)

class Node:
    def __init__(self, father=None) -> None:
        self.color = Color.Black
        self.father: Node | None = father
        self.left: Node | None = None
        self._position: Position | None = None
        self.right: Node | None = None
        self._value: int | None = None

    def __bool__(self) -> bool:
        return bool(self.value) or self.value == 0

    def __eq__(self, obj) -> bool:
        if isinstance(obj, Node):
            return self.value == obj.value if self or obj else self is obj
        elif isinstance(obj, int):
            return self.value == obj
        return False

    def __gt__(self, obj) -> bool:
        if not isinstance(obj, (Node, int)):
            raise ValueError('Object {} not in [Node, int] type'.format(obj))
        return self.value > obj.value if isinstance(obj, Node) else self.value > obj

    def __hash__(self) -> int:
        return object.__hash__(self)

    def __lt__(self, obj) -> bool:
        if not isinstance(obj, (Node, int)):
            raise ValueError('Object {} not in [Node, int] type'.format(obj))
        return self.value < obj.value if isinstance(obj, Node) else self.value < obj

    def __repr__(self) -> str:
        if self:
            return f'<{self.color.name}.Node: {self.value}>'
        elif self.father:
            side = 'Left' if self.is_left else 'Right'
            return f'<{side}.List(father={self.father.value})>'
        return '<Empty root>'

    def __str__(self) -> str:
        return str(self.value) if self else 'n'

    def child(self, value: int):
        return self.left if value < self else self.right

    @property
    def brother(self):
        if not self.father:
            return None
        return self.father.right if self.is_left else self.father.left

    @property
    def children_count(self) -> int:
        return bool(self.right) + bool(self.left)

    @property
    def grandpa(self):
        return self.father.father if self.father else None

    @property
    def is_black(self) -> bool:
        return self.color == Color.Black

    @property
    def is_left(self) -> bool:
        return bool(self.father) and self is self.father.left

    @property
    def is_red(self) -> bool:
        return self.color == Color.Red

    @property
    def position(self) -> Position:
        if not self.father:
            return self._position
        left = (-1)**self.is_left
        pos = self.father.position.value
        return pos + Position(left * 2**(pos[1] - 1), -1)
    
    def set_position(self, count: int):
        height = int(2 * math.log2(count + 1))
        self._position = Position(2**height - 1, height)

    @property
    def uncle(self):
        return self.father.brother if self.father else None

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, value: int) -> None:
        self._value = value if isinstance(value, int) else None
        if self:
            self.left = self.left if self.left != None else Node(father=self)
            self.right = self.right if self.right != None else Node(
                father=self)
        else:
            self.color = Color.Black
            self.left = None
            self.right = None

class RedBlackTree:
    def __init__(self):
        self.root: Node = Node()
        self.nodes: dict[int, Node] = {hash(self.root): self.root}

    def __balance(self, node):
        if node.grandpa and node.father.is_red:
            if node.uncle.is_red:
                node.father.color = Color.Black
                node.uncle.color = Color.Black
                node.grandpa.color = Color.Red
                self.__balance(node.grandpa)
            elif node.father < node.grandpa:
                self.__LLturn(node)
            elif node.father > node.grandpa:
                self.__RRturn(node)
        self.root.color = Color.Black
        self.root.set_position(len(self.nodes))

    def __black_list_case(self, node):
        brother = node.brother
        if not brother:
            return
        if brother.is_black:
            if brother.left.is_black and brother.right.is_black:
                brother.color = Color.Red
                if brother.father.is_red:
                    brother.father.color = Color.Black
                else:
                    self.__black_list_case(node.father)
            elif brother.is_left:
                if brother.right.is_red:
                    self.__RRturn(brother.right.right)
                brother.left.color = Color.Black
                self.__LLturn(brother.left)
            else:
                if brother.left.is_red:
                    self.__LLturn(brother.left.left)
                brother.right.color = Color.Black
                self.__RRturn(brother.right)
        else:
            if brother.is_left:
                self.__LLturn(brother.left)
            else:
                self.__RRturn(brother.right)
            self.__black_list_case(node)

    def __LLturn(self, node):
        if node and node > node.father:
            self.__RRturn(node.right)
        father = node.father
        grandpa = node.grandpa
        uncle = node.uncle
        father_right = father.right
        father.value, grandpa.value = grandpa.value, father.value
        grandpa.right = grandpa.left
        grandpa.left = node
        father.right = uncle
        father.left = father_right
        uncle.father = father
        node.father = grandpa

    def __RRturn(self, node):
        if node and node < node.father:
            self.__LLturn(node.left)
        father = node.father
        grandpa = node.grandpa
        uncle = node.uncle
        father_left = father.left
        father.value, grandpa.value = grandpa.value, father.value
        grandpa.left = grandpa.right
        grandpa.right = node
        father.left = uncle
        father.right = father_left
        uncle.father = father
        node.father = grandpa

    def insert(self, value):
        node = self.search(value)
        if node: 
            raise ValueError(f'Value {value} already exists in the tree')
        node.value = value
        node.color = Color.Red
        self.nodes[hash(node.right)] = node.right
        self.nodes[hash(node.left)] = node.left
        self.__balance(node)

    def delete(self, obj):
        node = obj if isinstance(obj, Node) else self.search(obj)
        if not node:
            raise ValueError(f'Value {obj} not exists in tree')
        elif node.children_count == 0:
            if node.is_black:
                self.__black_list_case(node)
            self.nodes.pop(hash(node.left))
            self.nodes.pop(hash(node.right))
            node.value = None
        elif node.children_count == 1:
            node_child = node.left or node.right
            node.value, node_child.value = node_child.value, node.value
            self.delete(node_child)
        elif node.children_count == 2:
            max_right_child = node.left
            while max_right_child.right:
                max_right_child = max_right_child.right
            node.value = max_right_child.value
            self.delete(max_right_child)
        self.root.set_position(len(self.nodes))

    def search(self, value):
        node = self.root
        while node and node != value:
            node = node.child(value)
        return node

    # Визуализация    
    def visualize_binary_tree_dot(self, node, dot):
        if node is not None:
            dot.node(str(node.value), str(node.value), style='filled', fillcolor=node.color.name)
            if node.left is not None:
                if node.left.value is not None:
                    dot.edge(str(node.value), str(node.left.value))
                    self.visualize_binary_tree_dot(node.left, dot)
            if node.right is not None:
                if node.right.value is not None:
                    dot.edge(str(node.value), str(node.right.value))
                    self.visualize_binary_tree_dot(node.right, dot)