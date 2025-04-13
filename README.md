# DevChat

DevChat is an AI-powered coding assistant that helps developers write better code through intelligent workflows and chat-based interactions.

## Project Structure

```
devchat/
├── src/                    # Main source code
├── tests/                  # Test files
├── examples/              # Example workflows and usage
├── scripts/               # Utility scripts
├── workflow/             # Workflow definitions
├── .github/              # GitHub Actions workflows
├── pyproject.toml        # Project dependencies (Poetry)
├── poetry.lock          # Lock file for dependencies
└── README.md            # Project documentation
```

## Features

- **Code Analysis**: Analyze Python code for complexity, style, and maintainability
- **AI-Powered Assistance**: Get help with coding questions and problems
- **Test Generation**: Automatically generate unit tests for your code
- **Workflow Automation**: Create and run custom coding workflows
- **Configuration Management**: Easy setup and customization

## Installation

1. Install Poetry if you haven't already:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Clone the repository:
```bash
git clone https://github.com/yourusername/devchat.git
cd devchat
```

3. Install dependencies:
```bash
poetry install
```

## Quick Start

1. Set up your configuration:
```bash
poetry run devchat config setup
```

2. Analyze a Python file:
```bash
poetry run devchat assist analyze path/to/your/file.py
```

3. Ask a coding question:
```bash
poetry run devchat assist ask "How do I implement a binary search in Python?"
```

4. Generate tests for a file:
```bash
poetry run devchat assist generate-tests path/to/your/file.py --output tests/test_file.py
```

## Workflows

DevChat supports custom workflows for automating coding tasks. Here's how to use them:

1. Create a workflow:
```bash
poetry run devchat workflow create my_workflow --steps examples/refactor_workflow.yaml
```

2. List available workflows:
```bash
poetry run devchat workflow list
```

3. Run a workflow:
```bash
poetry run devchat workflow run my_workflow --file path/to/your/file.py
```

## Configuration

Manage your DevChat configuration:

1. Set a configuration value:
```bash
poetry run devchat config set model gpt-4
```

2. Get a configuration value:
```bash
poetry run devchat config get model
```

3. List all configuration:
```bash
poetry run devchat config list
```

## Examples

### Code Analysis
```bash
poetry run devchat assist analyze src/example.py
```

### Test Generation
```bash
poetry run devchat assist generate-tests src/example.py --output tests/test_example.py
```

### Custom Workflow
```bash
# Create workflow
poetry run devchat workflow create refactor --steps examples/refactor_workflow.yaml

# Run workflow
poetry run devchat workflow run refactor --file src/example.py
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
