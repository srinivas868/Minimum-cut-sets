import copy
import queue
import machine_utilization


class Node:

    def __init__(self, val):
        self.val = val
        self.leftChild = None
        self.rightChild = None
        self.key = None

    def get(self):
        return self.val

    def set(self, val):
        self.val = val

    def set_left_child(self, node):
        self.leftChild = node

    def set_right_child(self, node):
        self.rightChild = node


def insert_node(root, val, left):

    if root is None:
        root = Node(val)
        zero_node = Node('0')
        one_node = Node('1')
        root.leftChild = one_node
        root.rightChild = zero_node
        return root
    elif root.val == '1' or root.val == '0':
        return insert_node(None, val, left)
    elif left:
        root.leftChild = insert_node(root.leftChild, val, left)
    else:
        root.rightChild = insert_node(root.rightChild, val, left)
    return root


def insert_bdd(root, node, side):

    if root is None:
        return node
    elif root.val == '1' or root.val == '0':
        return insert_bdd(None, node, side)
    elif side == 'left':
        root.leftChild = insert_bdd(root.leftChild, node, side)
    else:
        root.rightChild = insert_bdd(root.rightChild, node, side)
    return root


def insert_at_left(i_node, node):

    if i_node.leftChild.val == '1':
        t_node = copy.copy(i_node)
        t_node.leftChild = node
        return t_node
    i_node.leftChild = insert_at_left(i_node.leftChild, node)
    return i_node


def insert_at_right(root, node):

    if root.rightChild.val == '0':
        t_node = copy.copy(root)
        t_node.rightChild = node
        return t_node
    root.rightChild = insert_at_right(root.rightChild, node)
    return root


def merge(root, node):

    if root.rightChild.val == '0':
        root.rightChild = node
        return root
    return merge(root.rightChild, node)


def get_left_sub_tree(node):

    t_node = copy.copy(node)
    t_node.rightChild = Node('0')
    return t_node


def multiply_bdds(a, b):

    a_tree_pointer = a.rightChild
    a_tree = get_left_sub_tree(a)
    result = None
    while a_tree.val != '0':
        b_tree_pointer = b.rightChild
        b_tree = get_left_sub_tree(b)
        temp_result = None
        while b_tree.val != '0':
            if temp_result is not None:
                temp_result = insert_at_right(temp_result, insert_at_left(copy.copy(a_tree), copy.copy(b_tree)))
            else:
                temp_result = insert_at_left(copy.copy(a_tree), copy.copy(b_tree))
            b_tree = get_left_sub_tree(b_tree_pointer)
            b_tree_pointer = b_tree_pointer.rightChild
        a_tree = get_left_sub_tree(a_tree_pointer)
        a_tree_pointer = a_tree_pointer.rightChild
        if result is None:
            result = temp_result
        else:
            merge(result, temp_result)
    return result


def merge_bdds(type, bdd_one, bdd_two):

    if type == '+':
        bdd_one = insert_bdd(bdd_one, bdd_two, 'right')
    else:
        bdd_one = multiply_bdds(bdd_one, bdd_two)
    return bdd_one


def construct_bdds(input):

    root = None
    left = None
    for exp in input:
        if exp == '*':
            left = True
        elif exp == '+':
            left = False
        else:
            root = insert_node(root, exp, left)
    return root


def remove_repeated_node(root, child, val, count):

    if root.val == '1':
        return root
    if child.val == val:
        if count == 1:
            root.leftChild = child.leftChild
            return root
        else:
            count += 1
    return remove_repeated_node(child, child.leftChild, val, count)


def reduce(root):

    a_tree_pointer = root.rightChild
    a_tree = get_left_sub_tree(root)
    result = None
    while a_tree.val != '0':
        i_node = copy.copy(a_tree)
        while i_node.val != '1':
            if a_tree.val == i_node.val:
                count = 1
            else:
                count = 0
            remove_repeated_node(a_tree, a_tree.leftChild, i_node.val, count)
            i_node = i_node.leftChild
        if result is None:
            result = a_tree
        else:
            merge(result, a_tree)
        a_tree = get_left_sub_tree(a_tree_pointer)
        a_tree_pointer = a_tree_pointer.rightChild
    return result


def print_min_cut_set(root, path):

    path = path + "-" + str(root.val)
    if root.leftChild is not None and root.leftChild.val != '1':
        print_min_cut_set(root.leftChild, path)
    else:
        print(path)
    if root.rightChild and root.rightChild.val != '0':
        print_min_cut_set(root.rightChild, "")


def main():
    main_input = "(a+e)b*(c+d)"
    bdd1 = construct_bdds("b")
    bdd2 = construct_bdds("c+d")
    bdd3 = construct_bdds("a+e")
    bdd4 = construct_bdds("a*e")

    merge_bdd = merge_bdds("*", bdd1, bdd2)
    result = merge_bdds("*", bdd3, merge_bdd)

    reduced = reduce(copy.copy(result))
    print("Start printing")
    print_min_cut_set(reduced, "")

    print('dd')


if __name__ == '__main__':
    main()
