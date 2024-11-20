QWERTY_SYMB = set([
    '"', "'", '+', ',', '/', ':', ';', '<', '=', '>', '?', '[', '\\', ']', '`', '{', '|', '}', '~'
])

COMM_SYMB = set([
    '(', ')', '-', '.', '_'
])

SEC_SYMB = set([
    "!", "#", "$", "%", "&", "*", "@", "^"
])

NUMS = set([
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
])

LOWER = set([
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"
])

UPPER = set([
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"
])

ALLOWED_CHARS = (QWERTY_SYMB | COMM_SYMB | SEC_SYMB | NUMS | LOWER | UPPER)

def pass_has_chartype(password, char_list):
    return any(char in char_list for char in password)

def validate_password(password):
    return all(char in ALLOWED_CHARS for char in password)