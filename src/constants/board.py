from collections import namedtuple

env = namedtuple('Constants', ['state', 'cards'])([
    'ARMY-FAITH',
    'ARMY-BETRAYAL',
    'REVOLT',
    'BATTLE',
], [
    '🂷',
    '🂸',
    '🂹',
    '🂺',
    '🂻',
    '🂼',
    '🂽',
    '🂾',
    '🃁',
    '🃂',
    '🃃',
    '🃄',
    '🃅',
    '🃆',
    '🃇',
    '🃈',
    '🃉',
    '🃊',
    '🃋',
    '🃌',
    '🃍',
    '🃎',
    '🃑',
    '🃒',
    '🃓',
    '🃔',
    '🃕',
    '🃖',
    '🃗',
    '🃘',
    '🃙',
    '🃚',
    '🃛',
    '🃜',
    '🃝',
    '🃞',
    '🃒',
    '🃒',
])

STATES = env.state
CARDS = env.cards
