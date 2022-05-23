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
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

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
         
            # pass right subtree as new tree
            if item > self._root.data:
                self._root = self._root.right
    
            # pass left subtree as new tree
            elif item < self._root.data:
                self._root = self._root.left
            else:
                return True # if the key is found return 1
        return False

        # def recurse(node):
        #     if node is None:
        #         return None
        #     elif item == node.data:
        #         return node.data
        #     elif item < node.data:
        #         return recurse(node.left)
        #     else:
        #         return recurse(node.right)

        # return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, data) :
            #  Create a new node
            node = BSTNode(data)
            if (self._root == None) :
                #  When adds a first node in bst
                self._root = node
            else :
                find = self._root
                #  Add new node to proper position
                while (find != None) :
                    if (find.data >= data) :
                        if (find.left == None) :
                            #  When left child empty
                            #  So add new node here
                            find.left = node
                            return
                        else :
                            #  Otherwise
                            #  Visit left sub-tree
                            find = find.left
                        
                    else :
                        if (find.right == None) :
                            #  When right child empty
                            #  So add new node here
                            find.right = node
                            return
                        else :
                            #  Visit right sub-tree
                            find = find.right

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_max_in_left(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
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

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
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

        # Return None if the item is absent
        if item_removed == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current.left == None \
                and not current.right == None:
            lift_max_in_left(current)
        else:

            # Case 2: The node has no left child
            if current.left == None:
                new_child = current.right

                # Case 3: The node has no right child
            else:
                new_child = current.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
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
        self.is_balanced()
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
        print(self.search_in_list(path))
        # print(self.search_in_tree1(path))
        # print(self.search_in_tree2(path))
        # print(self.search_in_tree3(path))
tree = LinkedBST()
tree.demo_bst("words.txt")
# for letter in "hello":
#     tree.add(letter)
# print(tree)