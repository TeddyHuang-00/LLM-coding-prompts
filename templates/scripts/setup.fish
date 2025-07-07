#!/usr/bin/env fish

# Development Template Setup Script
# Interactive onboarding with gum for beautiful terminal UI

set -l SCRIPT_DIR (dirname (realpath (status current-filename)))
set -l TEMPLATES_DIR (dirname $SCRIPT_DIR)
set -l PROMPTS_DIR "$TEMPLATES_DIR/prompts"

# Color scheme
set -l PRIMARY_COLOR "#7C3AED"
set -l SUCCESS_COLOR "#10B981"
set -l WARNING_COLOR "#F59E0B"
set -l ERROR_COLOR "#EF4444"

function banner
    gum style \
        --foreground $PRIMARY_COLOR \
        --border-foreground $PRIMARY_COLOR \
        --border double \
        --align center \
        --width 60 \
        --margin "1 0" \
        "🚀 Development Template Setup" \
        "" \
        "Modern project templates with AI prompts"
end

function info
    gum style --foreground $PRIMARY_COLOR "ℹ️  $argv"
end

function success
    gum style --foreground $SUCCESS_COLOR "✅ $argv"
end

function warning
    gum style --foreground $WARNING_COLOR "⚠️  $argv"
end

function error
    gum style --foreground $ERROR_COLOR "❌ $argv"
end

function check_dependencies
    info "Checking dependencies..."
    
    set -l missing_deps
    
    # Check for required tools
    if not command -v gum >/dev/null 2>&1
        set -a missing_deps "gum (https://github.com/charmbracelet/gum)"
    end
    
    if not command -v python3 >/dev/null 2>&1
        set -a missing_deps "python3"
    end
    
    if test (count $missing_deps) -gt 0
        error "Missing required dependencies:"
        for dep in $missing_deps
            echo "  - $dep"
        end
        echo ""
        echo "Please install missing dependencies and try again."
        exit 1
    end
    
    success "All dependencies found"
end

function select_language
    info "Select your programming language:"
    
    # Only show Python and Rust
    set -l languages "Python" "Rust"
    
    # Verify the configuration files exist
    for lang in $languages
        set -l lang_file "$PROMPTS_DIR/"(string lower $lang)".toml"
        if not test -f $lang_file
            error "Language configuration not found: $lang_file"
            exit 1
        end
    end
    
    gum choose $languages
end

function get_project_info
    set -l project_name (gum input --placeholder "Enter project name" --prompt "Project name: ")
    if test -z "$project_name"
        error "Project name is required"
        exit 1
    end
    
    set -l author_name (gum input --placeholder "Enter your name" --prompt "Author name: " --value (git config user.name 2>/dev/null; or echo ""))
    if test -z "$author_name"
        warning "Author name not provided"
        set author_name "Your Name"
    end
    
    set -l author_email (gum input --placeholder "Enter your email" --prompt "Author email: " --value (git config user.email 2>/dev/null; or echo ""))
    if test -z "$author_email"
        warning "Author email not provided"
        set author_email "your.email@example.com"
    end
    
    echo "$project_name|$author_name|$author_email"
end

function select_ai_providers
    info "Select AI coding assistants to configure:"
    
    gum choose --no-limit \
        "GitHub Copilot" \
        "Cursor (Legacy)" \
        "Cursor (Modern)" \
        "Gemini CLI" \
        "Claude Code"
end

function select_vcs
    info "Select version control system:"
    
    gum choose "Git" "Jujutsu (jj)"
end

function confirm_setup
    argparse 'language=' 'project=' 'providers=' 'vcs=' -- $argv
    
    set -l project_info (string split "|" $_flag_project)
    set -l project_name $project_info[1]
    set -l author_name $project_info[2]
    set -l author_email $project_info[3]
    
    gum style \
        --border normal \
        --margin "1 0" \
        --padding "1 2" \
        "📋 Project Configuration Summary" \
        "" \
        "Language: $_flag_language" \
        "Project: $project_name" \
        "Author: $author_name <$author_email>" \
        "AI Providers: $_flag_providers" \
        "VCS: $_flag_vcs" \
        "" \
        "Target: "(pwd)
    
    gum confirm "Proceed with setup?"
end

