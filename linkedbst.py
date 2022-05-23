"""
File: linkedbst.py
Author: Ken Lambert
"""

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from linkedqueue import LinkedQueue
import math
import time
import random


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            line = ""
            if node != None:
                line += recurse(node.right, level + 1)
                line += "| " * level
                line += str(node.data) + "\n"
                line += recurse(node.left, level + 1)
            return line

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        result = []
        stack = []
        current = self._root
        while True:
            if current:
                stack.append(current)
                current = current.left
            elif(stack):
                current = stack.pop()
                result.append(current.data)
                current = current.right 
            else: 
                break
        return result

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None


    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""
        while self._root != None:
         
            if item > self._root.data:
                self._root = self._root.right

            elif item < self._root.data:
                self._root = self._root.left
            else:
                return True
        return False

    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, data) :
            node = BSTNode(data)
            if (self._root == None) :
                self._root = node
            else :
                find = self._root
                while (find != None) :
                    if (find.data >= data) :
                        if (find.left == None) :
                            find.left = node
                            return
                        else :
                            find = find.left
                        
                    else :
                        if (find.right == None) :
                            find.right = node
                            return
                        else :
                            find = find.right

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        def lift_max_in_left(top):
            parent = top
            current = top.left
            while not current.right == None:
                parent = current
                current = current.right
            top.data = current.data
            if parent == top:
                top.left = current.left
            else:
                parent.right = current.left

        if self.isEmpty(): return None

        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current = self._root
        while not current == None:
            if current.data == item:
                item_removed = current.data
                break
            parent = current
            if current.data > item:
                direction = 'L'
                current = current.left
            else:
                direction = 'R'
                current = current.right

        if item_removed == None: return None
        if not current.left == None \
                and not current.right == None:
            lift_max_in_left(current)
        else:

            if current.left == None:
                new_child = current.right
            else:
                new_child = current.left
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''

        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top.left is None and top.right is None:
                return 0
            left_sum = height1(top.left) if top.left is not None else -1
            right_sum = height1(top.right) if top.right is not None else -1
            return max(left_sum, right_sum) + 1
        return height1(self._root)

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        elements = self.inorder()
        lenght = len(list(elements))
        if 2 * math.log2(lenght + 1) - 1 > self.height():
            return True
        return False

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        elements = self.inorder()
        lst = []
        for elem in elements:
            if high>=elem >=low:
                lst.append(elem)
        return lst
    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        elements = self.inorder()
        def rb1(elements):
            if len(elements) == 0:
                return None

            i = len(elements)//2

            node = BSTNode(elements[i])
            node.left = rb1(elements[:i])
            node.right = rb1(elements[i+1:])
            return node
        self._root = rb1(list(elements))
    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        elements = self.inorder()
        for elem in elements:
            if elem > item:
                break
        if elem == item:
            return None
        return elem

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        elements = self.inorder()
        prev = None
        for elem in elements:
            if elem == item:
                return prev
            prev = elem
    def read_file(self, path):
        with open( path, 'r', encoding="UTF-8") as file:
            words_list = []
            for line in file:
                words_list.append(line[:-1])
        words_to_search = random.sample(words_list, 10000)
        return words_list, words_to_search
    def search_in_list(self, path):
        words_list, words_to_search = self.read_file(path)
        time_start = time.time()
        for word in words_to_search:
            word in words_list
        time_stop = time.time()
        result_time = time_stop - time_start
        return result_time

    def search_in_tree1(self, path):
        words_list, words_to_search = self.read_file(path)
        words_to_search.sort()
        for words in words_list:
            self.add(words)
        time_start = time.time()
        for word in words_to_search:
            self.find(word)
        time_stop = time.time()
        result_time = time_stop - time_start
        return result_time

    def search_in_tree2(self, path):
        words_list, words_to_search = self.read_file(path)
        for words in words_list:
            self.add(words)
        time_start = time.time()
        for word in words_to_search:
            self.find(word)
        time_stop = time.time()
        result_time = time_stop - time_start
        return result_time

    def search_in_tree3(self, path):
        words_list, words_to_search = self.read_file(path)
        for words in words_list:
            self.add(words)
        self.rebalance()
        time_start = time.time()
        for word in words_to_search:
            self.find(word)
        time_stop = time.time()
        result_time = time_stop - time_start
        return result_time

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        time_start = time.time()
        print("Test1 time:" + self.search_in_list(path))
        print("Test2 time:" + self.search_in_tree1(path))
        print("Test3 time:" + self.search_in_tree2(path))
        print("Test4 time:" + self.search_in_tree3(path))
        time_stop = time.time()
        print("Total time:"+time_stop - time_start)
