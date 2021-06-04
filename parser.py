import os

def instructions_parser(filepath):
    instructions = []
    arguments = []

    if not os.path.isfile(filepath):
        print('Invalid file path, file not found')
        exit()

    with open(filepath.rstrip('\r')) as file:
        complete_instructions = file.read().splitlines()
        for i, line in enumerate(complete_instructions):
            words = ' '.join(line.split()).split(' ')

            if words[0] == 'P':
                if len(words) < 3:
                    print('Invalid instruction, expected more arguments')
                    print('Skipping instruction {}'.format(i+1))
                else:
                    instructions.append(words[0])
                    arguments.append(int(words[1]))
                    arguments.append(int(words[2]))
            elif words[0] == 'A':
                if len(words) < 4:
                    print('Invalid instruction, expected more arguments')
                    print('Skipping instruction {}'.format(i+1))
                else:
                    instructions.append(words[0])
                    arguments.append(int(words[1]))
                    arguments.append(int(words[2]))
                    arguments.append(int(words[3]))
            elif words[0] == 'L':
                if len(words) < 2:
                    print('Invalid instruction, expected more arguments')
                    print('Skipping instruction {}'.format(i+1))
                else:
                    instructions.append(words[0])
                    arguments.append(int(words[1]))
            elif words[0] == 'C':
                instructions.append(words[0])
                # Joins words to be displayed
                arguments.append(' '.join(words[1::]))
            elif words[0] == 'F' or words[0] == 'E':
                instructions.append(words[0])
            else:
                print('Invalid instruction, unknown command')
                print('Skipping instruction {}'.format(i+1))

        return instructions, arguments
            