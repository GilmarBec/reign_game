from collections import namedtuple

env = namedtuple('Constants', ['colors', 'symbols'])([
    'red',
    'white',
    'green',
    'black',
    'purple',
    'yellow',
    'blue',
    '#ababab',
], [
    '👻',
    '🎃',
    '⛄',
    '👹',
    '👽',
    '🐶',
    '🐰',
    '🐳',
])

COLORS = env.colors
SYMBOLS = env.symbols
