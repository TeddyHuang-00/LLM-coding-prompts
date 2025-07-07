# {{PROJECT_NAME}}_cli

Command-line interface for {{PROJECT_NAME}}.

## Installation

```bash
cargo install --path .
```

## Usage

### Initialize a Project

```bash
{{PROJECT_NAME}} init --name my_new_project
```

### Run the Application

```bash
# Run with default settings
{{PROJECT_NAME}} run

# Run with input file
{{PROJECT_NAME}} run --input data.txt

# Enable debug mode
{{PROJECT_NAME}} --debug run
```

### Check Status

```bash
{{PROJECT_NAME}} status
```

## Options

### Global Options

- `--debug, -d`: Enable debug mode
- `--config, -c <FILE>`: Specify configuration file
- `--help, -h`: Show help information
- `--version, -V`: Show version information

### Commands

- `init`: Initialize a new project
  - `--name, -n <NAME>`: Project name
- `run`: Run the main application
  - `--input, -i <FILE>`: Input file path
- `status`: Show project status