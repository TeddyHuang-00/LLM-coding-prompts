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
