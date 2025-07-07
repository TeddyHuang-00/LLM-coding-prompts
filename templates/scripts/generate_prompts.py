#!/usr/bin/env python3
"""
Prompt generation engine for AI coding assistants.
Generates provider-specific prompt files from single-source TOML configurations.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Dict, List

try:
    import tomllib
except ImportError:
    import tomli as tomllib  # Python < 3.11 fallback


class PromptGenerator:
    """Generates AI provider-specific prompt files from TOML configurations."""

    def __init__(self, config_path: Path) -> None:
        """Initialize the generator with a configuration file."""
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from TOML file."""
        try:
            with open(self.config_path, "rb") as f:
                return tomllib.load(f)
        except FileNotFoundError:
            print(f"Error: Configuration file not found: {self.config_path}")
            sys.exit(1)
        except Exception as e:
            print(f"Error loading configuration: {e}")
            sys.exit(1)

    def generate_github_copilot(self) -> str:
        """Generate GitHub Copilot instructions."""
        language = self.config["metadata"]["language"]
        version = self.config["metadata"].get("version", "")

        content = [f"# GitHub Copilot Instructions for {language} Project\n"]

        # Add version info if available
        if version:
            content.append(f"- Use {language} {version} syntax and features")

        # Add all rule categories
        for category in [
            "core",
            "style",
            "structure",
            "libraries",
            "error_handling",
            "async",
            "testing",
            "workflow",
            "modern_features",
            "performance",
            "documentation",
            "data_types",
            "memory",
            "concurrency",
        ]:
            if category in self.config.get("rules", {}):
                for rule in self.config["rules"][category]:
                    content.append(f"- {rule}")

        # Add tool-specific commands
        if "commands" in self.config:
            commands = self.config["commands"]
            content.extend(
                [
                    f"- Run `{commands.get('format', 'format-command')}` to format code",
                    f"- Run `{commands.get('lint', 'lint-command')}` to lint code",
                    f"- Run `{commands.get('test', 'test-command')}` to run tests",
                ]
            )
            if "typecheck" in commands:
                content.append(f"- Run `{commands['typecheck']}` for type checking")

        return "\n".join(content)

    def generate_cursor_legacy(self) -> str:
        """Generate legacy .cursorrules file."""
        language = self.config["metadata"]["language"]

        content = [f"# {language} Development Rules\n"]

        # Add structured sections
        sections = {
            "Language and Version": ["core"],
            "Code Style and Formatting": ["style", "quality"],
            "Project Structure": ["structure"],
            "Libraries and Dependencies": ["libraries"],
            "Data Structures": ["data_types"],
            "Error Handling": ["error_handling"],
            "Async Programming": ["async"],
            "Testing": ["testing"],
            "Code Quality": ["workflow"],
            "Documentation": ["documentation"],
            "Performance": ["performance"],
            "Memory Management": ["memory"],
            "Concurrency": ["concurrency"],
        }

        for section_name, rule_categories in sections.items():
            content.append(f"## {section_name}")
            for category in rule_categories:
                if category in self.config.get("rules", {}):
                    for rule in self.config["rules"][category]:
                        content.append(f"- {rule}")
            content.append("")

        return "\n".join(content)

    def generate_cursor_modern(self) -> str:
        """Generate modern .cursor/rules/*.mdc file."""
        language = self.config["metadata"]["language"]
        description = self.config["metadata"].get(
            "description", f"{language} development rules"
        )

        # File extensions based on language
        extensions = {
            "Python": ["*.py", "*.pyi"],
            "Rust": ["*.rs", "Cargo.toml", "Cargo.lock"],
        }

        globs = extensions.get(language, [f"*.{language.lower()}"])

        content = [
            "---",
            f"description: {description}",
            f"globs: {globs}",
            "alwaysApply: true",
            "---",
            "",
            f"# {language} Development Guidelines",
            "",
        ]

        # Add core requirements
        content.extend(
            [
                "## Core Requirements",
                "",
            ]
        )

        if "core" in self.config.get("rules", {}):
            core_rules = self.config["rules"]["core"]
            content.append(
                " ".join(core_rules[:3]) + "."
            )  # First few rules as paragraph
            content.append("")

        # Add key sections as paragraphs
        key_sections = {
            "Code Style": ["style", "quality"],
            "Essential Libraries": ["libraries"],
            "Error Handling": ["error_handling"],
            "Quality Assurance": ["workflow"],
        }

        for section_name, rule_categories in key_sections.items():
            content.append(f"## {section_name}")
            content.append("")
            rules = []
            for category in rule_categories:
                if category in self.config.get("rules", {}):
                    rules.extend(self.config["rules"][category])

            if rules:
                # Format as bullet points
                for rule in rules[:8]:  # Limit to keep concise
                    content.append(f"- {rule}")
                content.append("")

        return "\n".join(content)

    def generate_gemini(self) -> str:
        """Generate Gemini CLI configuration."""
        language = self.config["metadata"]["language"]

        content = [f"# {language} Project Configuration\n"]

        # Add structured sections
        sections = {
            "Language and Version": ["core"],
            "Tooling and Development Environment": ["workflow"],
            "Code Style Standards": ["style", "quality"],
            "Project Structure": ["structure"],
            "Required Libraries": ["libraries"],
            "Data Handling": ["data_types"],
            "Error Handling": ["error_handling"],
            "Async Programming": ["async"],
            "Testing Strategy": ["testing"],
            "Quality Assurance Workflow": ["workflow"],
            "Documentation": ["documentation"],
            "Performance Considerations": ["performance"],
            "Security Practices": [
                "performance"
            ],  # Using performance for security rules
        }

        for section_name, rule_categories in sections.items():
            content.append(f"## {section_name}")
            for category in rule_categories:
                if category in self.config.get("rules", {}):
                    for rule in self.config["rules"][category]:
                        content.append(f"- {rule}")
            content.append("")

        # Add build commands
        if "commands" in self.config:
            content.append("## Build Commands")
            for cmd_name, cmd_value in self.config["commands"].items():
                content.append(
                    f"- `{cmd_value}` - {cmd_name.title()} {language.lower()} code"
                )
            content.append("")

        return "\n".join(content)

    def generate_claude(self) -> str:
        """Generate Claude Code configuration."""
        language = self.config["metadata"]["language"]

        content = [f"# {language} Project Configuration\n"]

        # Add key sections
        sections = {
            "Language and Tooling": ["core"],
            "Code Style": ["style", "quality"],
            "Project Structure": ["structure"],
            "Libraries and Dependencies": ["libraries"],
            "Error Handling": ["error_handling"],
            "Async Programming": ["async"],
            "Testing": ["testing"],
            "Quality Assurance": ["workflow"],
            "Documentation": ["documentation"],
            "Performance and Security": ["performance"],
        }

        # Add additional sections for specific languages
        if language == "Rust":
            sections["Memory Management"] = ["memory"]

        for section_name, rule_categories in sections.items():
            content.append(f"## {section_name}")
            for category in rule_categories:
                if category in self.config.get("rules", {}):
                    for rule in self.config["rules"][category]:
                        content.append(f"- {rule}")
            content.append("")

        # Add build commands
        if "commands" in self.config:
            content.append("## Build Commands")
            for cmd_name, cmd_value in self.config["commands"].items():
                content.append(
                    f"- `{cmd_value}` - {cmd_name.title()} {language.lower()} code"
                )
            content.append("")

        return "\n".join(content)

    def generate_all(self, output_dir: Path, providers: List[str]) -> None:
        """Generate all requested prompt files."""
        output_dir.mkdir(parents=True, exist_ok=True)

        generators = {
            "github-copilot": (
                self.generate_github_copilot,
                ".github/copilot-instructions.md",
            ),
            "cursor-legacy": (self.generate_cursor_legacy, ".cursorrules"),
            "cursor-modern": (
                self.generate_cursor_modern,
                f".cursor/rules/{self.config['metadata']['language'].lower()}.mdc",
            ),
            "gemini": (self.generate_gemini, "GEMINI.md"),
            "claude": (self.generate_claude, "CLAUDE.md"),
        }

        for provider in providers:
            if provider not in generators:
                print(f"Warning: Unknown provider '{provider}', skipping")
                continue

            generator_func, filename = generators[provider]
            file_path = output_dir / filename

            # Create subdirectories if needed
            file_path.parent.mkdir(parents=True, exist_ok=True)

            try:
                content = generator_func()
                file_path.write_text(content, encoding="utf-8")
                print(f"Generated: {file_path}")
            except Exception as e:
                print(f"Error generating {provider}: {e}")


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate AI provider-specific prompt files from TOML configurations"
    )
    parser.add_argument("config", type=Path, help="Path to TOML configuration file")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path.cwd(),
        help="Output directory (default: current directory)",
    )
    parser.add_argument(
        "-p",
        "--providers",
        nargs="+",
        default=[
            "github-copilot",
            "cursor-legacy",
            "cursor-modern",
            "gemini",
            "claude",
        ],
        choices=[
            "github-copilot",
            "cursor-legacy",
            "cursor-modern",
            "gemini",
            "claude",
        ],
        help="AI providers to generate prompts for",
    )

    args = parser.parse_args()

    if not args.config.exists():
        print(f"Error: Configuration file not found: {args.config}")
        sys.exit(1)

    generator = PromptGenerator(args.config)
    generator.generate_all(args.output, args.providers)

    print(
        f"\nSuccessfully generated {len(args.providers)} prompt files in {args.output}"
    )


if __name__ == "__main__":
    main()

