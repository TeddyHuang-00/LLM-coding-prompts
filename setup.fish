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
set AUTHOR_NAME
set AUTHOR_EMAIL
set GITHUB_NAME
set LICENSES
set AI_PROVIDERS
set CURRENT_YEAR (date +%Y)

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

function step
    set step_name $argv[1]
    set file_path "scripts/$step_name.fish"
    source $file_path; or begin
        error "Failed to source step: $step_name"
        exit 1
    end
end

function main
    banner "🚀 Modern Project Setup" "" "Fish shell + Cat templating + AI prompts"

    # Check dependencies
    step check_dependencies

    # Get user preferences
    step select_language
    if test -z "$LANGUAGE"
        error "Language selection cancelled"
        exit 1
    end

    step select_template
    if test -z "$TEMPLATE"
        error "Template selection cancelled"
        exit 1
    end

    step get_project_info
    step get_vcs_info
    step get_github_info
    step select_ai_providers
    step select_licenses

    # Confirm setup
    if not gum confirm "Proceed with setup?"
        info "Setup cancelled"
        exit 0
    end

    # Perform setup
    step copy_template
    step generate_ai_prompts
    step initialize_vcs

    # Show completion message
    step show_next_steps
end

# Run main function
main $argv
