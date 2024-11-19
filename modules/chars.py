qwerty_symbols = [
    "!", "\"", "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/",
    ":", ";", "<", "=", ">", "?", "@", "[", "\\", "]", "^", "_", "`", "{", "|", "}", "~"
]

pass_common_symbols = [
    "!", "#", "$", "%", "&", "(", ")", "*", "-", ".", "@", "^", "_"
]

pass_secure_symbols = [
    "!", "#", "$", "%", "&", "*", "@", "^"
]

numbers = [
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
]

lowercase_letters = [
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"
]

uppercase_letters = [
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"
]

def is_char_in_list(char, char_list):
    if not isinstance(char, str) or len(char) != 1:
        raise ValueError("El primer parámetro debe ser un carácter (cadena de longitud 1).")
    if not isinstance(char_list, list):
        raise ValueError("El segundo parámetro debe ser una lista.")

    return char in char_list
