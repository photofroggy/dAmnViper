''' Simply provides a cross-platform
    wrapper for getting input from the
    console.
'''

try:
    base = raw_input
except NameError as e:
    base = input

def get_input(prompt='>> ', empty=False):
    while True:
        data = base(prompt).strip()
        if not data and not empty:
            continue
        return data

# EOF
