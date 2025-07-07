# Development Templates for Python & Rust with AI Prompts

🚀 **Modern Python and Rust project templates with intelligent AI prompt generation and interactive setup**

## Features

- **📝 Single-Source Prompts**: Maintain AI prompts in TOML files, generate provider-specific formats automatically
- **🎯 Interactive Setup**: Beautiful Fish shell script with Gum for guided project initialization  
- **🤖 Multi-AI Support**: Generate prompts for GitHub Copilot, Cursor, Gemini CLI, and Claude Code
- **🔧 Modern Tooling**: Templates use latest best practices and tooling for Python and Rust
- **⚡ Dynamic Generation**: Prompts are generated on-demand with correct file paths and formats

## Quick Start

```bash
# Clone the repository
git clone <repository-url>
cd LLM-coding-prompts/templates

# Run interactive setup (requires Fish shell and Gum)
./scripts/setup.fish
```

## Requirements

- **Fish Shell**: For the interactive setup script
- **Gum**: For beautiful terminal UI (`brew install gum` or see [installation](https://github.com/charmbracelet/gum))
- **Python 3.11+**: For the prompt generation engine

## Supported Languages

| Language | Status | Template | AI Prompts |
|----------|--------|----------|------------|
| Python   | ✅     | ✅       | ✅         |
| Rust     | ✅     | ✅       | ✅         |

## AI Providers Supported

### GitHub Copilot
- **File**: `.github/copilot-instructions.md`
- **Format**: Markdown with bullet points
- **Scope**: Repository-wide instructions

### Cursor
- **Legacy**: `.cursorrules` (plain text)
- **Modern**: `.cursor/rules/{language}.mdc` (structured markdown)
- **Scope**: Project-specific rules with file pattern matching

### Gemini CLI
- **File**: `GEMINI.md`
- **Format**: Structured markdown with hierarchical organization
- **Scope**: Global, project, and local configurations

### Claude Code
- **File**: `CLAUDE.md`
- **Format**: Flexible markdown with import support
- **Scope**: Hierarchical discovery from current directory

## Architecture

```
templates/
├── scripts/
│   ├── setup.fish              # Interactive onboarding script
│   └── generate_prompts.py     # Prompt generation engine
├── prompts/
│   ├── python.toml             # Python language configuration
│   └── rust.toml               # Rust language configuration
├── python/
│   └── minimal/                # Python project template
├── rust/
│   └── minimal/                # Rust project template
└── README.md                   # This file
```

## Manual Usage

### Generate Prompts Only

```bash
# Generate all AI prompts for Python
python3 scripts/generate_prompts.py prompts/python.toml

# Generate specific providers
python3 scripts/generate_prompts.py prompts/rust.toml \
  --providers github-copilot claude

# Output to specific directory
python3 scripts/generate_prompts.py prompts/typescript.toml \
  --output /path/to/project \
  --providers cursor-modern gemini
```

### Copy Templates

```bash
# Copy Python template
cp -r python/minimal/* /path/to/your/project/

# Copy and generate prompts
cp -r rust/minimal/* /path/to/your/project/
python3 scripts/generate_prompts.py prompts/rust.toml \
  --output /path/to/your/project
```

## Interactive Setup Features

The Fish setup script provides:

- **🎨 Beautiful UI**: Colorful, intuitive interface with Gum
- **🔍 Language Selection**: Choose between Python and Rust
- **📝 Project Configuration**: Input project name, author details
- **🤖 AI Provider Selection**: Multi-select AI coding assistants to configure
- **📚 VCS Integration**: Choose between Git and Jujutsu (jj)
- **✅ Validation**: Dependency checking and error handling
- **📋 Summary**: Review configuration before proceeding
- **🎯 Next Steps**: Contextual guidance after setup

## Language-Specific Features

### Python
- **Modern Python 3.11+** with latest syntax features
- **Ruff** for ultra-fast linting and formatting (10-100x faster)
- **Pydantic Settings** for type-safe configuration
- **mypy** for strict type checking
- **pytest** for comprehensive testing

### Rust
- **Rust 2021 Edition** with modern idioms
- **Comprehensive Clippy** rules for code quality
- **async/await** patterns with Tokio
- **thiserror/anyhow** for robust error handling
- **Criterion** for benchmarking


## Customization

### Adding New Languages

1. Create `prompts/{language}.toml` with language configuration
2. Create `{language}/minimal/` template directory
3. Update setup script to include the new language in the selection list

### Modifying Prompts

Edit the TOML files in `prompts/` directory. The structure includes:

```toml
[metadata]
language = "Language Name"
version = "Version"
description = "Description"

[rules]
core = ["Rule 1", "Rule 2"]
style = ["Style rule 1", "Style rule 2"]
# ... additional categories
```

### Custom AI Providers

Extend `generate_prompts.py` to support additional AI coding assistants by adding new generator methods and output formats.

## Development

### Testing Changes

```bash
# Test prompt generation
python3 scripts/generate_prompts.py prompts/python.toml --output /tmp/test

# Test setup script in dry-run mode
fish scripts/setup.fish --help
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Add language templates or improve existing ones
4. Test with the setup script
5. Submit a pull request

## Best Practices

### For Template Maintainers

- Keep TOML configurations up-to-date with language evolution
- Test generated prompts with actual AI coding assistants
- Follow semantic versioning for breaking changes
- Document any special requirements or considerations

### For Users

- Customize generated prompts for your specific project needs
- Version control prompt files for team consistency
- Regularly update templates to get latest best practices
- Provide feedback on AI prompt effectiveness

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- **Gum** for beautiful terminal interfaces
- **Fish Shell** for powerful shell scripting
- **AI Coding Assistant** communities for prompt format specifications
- **Language communities** for best practices and tooling recommendations