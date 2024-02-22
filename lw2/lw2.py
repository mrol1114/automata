from pyvis.network import Network
from enum import Enum


class AutomataType(Enum):
    Milli = 'milli'
    Mur = 'mur'
    NotDefined = 'none'


class Automata:
    STATE_SYMBOL = 's'
    OUTPUT_SIGNAL_SYMBOL = 'y'
    INPUT_SIGNAL_SYMBOL = 'x'
    DELIMITER_SYMBOL = '/'
    EMPTY_SYMBOL = '-'
    GROUP_SYMBOL = 'q'

    def __init__(self):
        self.data = {}
        self.type = AutomataType.NotDefined
        self.number_of_states = 0
        self.number_of_in_signals = 0

    def init_from_file(self):
        with open('input.txt') as f:
            [number_of_states, number_of_in_signals, type_name] = f.readline().rstrip().split(' ')
            number_of_states = int(number_of_states)
            self.number_of_states = number_of_states
            number_of_in_signals = int(number_of_in_signals)
            self.number_of_in_signals = number_of_in_signals

            if type_name == AutomataType.Mur.value:
                self.type = AutomataType.Mur
            if type_name == AutomataType.Milli.value:
                self.type = AutomataType.Milli

            if self.type == AutomataType.Milli:
                line_number = 0

                while line_number < number_of_in_signals:
                    line_number += 1
                    line = f.readline().rstrip()

                    paths = [path.split(self.DELIMITER_SYMBOL) for path in line.split(' ')]
                    for i in range(0, number_of_states):
                        if self.STATE_SYMBOL + str(i + 1) in self.data:
                            self.data[self.STATE_SYMBOL + str(i + 1)].append((paths[i][0], paths[i][1]))
                        else:
                            self.data[self.STATE_SYMBOL + str(i + 1)] = [(paths[i][0], paths[i][1])]

            if self.type == AutomataType.Mur:
                line_number = 0
                states = [state.split(self.DELIMITER_SYMBOL) for state in f.readline().rstrip().split(' ')]
                states = [(state[0], state[1]) for state in states]
                while line_number < number_of_in_signals:
                    line_number += 1
                    line = f.readline().rstrip()

                    paths = [int(path_number) for path_number in line.split(' ')]
                    for i in range(0, number_of_states):
                        if states[i] in self.data:
                            self.data[states[i]].append(states[paths[i] - 1])
                        else:
                            self.data[states[i]] = [(states[paths[i] - 1])]

    def transform_to_milli(self):
        if self.type == AutomataType.Milli or self.type == AutomataType.NotDefined:
            return
        new_data = {}
        states_numbers = []

        for state in self.data.keys():
            if state[0][1] not in states_numbers:
                new_data[state[0]] = self.data[state]
                states_numbers.append(state[0])

        self.data = new_data
        self.number_of_states = len(self.data)
        self.type = AutomataType.Milli

    def transform_to_mur(self):
        if self.type == AutomataType.Mur or self.type == AutomataType.NotDefined:
            return
        new_data = {}

        for paths in self.data.values():
            for path in paths:
                new_data[path] = self.data[path[0]]

        self.data = new_data
        self.number_of_states = len(self.data)
        self.type = AutomataType.Mur

    def print_to_file(self):
        with open('output.txt', 'w') as f:
            if self.type == AutomataType.Milli:
                for index_of_in_signal in range(0, self.number_of_in_signals):
                    for state_number in range(1, self.number_of_states + 1):
                        state_key = self.STATE_SYMBOL + str(state_number)
                        f.write(self.data[state_key][index_of_in_signal][0]
                                + self.DELIMITER_SYMBOL + self.data[state_key][index_of_in_signal][1] + ' ')
                    f.write('\n')

            if self.type == AutomataType.Mur:
                states_keys = [state for state in self.data.keys()]
                states_keys.sort()

                for state_key in states_keys:
                    f.write(state_key[0] + self.DELIMITER_SYMBOL + state_key[1] + ' ')
                f.write('\n')

                for index_of_in_signal in range(0, self.number_of_in_signals):
                    for state_key in states_keys:
                        f.write(str(states_keys.index(self.data[state_key][index_of_in_signal]) + 1) + ' ')
                    f.writelines()
                    f.write('\n')

    def minimize(self):
        prev_groups = {}
        curr_groups = {}
        prev_state_to_group = {}
        curr_state_to_group = {}
        groups_values = []

        if self.type == AutomataType.Milli:
            for state, paths in self.data.items():
                output_signals = [int(path[1][1]) for path in paths]
                if output_signals not in groups_values:
                    groups_values.append(output_signals)
                    prev_groups[groups_values.index(output_signals)] = []
                prev_groups[groups_values.index(output_signals)].append(state)
                prev_state_to_group[state] = groups_values.index(output_signals)

        if self.type == AutomataType.Mur:
            states_keys = [state for state in self.data.keys()]
            states_keys.sort()
            for state in states_keys:
                output_signals = int(state[1][1])
                if output_signals not in groups_values:
                    groups_values.append(output_signals)
                    prev_groups[groups_values.index(output_signals)] = []
                prev_groups[groups_values.index(output_signals)].append(state)
                prev_state_to_group[state] = groups_values.index(output_signals)

        is_minimized = False
        while not is_minimized:
            is_minimized = True
            groups_values = []

            for group_id, states in prev_groups.items():
                new_groups = {}
                new_groups_values = []

                for state in states:
                    output_signals = [prev_state_to_group[path[0] if self.type == AutomataType.Milli else path]
                                      for path in self.data[state]]
                    if output_signals not in new_groups_values:
                        new_groups_values.append(output_signals)
                        new_groups[new_groups_values.index(output_signals) + len(groups_values)] = []
                    new_groups[new_groups_values.index(output_signals) + len(groups_values)].append(state)
                    curr_state_to_group[state] = new_groups_values.index(output_signals) + len(groups_values)

                groups_values = [*groups_values, *new_groups_values]
                curr_groups = {**curr_groups, **new_groups}
                if (len(new_groups) > 1):
                    is_minimized = False

            prev_groups = curr_groups
            prev_state_to_group = curr_state_to_group
            curr_groups = {}
            curr_state_to_group = {}

        minimized_machine = {}

        if self.type == AutomataType.Milli:
            for group_id, states in prev_groups.items():
                paths = self.data[states[0]]
                minimized_machine[self.STATE_SYMBOL + str(group_id + 1)] = []
                for i in range(0, len(paths)):
                    minimized_machine[self.STATE_SYMBOL + str(group_id + 1)].append(
                        (self.STATE_SYMBOL + str(groups_values[group_id][i] + 1), paths[i][1])
                    )

        if self.type == AutomataType.Mur:
            for group_id, states in prev_groups.items():
                paths = self.data[states[0]]
                minimized_machine[(self.STATE_SYMBOL + str(group_id + 1), states[0][1])] = []
                for i in range(0, len(paths)):
                    minimized_machine[(self.STATE_SYMBOL + str(group_id + 1), states[0][1])].append(
                        (self.STATE_SYMBOL + str(groups_values[group_id][i] + 1), paths[i][1])
                    )

        self.data = minimized_machine
        self.number_of_states = len(self.data)

