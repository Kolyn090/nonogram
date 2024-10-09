class Description:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.column_descriptions = []
        self.row_descriptions = []

    def get_row_description(self, y):
        return self.row_descriptions[y]

    def get_col_description(self, x):
        return self.column_descriptions[x]

    def from_file(self, file_path):
        with open(file_path, 'r') as file:
            lines = [line.replace('\n', '') for line in file.readlines()]

        self.width = int(lines[0].replace('width ', ''))
        self.height = int(lines[1].replace('height ', ''))

        idx_of_row = -1
        idx_of_col = -1
        for i in range(len(lines)):
            if lines[i] == 'rows':
                idx_of_row = i
            elif lines[i] == 'columns':
                idx_of_col = i

        if idx_of_row == -1 or idx_of_col == -1:
            raise Exception("Descriptor 'rows'/'columns' not found in .non file.")

        row_lines = [item for item in lines[idx_of_row+1:idx_of_col] if item]
        col_lines = [item for item in lines[idx_of_col+1:] if item]
        self.row_descriptions = [self.parse_row_desc(line) for line in row_lines]
        self.column_descriptions = [self.parse_row_desc(line) for line in col_lines]

    def parse_row_desc(self, s):
        return [int(num) for num in s.split(',')]
