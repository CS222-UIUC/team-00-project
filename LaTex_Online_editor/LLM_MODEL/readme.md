```bash
pip install llama-cpp-python  # If you want to use CUDA, check GitHub for instructions.
```

### Library
[model_deepseek_math](https://huggingface.co/Theta-Lev/deepseek-math-7b-base-Q8_0-GGUF)

### Commands
- Start the local model server:
    ```bash
    uvicorn api_server:app --reload --port 7000
    ```

- Run the model functioning test:
    ```bash
    node test_api.js
    ```

- Use the CLI-based LaTeX converter:
    ```bash
    python cli_latex.py
    ```

- Run test all coverage : coverage run -m pytest test_api_server.py -p no:warnings 

- See reports : coverage report -m
