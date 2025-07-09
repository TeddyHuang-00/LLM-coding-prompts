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
