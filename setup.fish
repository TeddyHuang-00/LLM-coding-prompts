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

function cache_get -a cache_key
    set cache_dir .cache
    set cache_file "$cache_dir/$cache_key"
    set meta_file "$cache_dir/$cache_key.ttl"

    # Check if cache file exists
    if not test -f $cache_file
        echo ""
        return
    end

    # Check if meta file exists (contains expiration timestamp)
    if not test -f $meta_file
        echo ""
        return
    end

    # Read expiration timestamp
    set expiry_time (cat $meta_file)
    set current_time (date +%s)

    # Check if cache is expired
    if test $current_time -gt $expiry_time
        # Clean up expired cache
        rm -f $cache_file $meta_file
        echo ""
        return
    end

    # Return cached content
    cat $cache_file
end

function cache_set -a cache_key content ttl_seconds
    set cache_dir .cache
    set cache_file "$cache_dir/$cache_key"
    set meta_file "$cache_dir/$cache_key.ttl"

    # Create cache directory if it doesn't exist
    mkdir -p $cache_dir

    # Save content to cache file
    echo $content >$cache_file

    # Calculate expiration time and save to meta file
    set expiry_time (math (date +%s) + $ttl_seconds)
    echo $expiry_time >$meta_file
end

function step
    set step_name $argv[1]
    set file_path "scripts/$step_name.fish"
    source $file_path; or begin
        error "Failed at step: $step_name"
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
