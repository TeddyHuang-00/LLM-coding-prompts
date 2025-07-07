# Development Templates with AI Prompt Files

This directory contains development templates for various programming languages, each with minimal project structure and comprehensive AI prompt files for different coding assistants.

## Structure

Each language template includes:
- **minimal/**: Basic project structure with essential files
- **ai-prompts/**: Prompt files for different AI coding assistants

## Supported Languages

- **Python**: Modern Python development with Ruff and Pydantic-Settings
- **Rust**: Enhanced Rust development with modern tooling
- **JavaScript**: Node.js/Browser development
- **TypeScript**: Type-safe JavaScript development
- **Go**: Go programming language
- **Java**: Java development
- **C#**: .NET development

## AI Providers Supported

Each template includes prompt files for:
- **GitHub Copilot**: `.github/copilot-instructions.md`
- **Cursor**: `.cursorrules` (legacy) and `.cursor/rules/*.mdc` (modern)
- **Gemini CLI**: `GEMINI.md`
- **Claude Code**: `CLAUDE.md`

## Usage

1. Copy the desired language template to your project directory
2. Copy the AI prompt files that match your preferred coding assistant
3. Customize the prompt files according to your project needs
4. Remove unused AI prompt files to avoid conflicts

## Quick Start

```bash
# Copy Python template
cp -r templates/python/minimal/* /path/to/your/project/
cp -r templates/python/ai-prompts/* /path/to/your/project/

# Copy Rust template
cp -r templates/rust/minimal/* /path/to/your/project/
cp -r templates/rust/ai-prompts/* /path/to/your/project/
```

## Customization

Each AI prompt file is designed to be:
- **Language-specific**: Tailored to the programming language's best practices
- **Comprehensive**: Covers coding style, tooling, and project structure
- **Modular**: Easy to customize for specific project needs
- **Team-friendly**: Suitable for version control and team collaboration

## Best Practices

- Keep prompt files in version control for team consistency
- Customize prompts to match your project's specific needs
- Use only the AI prompt files for your preferred coding assistant
- Regularly update prompt files as your project evolves