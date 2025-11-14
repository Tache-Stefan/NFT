from collections import defaultdict

class Translator:
    def __init__(self, states, initial_state, final_states, sigma, gamma, delta):
        self.Q = set(states)
        self.q0 = initial_state
        self.F = set(final_states)
        self.Sigma = set(sigma)
        self.Gamma = set(gamma)
        self.Delta = delta
        self.lambda_symbol = 'lambda'

    def lambda_closure(self, start_state):
        stack = [(start_state, "")]
        closure = set([(start_state, "")])

        while stack:
            current_state, current_output = stack.pop()

            state_moves = self.Delta.get(current_state, {})
            lambda_moves = state_moves.get(self.lambda_symbol, [])

            for next_state, output_part in lambda_moves:
                new_output = current_output + output_part
                new_configuration = (next_state, new_output)
                
                if new_configuration not in closure:
                    closure.add(new_configuration)
                    stack.append(new_configuration)

        return closure
    
    def simulate(self, input_string):
        stack = []

        initial_closure = self.lambda_closure(self.q0)
        for state, output_part in initial_closure:
            stack.append((state, input_string, output_part))
        
        final_outputs = set()

        while stack:
            current_state, remaining_input, generated_output = stack.pop()

            if not remaining_input:
                if current_state in self.F:
                    final_outputs.add(generated_output)
                continue
            
            input_symbol = remaining_input[0]
            next_remaining_input = remaining_input[1:]

            moves = self.Delta.get(current_state, {}).get(input_symbol, [])

            for next_state_move, output_part_move in moves:
                next_closure = self.lambda_closure(next_state_move)

                for state_after_lambda, output_part_lambda in next_closure:
                    new_output = generated_output + output_part_move + output_part_lambda
                    stack.append((state_after_lambda, next_remaining_input, new_output))
            
        return final_outputs
    
    def __repr__(self):
        return (f"Translator(\n"
                f"  States: {self.Q},\n"
                f"  Initial State: {self.q0},\n"
                f"  Final States: {self.F},\n"
                f"  Sigma: {self.Sigma},\n"
                f"  Gamma: {self.Gamma},\n"
                f"  Delta: {self.Delta}\n"
                f")")

def read_translator(filename='translator.txt'):
    with open(filename, 'r') as file:
        lines = file.readlines()
    lines = [line.strip().split(': ') for line in lines if line.strip()]
    
    states_string = lines[0][1]
    states = states_string.split(', ')
    
    initial_state = lines[1][1]

    final_states_string = lines[2][1]
    final_states = final_states_string.split(', ')

    sigma = lines[3][1].split(', ')

    gamma = lines[4][1].split(', ')

    delta = defaultdict(dict)
    for line in lines[6:]:
        parts = line[0].split(',')
        delta[parts[0]].setdefault(parts[1], []).append((parts[2], parts[3]))

    return Translator(states, initial_state, final_states, sigma, gamma, delta)

if __name__ == "__main__":
    translator = read_translator()
    
    input_string = "0101"
    outputs = translator.simulate(input_string)
    print(f"Input String: {input_string}")
    print(f"Output(s): {outputs}")
