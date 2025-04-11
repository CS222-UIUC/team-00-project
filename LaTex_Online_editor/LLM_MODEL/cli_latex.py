from model import get_latex
from tqdm import tqdm

history = []


def generate_latex_with_progress(user_input):
    print("Generating:", end=" ", flush=True)
    output = ""
    for _ in tqdm(range(30), ncols=75, desc="Progress"):
        output = get_latex(user_input)  # call local model
    return output


def cli_loop():
    print("🧮 LaTeX CLI | Type `quit()` to exit, `!history` to show last 10 results.\n")
    while True:
        user_input = input(">> ").strip()
        if user_input == "quit()":
            break
        elif user_input == "!history":
            print("\n📜 History (latest 10):")
            for i, h in enumerate(history[-10:], 1):
                print(f"{i}: {h}")
            print()
        elif user_input:
            latex = generate_latex_with_progress(user_input)
            print("\n📤 Output:\n" + latex + "\n")
            history.append(latex)


if __name__ == "__main__":
    cli_loop()
