import argparse
import subprocess

from openai import OpenAI

parser = argparse.ArgumentParser(description="Explain the meaning of a symbol in code")
parser.add_argument("name", type=str, help="The symbol to search for")
parser.add_argument(
    "-s",
    "--searcher",
    type=str,
    default="rg",
    help="The searcher tool to use (default: 'rg')",
)
args = parser.parse_args()
name = args.name

command = [args.searcher, "-C", "10", args.name]
result = subprocess.run(command, capture_output=True, text=True, check=True)
print("ripgrep output:\n", result.stdout)
