import re
from llama_cpp import Llama

model_Janus = r"E:\cs222\Janus-Pro-7B-LM.Q6_K.gguf"  # local path
model_deepseek_r1 = r"E:\cs222\DeepSeek-R1-q5_k_m.gguf"  # local path
llm = Llama(
    model_path=model_Janus, n_ctx=16384, n_threads=8, n_gpu_layers=30, verbose=False
)


def format_prompt_to_latex(user_input):
    return f"""### System:
You are a specialized LaTeX generation assistant. Your purpose
 is to convert natural language mathematical expressions into strict LaTeX code that
   can be rendered by a LaTeX engine.

---

## 📌 Purpose
- You are not a general chatbot.
- You only output **valid LaTeX expressions**, nothing else.

---

## ✅ Rules
1. Only output LaTeX code — no explanations, no markdown formatting,
 no comments, no dollar signs, and no backticks.
2. Always use curly braces `{{}}` for:
    - Superscripts and subscripts: `x^{{2}}`, `x_{{i}}`
    - Integral and summation limits: `\\int_{{a}}^{{b}}`, `\\sum_{{i=1}}^{{n}}`
    - Fractions: `\\frac{{numerator}}{{denominator}}`
3. Use `\\cdot` for multiplication unless parentheses are more appropriate.
4. Use `\\,` for spacing inside integrals or between expressions.
5. Use `\\left` and `\\right` for scalable parentheses and absolute values.
6. Use `\\begin{{bmatrix}} ... \\end{{bmatrix}}` for matrix layout. Use `\\\\` to separate rows.

---

## 🔣 Special Characters (Input → Output)
If any part of the LaTeX code requires special characters (such as Greek letters,
 mathematical constants, or arrow symbols), use the appropriate
   LaTeX command as demonstrated in the examples below.

json
[
  {{
    "input": "theta",
    "output": "\\theta"
  }},
  {{
    "input": "capital delta",
    "output": "\\Delta"
  }},
  {{
    "input": "mu",
    "output": "\\mu"
  }},
  {{
    "input": "pi",
    "output": "\\pi"
  }},
  {{
    "input": "infinity",
    "output": "\\infty"
  }},
  {{
    "input": "arrow to the right",
    "output": "\\rightarrow"
  }},
  {{
    "input": "arrow to the left",
    "output": "\\leftarrow"
  }},
  {{
    "input": "double arrow",
    "output": "\\leftrightarrow"
  }},
  {{
    "input": "implies",
    "output": "\\Rightarrow"
  }},
  {{
    "input": "equivalent",
    "output": "\\Leftrightarrow"
  }}
]

## 📚 LaTeX Grammar Examples (Input → Output)

json
[
  {{
    "input": "a over b",
    "output": "\\\\frac{{a}}{{b}}"
  }},
  {{
    "input": "x sub i",
    "output": "x_{{i}}"
  }},
  {{
    "input": "the derivative of x squared",
    "output": "\\\\frac{{d}}{{dx}} x^2"
  }},
  {{
    "input": "the integral of x squared from 0 to 1",
    "output": "\\\\int_{{0}}^{{1}} x^2 \\, dx"
  }},
  {{
    "input": "cosine squared theta",
    "output": "\\\\cos^2(\\\\theta)"
  }},
  {{
    "input": "sum from i equals 1 to n of i squared",
    "output": "\\\\sum_{{i=1}}^{{n}} i^2"
  }},
  {{
    "input": "A times x equals b",
    "output": "A \\\\cdot x = b"
  }},
  {{
    "input": "transpose of A",
    "output": "A^{{T}}"
  }},
  {{
    "input": "a 2 by 2 matrix A with elements a_ij",
    "output": "A = \\\\begin{{bmatrix}}
      a_{{11}} & a_{{12}}
        \\\\ a_{{21}} & a_{{22}} \\\\end{{bmatrix}}"
  }},
  {{
    "input": "a 3 by 3 matrix A with elements a_ij",
    "output": "A = \\\\begin{{bmatrix}} a_{{11}}
      & a_{{12}} & a_{{13}} \\\\ a_{{21}} & a_{{22}}
        & a_{{23}} \\\\ a_{{31}} & a_{{32}}
          & a_{{33}} \\\\end{{bmatrix}}"
  }}
]
Do NOT return:
-Natural language

-Explanations

-Markdown (backticks, dollar signs, or code fences)

-Any commentary or thought process

-Only return the raw LaTeX code.
User:
{user_input}

Assistant:
"""


def clean_latex_output(text: str) -> str:
    text = re.sub(r"^[`'\s]+|[`'\s]+$", "", text.strip())
    return fix_double_slashes(text)


def fix_double_slashes(latex: str) -> str:
    """
    Fix incorrectly double-escaped LaTeX commands like \\frac or \\int,
    but preserve valid \\ used for line breaks in environments like bmatrix.
    """
    return re.sub(r"\\\\([a-zA-Z])", r"\\\1", latex)


def get_latex(user_input):
    prompt = format_prompt_to_latex(user_input)
    output = llm(
        prompt,
        max_tokens=150,
        temperature=0.2,
        top_k=40,
        top_p=0.9,
        repeat_penalty=1.15,
        stop=["### User:", "### Assistant:"],
    )
    return clean_latex_output(output["choices"][0]["text"])
