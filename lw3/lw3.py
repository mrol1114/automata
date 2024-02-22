from pyvis.network import Network

class Machine:
    START_STATE_INDEX = 0
    STATE_SYMBOL = 'S'
    EMPTY_SIGNAL = 'e'
    END_STATE_SIGNAL = '#'

    def __init__(self):
        self.transitions = {}
        self.next_state_index = 1
        self.input_signals = []

    def read_machine_from_file(self):
        with open("input.txt", "r") as f:
            grammar_type = f.readline().strip()
            file_vertical_name_to_state_name = {}

            for line in f:
                line = line.strip()
                if not line:
                    continue

                vertical_file_name, transition_patterns = line.split('->')
                transition_patterns = transition_patterns.split('|')
                transition_patterns = list(map(lambda x: x.strip(), transition_patterns))

                vertical_file_name = vertical_file_name.strip()
                self.add_transition_from_file(vertical_file_name, file_vertical_name_to_state_name)

                for pattern in transition_patterns:
                    if len(pattern) < 2:
                        continue

                    if grammar_type == 'left':
                        if pattern[0] not in file_vertical_name_to_state_name:
                            self.add_transition_from_file(pattern[0], file_vertical_name_to_state_name)

                        if pattern[1] not in self.transitions[file_vertical_name_to_state_name[pattern[0]]]:
                            self.transitions[file_vertical_name_to_state_name[pattern[0]]][pattern[1]] = set()

                        if pattern[1] != self.EMPTY_SIGNAL and pattern[1] not in self.input_signals:
                            self.input_signals.append(pattern[1])

                        self.transitions[file_vertical_name_to_state_name[pattern[0]]][pattern[1]].add(
                            file_vertical_name_to_state_name[vertical_file_name]
                        )

                    elif grammar_type == 'right':
                        if pattern[1] not in file_vertical_name_to_state_name:
                            self.add_transition_from_file(pattern[1], file_vertical_name_to_state_name)

                        if pattern[0] not in self.transitions[file_vertical_name_to_state_name[vertical_file_name]]:
                            self.transitions[file_vertical_name_to_state_name[vertical_file_name]][pattern[0]] = set()

                        if pattern[0] != self.EMPTY_SIGNAL and pattern[0] not in self.input_signals:
                            self.input_signals.append(pattern[0])

                        self.transitions[file_vertical_name_to_state_name[vertical_file_name]][pattern[0]].add(
                            file_vertical_name_to_state_name[pattern[1]]
                        )

    def clear_empty_transitions(self):
        short_circuit = {}

        for state_name, transitions in self.transitions.items():
            visited = set()
            states = set()
            states.add(state_name)
            short_circuit[state_name] = set()

            while states:
                curr_state = states.pop()
                short_circuit[state_name].add(curr_state)
                empty_transitions = self.transitions[curr_state][self.EMPTY_SIGNAL] if self.EMPTY_SIGNAL in self.transitions[curr_state] else set()

                curr_set = set()
                curr_set.add(curr_state)
                visited = visited.union(curr_set)
                states = states.union(empty_transitions.difference(visited))

        new_transitions = {}
        for main_state, included_states in short_circuit.items():
            new_transitions[main_state] = {}

            for state in included_states:
                for input_signal, states in self.transitions[state].items():
                    if input_signal == self.EMPTY_SIGNAL:
                        continue
                    if input_signal not in new_transitions[main_state]:
                        new_transitions[main_state][input_signal] = set()
                    new_transitions[main_state][input_signal] = new_transitions[main_state][input_signal].union(states)

        self.transitions = new_transitions

    def determine(self):
        new_transitions = {}
        unprocessed_new_states = []
        added_new_states = []
        added_new_states_aliases = []

        for existing_state in self.transitions.keys():
            init_value = set()
            init_value.add(existing_state)
            unprocessed_new_states.append(init_value)

            while len(unprocessed_new_states) > 0:
                unprocessed_states = unprocessed_new_states.pop()

                transitions = {}
                for state in unprocessed_states:
                    for input_signal, states in self.transitions[state].items():
                        if input_signal not in transitions:
                            transitions[input_signal] = set()
                        transitions[input_signal] = transitions[input_signal].union(states)

                if len(unprocessed_states) > 1:
                    curr_state = self.STATE_SYMBOL + str(self.next_state_index)
                    self.next_state_index += 1
                    added_new_states_aliases.append(curr_state)
                    added_new_states.append(unprocessed_states)
                else:
                    curr_state = list(unprocessed_states)[0]

                new_transitions[curr_state] = {}
                for input_signal, states in transitions.items():
                    new_transitions[curr_state][input_signal] = states

                    if len(states) > 1 and states not in added_new_states:
                        unprocessed_new_states.append(states)

            for main_state, transitions in new_transitions.items():
                for input_signal, states in transitions.items():

                    if len(states) > 1:
                        new_transitions[main_state][input_signal] = set([added_new_states_aliases[added_new_states.index(states)]])

        self.transitions = new_transitions

    def print_machine_to_file(self):
        with open("output.txt", "w") as w:
            sorted_states = list(self.transitions.keys())
            sorted_states.sort()

            sorted_input_signals = self.input_signals
            sorted_input_signals.sort()

            transitions_rows = []
            for input_signal in sorted_input_signals:
                transitions_rows.append([])
                for main_state in sorted_states:
                    state = list(self.transitions[main_state][input_signal])[0] if input_signal in self.transitions[main_state] else '-'
                    transitions_rows[len(transitions_rows) - 1].append(state)

            row_format = "{:>8}" * (len(sorted_states) + 1)
            w.write(row_format.format("", *sorted_states) + "\n")
            for team, row in zip(sorted_input_signals, transitions_rows):
                w.write(row_format.format(team, *row) + "\n")

    def add_transition_from_file(self, adding_state, vertical_name_to_state):
        if adding_state not in vertical_name_to_state:
            vertical_name_to_state[adding_state] = self.STATE_SYMBOL + str(self.next_state_index)
            self.transitions[vertical_name_to_state[adding_state]] = {}
            self.next_state_index += 1

    def visualize(self):
        net = Network(notebook=True, directed=True)

        for state in self.transitions.keys():
            net.add_node(state, label=state)

        for main_state, transitions in self.transitions.items():
            for input_signal, states in transitions.items():
                net.add_edge(
                    main_state,
                    list(states)[0],
                    label=input_signal
                )

        net.show('index.html')


machine = Machine()

machine.read_machine_from_file()
machine.clear_empty_transitions()
machine.determine()
machine.print_machine_to_file()
machine.visualize()
