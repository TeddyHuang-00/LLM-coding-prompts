# Usage Example

This demonstrates how to use the enhanced template system.

## Interactive Setup (Recommended)

```bash
# Navigate to templates directory
cd templates

# Run interactive setup
./scripts/setup.fish
```

The script will guide you through:
1. **Language Selection**: Choose between Python and Rust
2. **Project Details**: Enter name, author, email
3. **AI Providers**: Select which coding assistants to configure
4. **Version Control**: Choose Git or Jujutsu (jj)
5. **Confirmation**: Review and confirm setup

## Manual Usage Examples

### Python Project

```bash
# Create new directory for your project
mkdir my-python-app && cd my-python-app

# Copy Python template
cp -r ../templates/python/minimal/* .

# Generate AI prompts for specific providers
python3 ../templates/scripts/generate_prompts.py \
  ../templates/prompts/python.toml \
  --providers claude cursor-modern

# Customize project files
sed -i 's/my-python-project/my-python-app/g' pyproject.toml
```

### Rust Project

```bash
# Create new directory
mkdir my-rust-cli && cd my-rust-cli

# Copy Rust template
cp -r ../templates/rust/minimal/* .

# Generate all AI prompts
python3 ../templates/scripts/generate_prompts.py \
  ../templates/prompts/rust.toml

# Update project name
sed -i 's/my-rust-project/my-rust-cli/g' Cargo.toml
```

### Generate Prompts Only

```bash
# For existing Python project
python3 scripts/generate_prompts.py \
  prompts/python.toml \
  --output /path/to/existing/project \
  --providers github-copilot gemini

# For existing Rust project with specific providers
python3 scripts/generate_prompts.py \
  prompts/rust.toml \
  --output . \
  --providers cursor-legacy claude
```

## Generated File Structure

After running the setup, you'll have:

```
my-project/
├── src/                        # Source code
├── tests/                      # Tests (if applicable)
├── pyproject.toml             # Python config
├── Cargo.toml                 # Rust config
├── .gitignore                 # VCS ignore file
├── README.md                  # Project documentation
├── .github/
│   └── copilot-instructions.md # GitHub Copilot prompts
├── .cursorrules               # Cursor legacy prompts
├── .cursor/
│   └── rules/
│       └── {language}.mdc     # Cursor modern prompts
├── GEMINI.md                  # Gemini CLI prompts
└── CLAUDE.md                  # Claude Code prompts
```

## Next Steps After Setup

### Python
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
ruff format && ruff check && mypy src/ && pytest
```

### Rust
```bash
cargo build
cargo test
cargo fmt
cargo clippy --all-targets --all-features -- -D warnings
```


## Customization

### Modify Prompt Templates
Edit files in `templates/prompts/` directory:
- `python.toml` - Python-specific rules
- `rust.toml` - Rust-specific rules

### Regenerate Prompts
After modifying TOML files:
```bash
python3 scripts/generate_prompts.py prompts/python.toml --output .
```

This system provides maximum flexibility while maintaining consistency across AI coding assistants!