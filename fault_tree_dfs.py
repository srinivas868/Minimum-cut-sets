import queue
import machine_utilization

class Node:
    def __init__(self, key, name=None, left=None, right=None):
        self.key = key
        self.name = name
        self.left = left
        self.right = right

    def get_key(self):
        return self.key

    def set_key(self, key):
        self.key = key

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

    def get_component(self):
        return self.component

    def get_parent_branch(self):
        return self.parent_branch


class Tree:

    #1,2,3
    def add(self, root, current, left, right):
        c_input = current.split('=')
        l_node = self.construct_node(left)
        r_node = self.construct_node(right)
        if root is None:
            root = Node(c_input[0], c_input[1], l_node, r_node)
            return root
        else:
            c_node = self.find_node(root, c_input[0])
            if c_node is not None:
                c_node = Node(c_node.key, c_node.name, l_node, r_node)
                return self.replace_node(root, c_node)


    def construct_node(self, input):

        if input != '':
            array = input.split('=')
            return Node(array[0], array[1])
        return None

    def replace_node(self, root, node):

        if root is None:
            return None
        if root.key == node.key:
            return node
        root.left = self.replace_node(root.left, node)
        root.right = self.replace_node(root.right, node)
        return root


    def find_node(self, root, current):

        if root is None:
            return None
        elif root.key == current:
            return root
        n1 = self.find_node(root.left, current)
        if n1 is not None:
            return n1
        else:
            n2 = self.find_node(root.right, current)
            return n2


visited = []

def print_dfs(root, path):

    path = path+"-"+str(root.name)
    if root.left is not None:
        print_dfs(root.left, path)
    else:
        if root.key not in visited:
            visited.append(root.key)
            print(path)
    if root.right is not None:
        print_dfs(root.right, path)


def main():
    tree = Tree()
    root = None
    with open("input_fault_tree.txt", "r") as ins:
        for line in ins:
            line = line.replace(' ', '')
            inputs = line.strip().split(',')
            root = tree.add(root, inputs[0], inputs[1], inputs[2])
    print_dfs(root, "")
    machine_utilization.track()


if __name__ == '__main__':
    main()
