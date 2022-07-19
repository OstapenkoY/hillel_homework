class colorizer:
    colors = {
        'grey': '\033[90m',
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'pink': '\033[95m',
        'turquoise': '\033[96m',
        'default': '\033[97m'
    }

    def __init__(self, color='default'):
        self.color = color

    def __enter__(self):
        print(self.colors.get(self.color, self.colors['default']))
        return

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(self.colors['default'])


with colorizer('red'):
    print('printed in red')
print('printed in default color')

