#!/usr/bin/env fish

# Modern Project Setup Script
# Uses Fish shell and cat templating with gum for interactions

set PROMPTS_SRC_DIR prompts
set TEMPLATES_DIR templates

# Colors for output
set PRIMARY_COLOR 6
set INFO_COLOR 4
set SUCCESS_COLOR 2
set WARNING_COLOR 3
set ERROR_COLOR 1

set LANGUAGE
set TEMPLATE
set PROJECT_NAME
set PROJECT_PATH
set VCS_NAME
set AUTHOR_NAME "Your Name"
set AUTHOR_EMAIL "your.email@example.com"
set GITHUB_NAME your-github-username
set AI_PROVIDERS

function banner
    gum style \
        --border-foreground $PRIMARY_COLOR \
        --border double \
        --align center \
        --width 60 \
        --margin "1 0" \
        $argv
end

function info
    gum style --foreground $INFO_COLOR "ℹ️  $argv"
end

function warning
    gum style --foreground $WARNING_COLOR "⚠️  $argv"
end

function error
    gum style --foreground $ERROR_COLOR "❌ $argv"
end

function success
    gum style --foreground $SUCCESS_COLOR "✅ $argv"
end

function check_dependencies
    set missing_deps

    if not type -q gum
        set -a missing_deps "gum (https://github.com/charmbracelet/gum)"
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
    set languages
    for lang_file in $PROMPTS_SRC_DIR/*.md
        set lang_name (basename $lang_file .md)
        if test "$lang_name" != general
            set -a languages $lang_name
        end
    end

    if test (count $languages) -eq 0
        error "No language files found in $PROMPTS_SRC_DIR"
        exit 1
    end

    set LANGUAGE (gum choose $languages --header "Select programming language:")
    info "Language: $LANGUAGE"
end

function select_template
    set template_dir "$TEMPLATES_DIR/$LANGUAGE"
    if not test -d "$template_dir"
        error "No templates found for $LANGUAGE"
        exit 1
    end

    set templates
    for template_path in $template_dir/*
        if test -d "$template_path"
            set -a templates (basename $template_path)
        end
    end

    if test (count $templates) -eq 0
        error "No templates found in $template_dir"
        exit 1
    end

    set TEMPLATE (gum choose $templates --header "Select project template:")
    info "Template: $TEMPLATE"
end

function get_project_info
    set PROJECT_NAME (gum input --placeholder "Enter project name" --prompt "Project name: ")
    if test -z "$PROJECT_NAME"
        error "Project name is required"
        exit 1
    end

    set PROJECT_PATH (gum input --placeholder "Enter project path (default: current directory)" --prompt "Project path: ")
    set PROJECT_PATH (string trim $PROJECT_PATH | path normalize)
    if test -z "$PROJECT_PATH"
        set PROJECT_PATH "$(pwd)/new_project"
    end

    if test -d "$PROJECT_PATH"
        warning "Directory '$PROJECT_PATH' already exists."
        if not gum confirm "Remove existing directory and create a new one?"
            error "Directory already exists: $PROJECT_PATH"
            exit 1
        end
    end

    info "Project name: $PROJECT_NAME"
    info "Project path: $PROJECT_PATH"
end

function select_ai_providers
    set providers "GitHub Copilot:copilot" "Cursor:cursor" "Gemini CLI:gemini" "Claude Code:claude"

    set selected (gum choose --no-limit $providers --header "Select AI coding assistants:" --label-delimiter ":")
    if test -z "$selected"
        warning "No AI providers selected"
    else
        set AI_PROVIDERS $selected
        info "Selected AI providers: $(string join ", " $AI_PROVIDERS)"
    end
end

function get_vcs_info
    set vcs_options "Git:git" "Jujutsu:jj" "None:"
    set VCS_NAME (gum choose $vcs_options --header "Select version control system (VCS):" --label-delimiter ":")

    if test -z "$VCS_NAME"
        warning "No VCS selected, proceeding without version control"
    else if not type -q "$VCS_NAME"
        error "'$VCS_NAME' is not installed or recognized. Please install it or choose another VCS."
        exit 1
    else
        set config_name
        set config_email
        if test "$VCS_NAME" = git
            set config_name (git config user.name 2>/dev/null; or echo "")
            set config_email (git config user.email 2>/dev/null; or echo "")
        else if test "$VCS_NAME" = jj
            set config_name (jj config g user.name 2>/dev/null; or echo "")
            set config_email (jj config g user.email 2>/dev/null; or echo "")
        else
            error "Unsupported VCS: $VCS_NAME"
            exit 1
        end

        set AUTHOR_NAME (gum input --placeholder "Enter your name" --prompt "Author name: " --value "$config_name")
        if test -z "$AUTHOR_NAME"
            set AUTHOR_NAME "Your Name"
        end

        set AUTHOR_EMAIL (gum input --placeholder "Enter your email" --prompt "Author email: " --value "$config_email")
        if test -z "$AUTHOR_EMAIL"
            set AUTHOR_EMAIL "your.email@example.com"
        end

        info "VCS: $VCS_NAME"
        info "Author: $AUTHOR_NAME <$AUTHOR_EMAIL>"
    end
end

function copy_template
    set template_path "$TEMPLATES_DIR/$LANGUAGE/$TEMPLATE"

    info "Copying template files..."

    if not test -d "$template_path"
        error "Template not found: $template_path"
        exit 1
    end

    # Copy template files
    mkdir -p (path dirname "$PROJECT_PATH")
    rm -rf "$PROJECT_PATH"
    cp -r "$template_path" "$PROJECT_PATH"
    success "Template files copied"

    # Update template placeholders using sed
    for file in (find "$PROJECT_PATH" -type f -name "*.toml" -o -name "*.md" -o -name "*.py" -o -name "*.rs")
        if test -f "$file"
            sed -i.bak "s/{{PROJECT_NAME}}/$PROJECT_NAME/g" "$file"
            sed -i.bak "s/{{AUTHOR_NAME}}/$AUTHOR_NAME/g" "$file"
            sed -i.bak "s/{{AUTHOR_EMAIL}}/$AUTHOR_EMAIL/g" "$file"
            rm "$file.bak"
        end
    end

    success "Project files updated"
end

function generate_claude
    # Create CLAUDE.md with header
    set file_path "$PROJECT_PATH/CLAUDE.md"

    # Append general rules
    cat $PROMPTS_SRC_DIR/general.md >>$file_path
    echo "" >>$file_path

    # Append language-specific rules
    cat $PROMPTS_SRC_DIR/$LANGUAGE.md >>$file_path
end

function generate_gemini
    set file_path "$PROJECT_PATH/GEMINI.md"

    # Append general rules
    cat $PROMPTS_SRC_DIR/general.md >>$file_path
    echo "" >>$file_path

    # Append language-specific rules
    cat $PROMPTS_SRC_DIR/$LANGUAGE.md >>$file_path
end

function generate_cursor
    set dir_path "$PROJECT_PATH/.cursor/rules"
    mkdir -p $dir_path
    set general_path "$dir_path/general.mdc"
    set language_path "$dir_path/$LANGUAGE.mdc"

    # Cursor specific conditional application rule
    set globs
    switch $LANGUAGE
        case python
            set -a globs "*.py" "pyproject.toml"
        case rust
            set -a globs "*.rs" "Cargo.toml"
        case *
            warning "No specific globs defined for $LANGUAGE, setting to always apply"
    end

    # Create header for general rules
    echo --- >>$general_path
    echo "description: General development rules with modern tooling" >>$general_path
    echo "alwaysApply: true" >>$general_path
    echo --- >>$general_path
    echo "" >>$general_path

    # Append general rules
    cat $PROMPTS_SRC_DIR/general.md >>$general_path

    # Create header for language-specific rules
    echo --- >>$language_path
    echo "description: $LANGUAGE development rules" >>$language_path
    if test -n "$globs"
        echo "globs: $(string join "," $globs)" >>$language_path
        echo "alwaysApply: false" >>$language_path
    else
        echo "alwaysApply: true" >>$language_path
    end
    echo --- >>$language_path
    echo "" >>$language_path

    # Append language-specific rules
    cat $PROMPTS_SRC_DIR/$LANGUAGE.md >>$language_path

end

function generate_copilot
    set dir_path "$PROJECT_PATH/.github"
    mkdir -p $dir_path
    set file_path "$dir_path/copilot-instructions.md"

    # Append general rules
    cat $PROMPTS_SRC_DIR/general.md >>$file_path
    echo "" >>$file_path

    # Append language-specific rules
    cat $PROMPTS_SRC_DIR/$LANGUAGE.md >>$file_path
end

function generate_ai_prompts
    for provider in $AI_PROVIDERS
        switch $provider
            case copilot
                generate_copilot
            case cursor
                generate_cursor
            case gemini
                generate_gemini
            case claude
                generate_claude
        end
    end
end

function initialize_vcs
    switch $VCS_NAME
        case git
            git init $PROJECT_PATH
        case jj
            jj git init $PROJECT_PATH
    end
end

function show_next_steps
    set message
    set -a message "🎉 Setup Complete!" ""
    set -a message "Your $LANGUAGE project '$PROJECT_NAME' is ready!" ""
    set -a message "Next steps:"
    set -a message "1. Review the generated AI prompt files"
    set -a message "2. Customize prompts for your specific needs"
    set -a message "3. Start coding with AI assistance!"
    banner $message
end

function main
    banner "🚀 Modern Project Setup" "" "Fish shell + Cat templating + AI prompts"

    # Check dependencies
    check_dependencies

    # Get user preferences
    select_language
    if test -z "$LANGUAGE"
        error "Language selection cancelled"
        exit 1
    end

    select_template
    if test -z "$TEMPLATE"
        error "Template selection cancelled"
        exit 1
    end

    get_project_info
    get_vcs_info
    select_ai_providers

    # Confirm setup
    if not gum confirm "Proceed with setup?"
        info "Setup cancelled"
        exit 0
    end

    # Perform setup
    copy_template
    generate_ai_prompts
    initialize_vcs

    # Show completion message
    show_next_steps
end

# Run main function
main $argv
