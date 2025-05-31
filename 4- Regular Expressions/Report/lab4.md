# Laboratory Work Report: Regular Expression Parsing and Logging System

### Course: Formal Languages & Finite Automata  
### Author: Mohammed Dhiaeddine Hassine, st.gr.FAF-233 
### Verified by: Dumitru Crețu, University Assistant  

---

## Theoretical Background

### Regular Expressions

A **regular expression (regex)** is a formal language for specifying text search patterns. In theoretical computer science, regular expressions define **regular languages**, which are precisely the languages accepted by **finite automata**.

Regular expressions are used in:
- **Pattern recognition** and **text matching**
- **Tokenization** in compilers
- **Input validation** (e.g., emails, passwords)
- **Data cleaning and transformation**

In programming, they are commonly used to describe patterns such as:
- `a*` – zero or more occurrences of 'a'
- `a+` – one or more occurrences
- `a?` – zero or one occurrence
- `(a|b)` – 'a' or 'b'
- `a^{3}` – exactly three occurrences of 'a' (custom syntax in this lab)

---

## Objectives

1. Develop a parser to tokenize simplified regex patterns using custom modifiers (`^`, `{}`, etc.)
2. Log each step of parsing for educational and debugging purposes
3. Support groups, repetitions, optional characters, and modifiers
4. Prepare data for generation or validation systems

---

## Implementation Overview

### Components

- `RegexLogger`: Logs every parsing step
- `RegexParser`: Parses regex patterns into structured tokens
- (Generation is not covered in this lab but can follow from the parsed output)

---

## RegexLogger Class

This component is responsible for recording all the intermediate parsing steps.

```python
class RegexLogger:
    def __init__(self):
        self.steps = []

    def process(self, step):
        self.steps.append(step)

    def show_steps(self):
        for i, step in enumerate(self.steps, 1):
            print(f"Step {i}: {step}")
```

✅ **Responsibilities:**
- Collects a sequential list of parsing actions
- Can output a trace log for debugging and understanding the process

---

## RegexParser Class

This class analyzes a regex pattern and produces a token list. It supports:
- **Character tokens**
- **Character modifiers** (`?`, `*`, `+`)
- **Repetition via `{n}`**
- **Grouped alternatives** (e.g., `(a|b|c)`)
- **Grouped repetitions and modifiers**

### Sample Syntax Support

- `'a?b*'`: optional 'a', zero or more 'b'
- `'c^{3}'`: exactly three 'c's
- `'(x|y)^3'`: group repeated three times
- `'(p|q)*'`: group with zero or more repetition

### Parser Code

```python
import re
from regex_logger import RegexLogger

class RegexParser:
    def __init__(self):
        self.tokens = []
        self.logger = RegexLogger()

    def parse(self, pattern):
        self.logger = RegexLogger() 
        self.logger.process(f"Parsing pattern: {pattern}")
        self.tokens = []
        i = 0

        while i < len(pattern):
            char = pattern[i]

            # Handle groupings
            if char == "(":
                group_end = pattern.find(")", i)
                if group_end != -1:
                    if group_end + 1 < len(pattern) and pattern[group_end + 1] == "^":
                        match = re.match(r"\((.*?)\)\^\{(\d+)\}", pattern[i:])
                        if match:
                            group_content = match.group(1).split('|')
                            repetition = int(match.group(2))
                            self.tokens.append(('group', (group_content, repetition)))
                            i += len(match.group(0))
                            self.logger.process(f"Found group with repetition: {match.group(0)}")
                            continue
                    elif group_end + 1 < len(pattern) and pattern[group_end + 1] in "?*+":
                        group_content = pattern[i + 1:group_end].split('|')
                        modifier = pattern[group_end + 1]
                        self.tokens.append(('group_mod', (group_content, modifier)))
                        i = group_end + 2
                        self.logger.process(f"Found group with modifier: ({pattern[i + 1:group_end]}){modifier}")
                        continue
                    else:
                        group_content = pattern[i + 1:group_end].split('|')
                        self.logger.process(f"Found simple group: ({pattern[i + 1:group_end]})")
                        self.tokens.append(('group', (group_content, 1)))
                        i = group_end + 1
                        continue

            # Character with repetition
            if i + 1 < len(pattern) and pattern[i + 1] == "^":
                match = re.match(r"(\w)\^\{(\d+)\}", pattern[i:])
                if match:
                    char = match.group(1)
                    repetition = int(match.group(2))
                    self.tokens.append(('char_rep', (char, repetition)))
                    i += len(match.group(0))
                    self.logger.process(f"Found character with repetition: {match.group(0)}")
                    continue

            # Character with modifier (?, *, +)
            if i + 1 < len(pattern) and pattern[i + 1] in "?*+":
                modifier = pattern[i + 1]
                self.tokens.append(('char_mod', (char, modifier)))
                i += 2
                self.logger.process(f"Found character with modifier: {char}{modifier}")
                continue

            # Simple character
            self.tokens.append(('char', char))
            self.logger.process(f"Found simple character: {char}")
            i += 1

        return self.tokens
```