function setup_project_structure
    argparse 'language=' 'project=' -- $argv
    
    set -l project_info (string split "|" $_flag_project)
    set -l project_name $project_info[1]
    set -l language (string lower $_flag_language)
    
    info "Setting up project structure..."
    
    # Copy minimal template
    set -l template_dir "$TEMPLATES_DIR/$language/minimal"
    if test -d $template_dir
        cp -r $template_dir/* .
        success "Copied $language template"
    else
        error "Template not found: $template_dir"
        exit 1
    end
    
    # Update project name in files
    update_project_files --language=$_flag_language --project=$_flag_project
end

function update_project_files
    argparse 'language=' 'project=' -- $argv
    
    set -l project_info (string split "|" $_flag_project)
    set -l project_name $project_info[1]
    set -l author_name $project_info[2]
    set -l author_email $project_info[3]
    set -l language (string lower $_flag_language)
    
    info "Updating project files..."
    
    # Update based on language
    switch $language
        case python
            if test -f pyproject.toml
                sed -i.bak "s/my-python-project/$project_name/g" pyproject.toml
                sed -i.bak "s/Your Name/$author_name/g" pyproject.toml
                sed -i.bak "s/your.email@example.com/$author_email/g" pyproject.toml
                rm pyproject.toml.bak
                success "Updated pyproject.toml"
            end
        case rust
            if test -f Cargo.toml
                sed -i.bak "s/my-rust-project/$project_name/g" Cargo.toml
                sed -i.bak "s/Your Name <your.email@example.com>/$author_name <$author_email>/g" Cargo.toml
                rm Cargo.toml.bak
                success "Updated Cargo.toml"
            end
    end
    
    # Update README
    if test -f README.md
        sed -i.bak "s/My .* Project/$project_name/g" README.md
        rm README.md.bak
        success "Updated README.md"
    end
end

function generate_ai_prompts
    argparse 'language=' 'providers=' -- $argv
    
    set -l language (string lower $_flag_language)
    set -l config_file "$PROMPTS_DIR/$language.toml"
    
    if not test -f $config_file
        error "Language configuration not found: $config_file"
        exit 1
    end
    
    info "Generating AI prompt files..."
    
    # Convert provider names to script format
    set -l provider_args
    for provider in (string split " " $_flag_providers)
        switch $provider
            case "GitHub Copilot"
                set -a provider_args "github-copilot"
            case "Cursor (Legacy)"
                set -a provider_args "cursor-legacy"
            case "Cursor (Modern)"
                set -a provider_args "cursor-modern"
            case "Gemini CLI"
                set -a provider_args "gemini"
            case "Claude Code"
                set -a provider_args "claude"
        end
    end
    
    # Generate prompts
    python3 "$SCRIPT_DIR/generate_prompts.py" $config_file --output . --providers $provider_args
    
    success "Generated AI prompt files"
end

function setup_vcs
    argparse 'vcs=' -- $argv
    
    info "Setting up version control..."
    
    switch $_flag_vcs
        case "Git"
            if not test -d .git
                git init
                success "Initialized Git repository"
            else
                info "Git repository already exists"
            end
        case "Jujutsu (jj)"
            if command -v jj >/dev/null 2>&1
                if not test -d .jj
                    jj init --git
                    success "Initialized Jujutsu repository"
                else
                    info "Jujutsu repository already exists"
                end
            else
                warning "Jujutsu (jj) not found, skipping VCS setup"
            end
    end
end

function setup_gitignore
    argparse 'language=' 'vcs=' -- $argv
    
    if test "$_flag_vcs" = "Git"
        if not test -f .gitignore
            warning "No .gitignore found (should have been copied from template)"
        end
    end
end

function show_next_steps
    argparse 'language=' 'project=' 'vcs=' -- $argv
    
    set -l project_info (string split "|" $_flag_project)
    set -l project_name $project_info[1]
    set -l language (string lower $_flag_language)
    
    gum style \
        --border normal \
        --border-foreground $SUCCESS_COLOR \
        --margin "1 0" \
        --padding "1 2" \
        "🎉 Setup Complete!" \
        "" \
        "Your $language project '$project_name' is ready!" \
        "" \
        "Next steps:"
    
    # Language-specific next steps
    switch $language
        case python
            echo "  1. Create virtual environment: python -m venv .venv"
            echo "  2. Activate environment: source .venv/bin/activate"
            echo "  3. Install dependencies: pip install -e '.[dev]'"
            echo "  4. Run quality checks: ruff format && ruff check && mypy src/ && pytest"
        case rust
            echo "  1. Build project: cargo build"
            echo "  2. Run tests: cargo test"
            echo "  3. Format code: cargo fmt"
            echo "  4. Run lints: cargo clippy --all-targets --all-features -- -D warnings"
    end
    
    echo ""
    echo "  🤖 Your AI coding assistants are configured and ready!"
    echo "  📚 Check the generated prompt files for AI-specific settings"
    
    if test "$_flag_vcs" != "None"
        echo "  📝 Consider making your first commit"
    end
end

function main
    banner
    
    # Check dependencies
    check_dependencies
    
    # Get user preferences
    set -l language (select_language)
    if test -z "$language"
        error "Language selection cancelled"
        exit 1
    end
    
    set -l project_info (get_project_info)
    set -l ai_providers (select_ai_providers)
    if test -z "$ai_providers"
        warning "No AI providers selected"
        set ai_providers ""
    end
    
    set -l vcs (select_vcs)
    if test -z "$vcs"
        error "VCS selection cancelled"
        exit 1
    end
    
    # Confirm setup
    if not confirm_setup --language="$language" --project="$project_info" --providers="$ai_providers" --vcs="$vcs"
        info "Setup cancelled"
        exit 0
    end
    
    # Perform setup
    setup_project_structure --language="$language" --project="$project_info"
    
    if test -n "$ai_providers"
        generate_ai_prompts --language="$language" --providers="$ai_providers"
    end
    
    setup_vcs --vcs="$vcs"
    setup_gitignore --language="$language" --vcs="$vcs"
    
    # Show completion message
    show_next_steps --language="$language" --project="$project_info" --vcs="$vcs"
end

# Run main function
main $argv