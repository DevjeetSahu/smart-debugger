
# Smart Debugger

Smart Debugger is a CLI-based tool that simplifies the debugging process using LLMs. It reads stack traces, fetches code context from the source code, and generates helpful suggestions using an LLM (e.g., Perplexity AI).

## Current Workflow

1. **Accept stack trace + codebase directory**
2. **Parse stack trace → file + line**
3. **Read code + gather context**
4. **Generate and send prompt to LLM**
5. **Display suggestion via terminal**

---

## Features

- Takes in a JavaScript/React stack trace from a `.txt` file
- Parses the trace using regex to extract filenames and line numbers
- Gathers code context (±5 lines) from the error site in the codebase
- Sends the error + context to an LLM (Perplexity AI)
- Displays the LLM's suggestions in the terminal

---

## Setup

1. Place your test codebase inside the root directory (e.g., `./codebase`).
2. Save your stack trace in a `.txt` file (e.g., `error_logs/sample_error.txt`).
3. Make sure your `.env` file contains the Perplexity API key:

```
PERPLEXITY_API_KEY=your_api_key_here
```
## 🛠️ Install Requirements

Make sure you have Python installed. Then install the required dependencies using:

```bash
pip install -r requirements.txt
```
## 🚀 Run the Smart Debugger

You can run the tool using:

```bash
python main.py --log error_logs/sample_error.txt --codebase ./tenzies
```
---

## Future Improvements

- 🌍 Support for more languages (Python, Java, C++, etc.)
- 💻 Web UI or IDE extension (especially for VS Code)
- 🔧 Auto-fix mode to apply changes with a button click
- 🔗 Clickable links in terminal to open file and line in editor
- 🤖 Multiple LLM suggestions handling and display

---

## Note

Currently, the stack trace parsing technique is **language-specific** (JavaScript) and may fail for others. The code context fetches ±5 lines around the error, but it can be extended to fetch full functions or files.

---

## License

MIT