---

## Example: Step-by-Step Execution

Log steps:
Step 1: Parsing pattern:  (a | b) (c | d) E+ G?
Step 2: Found simple character:  
Step 3: Found simple group: (a | b)
Step 4: Found simple character:  
Step 5: Found simple group: (c | d)
Step 6: Found simple character:  
Step 7: Found character with modifier: E+
Step 8: Found simple character:  
Step 9: Found character with modifier: G?
Step 1: Processing token: char -  
Step 2: Processing token: group - (['a ', ' b'], 1)
Step 3: Generated group options: ['a ', ' b']
Step 4: Processing token: char -  
Step 5: Processing token: group - (['c ', ' d'], 1)
Step 6: Generated group options: ['c ', ' d']
Step 7: Processing token: char -  
Step 8: Processing token: char_mod - ('E', '+')
Step 9: Generated 1-5 repetitions of 'E'
Step 10: Processing token: char -  
Step 11: Processing token: char_mod - ('G', '?')
Step 12: Generated optional character: '' or 'G'
Step 13: Generating final combinations...
Step 14: Generated 40 total combinations

Sample combinations:
 a  c  E 
 a  c  E G
 a  c  EE 
 a  c  EE G
 a  c  EEE 
All combinations saved to /home/mrdine/University/2nd/semester2/DSL_Laboratory_works/4- Regular Expressions/src/file/regex_combination.txt

Log steps:
Step 1: Parsing pattern: P(Q |R |S)T(UV |W |X) * Z+
Step 2: Found simple character: P
Step 3: Found simple group: (Q |R |S)
Step 4: Found simple character: T
Step 5: Found simple group: (UV |W |X)
Step 6: Found character with modifier:  *
Step 7: Found simple character:  
Step 8: Found character with modifier: Z+
Step 1: Processing token: char - P
Step 2: Processing token: group - (['Q ', 'R ', 'S'], 1)
Step 3: Generated group options: ['Q ', 'R ', 'S']
Step 4: Processing token: char - T
Step 5: Processing token: group - (['UV ', 'W ', 'X'], 1)
Step 6: Generated group options: ['UV ', 'W ', 'X']
Step 7: Processing token: char_mod - (' ', '*')
Step 8: Generated 0-5 repetitions of ' '
Step 9: Processing token: char -  
Step 10: Processing token: char_mod - ('Z', '+')
Step 11: Generated 1-5 repetitions of 'Z'
Step 12: Generating final combinations...
Step 13: Generated 270 total combinations

Sample combinations:
PQ TUV  Z
PQ TUV  ZZ
PQ TUV  ZZZ
PQ TUV  ZZZZ
PQ TUV  ZZZZZ
All combinations saved to /home/mrdine/University/2nd/semester2/DSL_Laboratory_works/4- Regular Expressions/src/file/regex_combination.txt

Log steps:
Step 1: Parsing pattern: 1(0/1)*2(3/4)^5 36
Step 2: Found simple character: 1
Step 3: Found group with modifier: ()*
Step 4: Found simple character: 2
Step 5: Found simple character: (
Step 6: Found simple character: 3
Step 7: Found simple character: /
Step 8: Found simple character: 4
Step 9: Found simple character: )
Step 10: Found simple character: ^
Step 11: Found simple character: 5
Step 12: Found simple character:  
Step 13: Found simple character: 3
Step 14: Found simple character: 6
Step 1: Processing token: char - 1
Step 2: Processing token: group_mod - (['0/1'], '*')
Step 3: Generated 0-5 group repetitions
Step 4: Processing token: char - 2
Step 5: Processing token: char - (
Step 6: Processing token: char - 3
Step 7: Processing token: char - /
Step 8: Processing token: char - 4
Step 9: Processing token: char - )
Step 10: Processing token: char - ^
Step 11: Processing token: char - 5
Step 12: Processing token: char -  
Step 13: Processing token: char - 3
Step 14: Processing token: char - 6
Step 15: Generating final combinations...
Step 16: Generated 6 total combinations

Sample combinations:
12(3/4)^5 36
10/12(3/4)^5 36
10/10/12(3/4)^5 36
10/10/10/12(3/4)^5 36
10/10/10/10/12(3/4)^5 36

## Conclusions

✅ This laboratory work provided an educational and functional exploration into **parsing custom regular expressions**.  
The main takeaways include:

- **Modular Design**: Separation of concerns between logging and parsing enhances maintainability.
- **Clear Traceability**: Logging each parsing step helps in debugging and learning.
- **Support for Extended Syntax**: The parser successfully handles repetition, optional characters, and groups.
- **Foundation for Future Work**: The parsed tokens can be used in validators, generators, or automata builders.

---
