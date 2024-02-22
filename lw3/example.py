from os import linesep

visited = []
def get_vertice_closure(machine_transitions, vertice, signal):
    global visited
    result = '' + vertice
    visited += [vertice]
    for transition in machine_transitions[vertice]:
        if transition[1] == signal or transition[1] == 'e':
            if transition[0] not in visited:
                result += get_vertice_closure(machine_transitions, transition[0], signal)
    return ''.join(sorted(set(result)))

with open("input.txt", "r") as f:
    with open("output.txt", "w") as w:
        machine_transitions = dict()
        all_possible_keys_transition = set()
        all_possible_vertices = set()
        for line in f:
            line = line.strip()
            if not line: continue

            vertice_name, tranition_patterns = line.split('->')
            vertice_name = vertice_name.strip()
            all_possible_vertices.add(vertice_name)
            tranition_patterns = tranition_patterns.split('|')
            tranition_patterns = list(map(lambda x: x.strip(), tranition_patterns))
            for pattern in tranition_patterns:
                if len(pattern) <= 1: continue
                if not pattern[0].isupper() or pattern[0] == '#':
                    if vertice_name not in machine_transitions:
                        machine_transitions[vertice_name] = list()
                    machine_transitions[vertice_name].append((pattern[1], pattern[0]))
                    all_possible_keys_transition.add(pattern[0])
                if not pattern[1].isupper() or pattern[1] == '#':
                    if pattern[0] not in machine_transitions:
                        machine_transitions[pattern[0]] = list()
                    machine_transitions[pattern[0]].append((vertice_name, pattern[1]))
                    all_possible_keys_transition.add(pattern[1])

        for vertice_name in all_possible_vertices:
            if vertice_name not in machine_transitions:
                machine_transitions[vertice_name] = ''

        visited = []

        # convert to sorted transition vertice
        transition_table = dict()
        for vertice_name in machine_transitions:
            transition_table[vertice_name] = dict()
            for transition in machine_transitions[vertice_name]:
                if transition[1] not in transition_table[vertice_name]:
                    transition_table[vertice_name][transition[1]] = ''
                transition_table[vertice_name][transition[1]] += transition[0]

        for vertice_key, vertice_value in transition_table.items():
            for transition_key, transition_value in vertice_value.items():
                transition_table[vertice_key][transition_key] = ''.join(sorted(set(transition_table[vertice_key][transition_key])))

        processing_table = list()
        processing_keys = list()
        processing_table.append(transition_table['S'])
        for vertice_key, vertice_value in processing_table[0].items():
            if vertice_key == 'e':
                visited = []
                processing_table[0][vertice_key] = get_vertice_closure(machine_transitions, 'S', 'e')
        processing_keys += ['S']
        current_index = 0

        while True:
            keys_to_process = []
            for vertice_key, vertice_transitions in processing_table[current_index].items():
                if vertice_transitions not in processing_keys and vertice_key not in processing_keys:
                    if len(vertice_transitions) == 0: continue
                    keys_to_process.append(vertice_transitions)

            if len(keys_to_process) == 0: break

            keys_to_process = sorted(set(keys_to_process))
            for key_to_process in keys_to_process:
                vertice = dict()
                for key in all_possible_keys_transition:
                    if key == 'e': continue
                    clojure = ''
                    for char in key_to_process:
                        visited = []
                        clojure += get_vertice_closure(machine_transitions, char, 'e')
                    vertice[key] = ''
                    for transition_table_vertice_name, transition_table_vertice_value in transition_table.items():
                        if transition_table_vertice_name not in key_to_process and transition_table_vertice_name not in clojure: continue

                        for transition_table_key, transition_table_value in transition_table_vertice_value.items():
                            if transition_table_key != key: continue
                            vertice[key] += transition_table_value
                            vertice[key] = ''.join(sorted(set(vertice[key])))

                processing_table.append(vertice)
                processing_keys.append(key_to_process)

            current_index += 1

        if 'H' in all_possible_vertices:
            if 'H' not in processing_keys:
                processing_table.append({
                    'H': {}
                })
            processing_keys.append('H')
        if processing_table[0].keys() == {'e'}:
            processing_table = processing_table[1:]
            processing_keys = processing_keys[1:]

        for i in range(len(processing_table)):
            w.write('\t' + processing_keys[i])
        w.write('\n')

        for key in sorted(all_possible_keys_transition):
            w.write(key + '\t')
            for processing_vertice, processing_key in zip(processing_table, processing_keys):
                char = processing_vertice[key] if key in processing_vertice else '-'
                char = '-' if char == '' else char
                w.write(char + '\t')
            w.write('\n')

