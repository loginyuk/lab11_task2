"""
File: linkedbst.py
Author: Ken Lambert
"""
import random
import time
from math import log, ceil
from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
# from linkedqueue import LinkedQueue


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
            string = ""
            if node != None:
                string += recurse(node.right, level + 1)
                string += "| " * level
                string += str(node.data) + "\n"
                string += recurse(node.left, level + 1)
            return string

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

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    def find2(self, item):
        """By while loop"""
        current = self._root
        while current is not None:
            if item == current.data:
                return current.data
            elif item < current.data:
                current = current.left
            else:
                current = current.right
        return None
    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left == None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right == None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1
    
    def add2(self, item):
        """
        By while loop
        """
        if self.isEmpty():
            self._root = BSTNode(item)
            self._size += 1
            return
        current = self._root
        while True:
            if item < current.data:
                if current.left is None:
                    current.left = BSTNode(item)
                    self._size += 1
                    return
                else:
                    current = current.left
            else:
                if current.right is None:
                    current.right = BSTNode(item)
                    self._size += 1
                    return
                else:
                    current = current.right

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_max_in_left_subtree_to_top(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while not current_node.right == None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while not current_node == None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current_node.left == None \
                and not current_node.right == None:
            lift_max_in_left_subtree_to_top(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left == None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

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
        if self.isEmpty():
            return 0
        else:
            return self._height(self._root)

    def _height(self, node):
        '''
        Helper function for height
        :param node:
        :return:
        '''
        if self.leaf(node):
            return 0
        return 1 + max(self._height(child) for child in self.child(node))

    def leaf(self, node):
        """
        Check if node is leaf
        """
        if node is None:
            return False
        if node.left is None and node.right is None:
            return True
        return False

    def child(self, node):
        """
        Returns list of children of node
        """
        children = []
        if node.left is not None:
            children.append(node.left)
        if node.right is not None:
            children.append(node.right)
        return children


    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        height_tree = self.height()
        num_nodes = self._size
        return height_tree < 2 * log(num_nodes + 1, 2) - 1

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        inorder = list(self.inorder())
        return [item for item in inorder if low <= item <= high]

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        if self.is_balanced():
            return
        inorder = list(self.inorder())
        self.clear()
        self._root = self._rebalance(inorder, 0, len(inorder) - 1)
        self._size = len(inorder)



    def _rebalance(self, inorder, low, high):
        '''
        Helper function for rebalance
        :param inorder:
        :param low:
        :param high:
        :return:
        '''
        if low > high:
            return None
        else:
            mid = ceil((low + high) / 2)
            node = BSTNode(inorder[mid])
            node.left = self._rebalance(inorder, low, mid - 1)

            node.right = self._rebalance(inorder, mid + 1, high)
            return node


    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        inorder = list(self.inorder())
        while inorder:
            element = inorder.pop(0)
            if element > item:
                return element
        return None


    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        inorder = list(self.inorder())
        while inorder:
            element = inorder.pop()
            if element < item:
                return element
        return None

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        print("It gets only 35000 words from the file")
        print("It find 10000 words from the file")
        print("You can change it in the code")
        data_from_lile = 35000
        to_find = 10000
        with open(path, 'r', encoding='utf-8') as file:
            words = file.read().split()[:data_from_lile]
        time_start = time.time()
        for _ in range(to_find):
            word = random.choice(words)
            words.index(word)
        time_end = time.time()
        print('Time for list: ', time_end - time_start)


        self.clear()
        for word in words:
            self.add2(word)

        time_start = time.time()
        for _ in range(to_find):
            word = random.choice(words)
            self.find2(word)
        time_end = time.time()
        print('Time for tree successively: ', time_end - time_start)


        self.clear()
        while words:
            word = random.choice(words)
            self.add(word)
            words.remove(word)

        with open(path, 'r', encoding='utf-8') as file:
            words = file.read().split()[:data_from_lile]

        time_start = time.time()
        for _ in range(to_find):
            word = random.choice(words)
            self.find(word)
        time_end = time.time()
        print('Time for tree random: ', time_end - time_start)


        self.rebalance()
        time_start = time.time()
        for _ in range(to_find):
            word = random.choice(words)
            self.find(word)
        time_end = time.time()
        print('Time for tree random rebalance: ', time_end - time_start)

tree = LinkedBST()
tree.demo_bst('words.txt')
