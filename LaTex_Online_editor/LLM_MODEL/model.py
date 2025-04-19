import re
import llama_cpp
from llama_cpp import Llama

model_Janus = r"E:\cs222\Janus-Pro-7B-LM.Q6_K.gguf"  # local path
model_deepseek_r1 = r"E:\cs222\DeepSeek-R1-q5_k_m.gguf"  # local path
model_deepseek_math = r"E:\cs222\deepseek-math-7b-base-q8_0.gguf"
llm = Llama(
    model_path=model_deepseek_math, n_ctx=4096, n_threads=16, n_gpu_layers=30, verbose=False
)


def build_prompt_latex(user_input: str) -> str:
    return f"""### Instruction:
Convert the following math expression into LaTeX format only.
Do not add any explanation or formatting.
### Input:
{user_input}

### Output:
"""

def clean_latex_output(raw_output: str) -> str:
    cleaned = re.sub(r'^\${1,2}\s*|\s*\${1,2}$', '', raw_output.strip())
    cleaned = re.sub(r'["`]{2,}|\\n+$', '', cleaned).strip()

    return cleaned


def get_latex(user_input: str) -> str:
    prompt = build_prompt_latex(user_input)
    response = llm(
        prompt,
        max_tokens=1200,
        temperature=0,            #for deterministic output for math
        repeat_penalty=1.0,       #natural language  
        top_k=0,                  #no sampling only choosing the top token 
        top_p=1.0,                #include all tokens
        stop=["###", '"""'],
    )
    output = clean_latex_output(response['choices'][0]['text'])
    return output

