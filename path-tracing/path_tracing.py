import queue
import machine_utilization


class Data:
    def __init__(self, node_number, parent_branch, branch_number, component, status):
        self.node_number = node_number
        self.parent_branch = parent_branch
        self.branch_number = branch_number
        self.component = component
        self.status = status

    def get_node_number(self):
        return self.node_number

    def set_node_number(self, node_number):
        self.node_number = node_number

    def get_branch_number(self):
        return self.branch_number

    def get_status(self):
        return self.status

    def get_component(self):
        return self.component

    def get_parent_branch(self):
        return self.parent_branch


def trace_all_min_paths(connection_matrix, matrix_count):
    counter = 1
    matrix_count = 10
    path_data_map = {}
    queue_list = queue.Queue()
    input_data = Data(1, 0, 0, '', 'True')
    queue_list.put(input_data)

    while not queue_list.empty():
        i_data = queue_list.get()
        row_number = i_data.get_node_number()
        branch_number = i_data.get_branch_number()
        status = i_data.get_status()
        component = i_data.get_component()
        path_data_map[branch_number] = i_data
        if status == 'True':
            for i in range(len(connection_matrix[row_number])):
                if connection_matrix[row_number][i] != component and connection_matrix[row_number][i] != '1' \
                        and connection_matrix[row_number][i] != '0':
                    if i < matrix_count-1:
                        status = 'True'
                    else:
                        status = 'False'
                    data = Data(i+1, branch_number, counter, connection_matrix[row_number][i], status)
                    queue_list.put(data)
                    counter += 1
    return path_data_map


def print_identified_path(path_data, path_data_map):

    que = queue.Queue()
    que.put(path_data)
    path = ''
    while not que.empty():
        data = que.get()
        path += str(data.get_component())+"-"
        parent_branch_number = data.get_parent_branch()
        if parent_branch_number > 0:
            data = path_data_map[parent_branch_number]
            que.put(data)
    print(path)


def retrieve_all_min_paths(path_data_map, matrix_count):
    for key in path_data_map:
        path_data = path_data_map[key]
        node_number = path_data.get_node_number()
        if node_number == matrix_count:
            print('Printing path -->> ')
            print_identified_path(path_data, path_data_map)


def main():
    connection_matrix = []
    i = 1
    array = []
    with open("example_1.txt", "r") as ins:
        for line in ins:
            if i == 1:
                matrix_count = int(line.strip())
                for x in range(matrix_count):
                    array.append('')
                connection_matrix.append(array)
            else:
                array = line.strip().split(', ')
                connection_matrix.append(array)
            i += 1
    path_data_map = trace_all_min_paths(connection_matrix, matrix_count)
    retrieve_all_min_paths(path_data_map, matrix_count)
    machine_utilization.track()


if __name__ == '__main__':
    main()