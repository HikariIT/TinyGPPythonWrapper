import subprocess


class TinyGPRunner:
    JAVA_FILE_DIR = 'java_files'
    JAVA_CLASS_NAME = 'tiny_gp'

    def __init__(self, problem_path: str):
        self.problem_path = problem_path

    def run(self):
        best_individual = ''
        with subprocess.Popen(['java', f'{self.JAVA_FILE_DIR}.{self.JAVA_CLASS_NAME}', self.problem_path],
                              stdout=subprocess.PIPE,
                              bufsize=1,
                              universal_newlines=True) as p:

            for line in p.stdout:
                if 'Generation' in line:
                    best_fitness = self.extract_best_fitness(line)

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

    @staticmethod
    def extract_best_fitness(line: str) -> float:
        return float(line.split(' ')[4].replace('Fitness=', ''))

    @staticmethod
    def extract_generation(line: str) -> int:
        return int(line.split(' ')[0].replace('Generation=', ''))