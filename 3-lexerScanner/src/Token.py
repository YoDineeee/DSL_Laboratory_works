from collections import namedtuple

# Define Token structure
token_fields = ['token_type', 'value', 'line', 'column']
Token = namedtuple('Token', token_fields)
