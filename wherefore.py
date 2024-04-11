import argparse
import re
import subprocess
import sys

from openai import OpenAI


def extract_last_word(s):
    # Use a regular expression to find all word occurrences
    words = re.findall(r"\b\w+\b", s)
    # Return the last word, if there is any
    return words[-1] if words else None


parser = argparse.ArgumentParser(description="Explain the meaning of a symbol in code")
parser.add_argument("name", type=str, help="The symbol to search for")
parser.add_argument(
    "path", type=str, nargs="?", help="The path to search (default: current directory)"
)
parser.add_argument(
    "-C",
    "--context",
    type=int,
    default=5,
    help="The number of context lines to show around matches (default: 5)",
)
parser.add_argument(
    "-d", "--dump", action="store_true", help="Also dump the searcher output"
)
parser.add_argument(
    "-m",
    "--model",
    type=str,
    default="gpt-3.5-turbo",
    help="The GPT model (default: 'gpt-3.5-turbo')",
)
parser.add_argument(
    "-s",
    "--searcher",
    type=str,
    default="rg",
    help="The searcher tool to use (default: 'rg')",
)
args = parser.parse_args()
compound = args.name
atom = extract_last_word(compound)
if not atom:
    sys.stderr.write(compound + ": contains no word\n")
    sys.exit(1)

command = [args.searcher, "-w", "-C", str(args.context), atom]
if args.path is not None:
    command.append(args.path)
result = subprocess.run(command, capture_output=True, text=True, check=True)
if args.dump:
    print(result.stdout)

client = OpenAI()
system_prompt = "You are an expert at analyzing and explaining code."
user_prompt = f"I want to know what's up with {compound}; how is it defined, where is it used? This is a full list of occurrences of `{atom}` in the entire code base, with a few lines of context in each case:\n"
user_prompt += result.stdout
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt},
]
response = client.chat.completions.create(model=args.model, messages=messages)
r = response.choices[0].message.content
print(r)
