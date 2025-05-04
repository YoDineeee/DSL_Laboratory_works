from regex_parser import RegexParser
from regex_generator import RegexGenerator

patterns = [
   " (a | b) (c | d) E+ G?",
 "P(Q |R |S)T(UV |W |X) * Z+",
 "1(0/1)*2(3/4)^5 36"
]

parser = RegexParser()
generator = RegexGenerator()

file_path = "/home/mrdine/University/2nd/semester2/DSL_Laboratory_works/4- Regular Expressions/src/file/regex_combination.txt"
with open(file_path, "a") as f:
    for pattern in patterns:
        tokens = parser.parse(pattern)
        results = generator.generate(tokens)

        # Write the pattern and the combinations
        f.write(f"Pattern: {pattern}\n")
        for combo in results:
            f.write(combo + "\n")

        # Show log steps
        print("\nLog steps:")
        parser.logger.show_steps()
        generator.logger.show_steps()

        print("\nSample combinations:")
        for sample in results[:5]:
            print(sample)

        print(f"All combinations saved to {file_path}")