# Milton: Developer Documentation
* [Environment Setup](#environment-setup)

## Environment Setup
**Step 1.** Clone the repository.
```bash
git clone https://github.com/cyberphor/milton.git
```

**Step 2.** Create a Python virtual environment.
```bash
python -m venv .venv
```

**Step 3.** Activate the Python virtual environment you just created.
```bash
source .venv/bin/activate
``` 

**Step 4.** Install Poetry in your Python virtual environment.
```bash
pip install poetry
```

**Step 5.** Use Poetry to install Milton.
```bash
poetry install
```

**Step 6.** Set your environment variables in a file called `.env`,
```bash
echo "export OPENAI_API_KEY=..." > .env
```

**Step 7.** Add the environment variables you set in the `.env` file to your shell environment using `source`.
```bash
source .env
```

**Step 7.** Run Milton.
```bash
streamlit run milton/main.py
```