class GraphVisualizer:
    def __init__(self, automata: Automata):
        self.automata = automata

    def draw_automata(self):
        net = Network(notebook=True, directed=True)

        if automata.type == AutomataType.Milli:

            for state_key in automata.data:
                net.add_node(state_key, label=state_key)

            for state_key in automata.data:
                for path_index in range(0, len(automata.data[state_key])):
                    path = automata.data[state_key][path_index]
                    net.add_edge(
                        state_key,
                        path[0],
                        label=automata.INPUT_SIGNAL_SYMBOL + str(path_index + 1) + automata.DELIMITER_SYMBOL + path[1]
                    )

        if automata.type == AutomataType.Mur:

            for state_key in automata.data:
                net_state_key = state_key[0] + automata.DELIMITER_SYMBOL + state_key[1]
                net.add_node(net_state_key, label=net_state_key)

            for state_key in automata.data:
                for path_index in range(0, len(automata.data[state_key])):
                    path = automata.data[state_key][path_index]
                    net.add_edge(
                        state_key[0] + automata.DELIMITER_SYMBOL + state_key[1],
                        path[0] + automata.DELIMITER_SYMBOL + path[1],
                        label=automata.INPUT_SIGNAL_SYMBOL + str(path_index + 1)
                    )

        net.show('index.html')


automata = Automata()
automata.init_from_file()

automata.minimize()

automata.print_to_file()

visualizer = GraphVisualizer(automata)
visualizer.draw_automata()