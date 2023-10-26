import subprocess
import matplotlib.pyplot as plt


class TinyGPRunner:
    JAVA_FILE_DIR = 'java_files'
    JAVA_CLASS_NAME = 'tiny_gp'

    def __init__(self, problem_path: str):
        self.problem_path = problem_path

    def run(self):
        best_individual = ''
        best_fitness_values = []
        avg_fitness_values = []
        with subprocess.Popen(['java', f'{self.JAVA_FILE_DIR}.{self.JAVA_CLASS_NAME}', self.problem_path],
                              stdout=subprocess.PIPE,
                              bufsize=1,
                              universal_newlines=True) as p:

            for line in p.stdout:
                if 'Generation' in line:
                    best_fitness_values.append(self.extract_best_fitness(line))
                    avg_fitness_values.append(self.extract_average_fitness(line))
                    generation = self.extract_generation(line)

                    if generation % 10 == 0:
                        print(f'Generation {generation} finished')

                if 'Best Individual' in line:
                    best_individual = line.replace('Best Individual: ', '').strip()

        print(f'Best individual after 30 generations: {best_individual}')

        with open(self.problem_path, 'r') as f:
            header = f.readline()
            no_vars = int(header.split(' ')[0])

        problem_name = self.problem_path.split('/')[1].split('.')[0]

        with open(f'functions/{problem_name}.py', 'w') as f:
            problem_id = problem_name.replace('problem_', '')
            f.write(f'def f_{problem_id}(')
            for i in range(no_vars - 1):
                f.write(f'X{i + 1}: float, ')
            f.write(f'X{no_vars}: float')
            f.write(') -> float:\n')
            f.write(f'    return {best_individual}')

        with open(f'functions/plots/{problem_name}.png', 'wb') as f:
            plt.plot(range(1, len(best_fitness_values) + 1), best_fitness_values, label='Best fitness')
            plt.plot(range(1, len(avg_fitness_values) + 1), avg_fitness_values, label='Average fitness')
            plt.xlabel('Generation')
            plt.ylabel('Fitness')
            plt.title(f'Best and average fitness values for problem {problem_name}')
            plt.legend()
            plt.savefig(f, format='png')

    @staticmethod
    def extract_best_fitness(line: str) -> float:
        return float(line.split(' ')[4].replace('Fitness=', ''))

    @staticmethod
    def extract_average_fitness(line: str) -> float:
        return float(line.split('')[2].replace('Fitness=', ''))

    @staticmethod
    def extract_generation(line: str) -> int:
        return int(line.split(' ')[0].replace('Generation=', ''))