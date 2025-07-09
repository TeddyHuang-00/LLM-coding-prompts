set providers "GitHub Copilot:copilot" "Cursor:cursor" "Gemini CLI:gemini" "Claude Code:claude"

set selected (gum choose --no-limit $providers --header "Select AI coding assistants:" --label-delimiter ":")
if test -z "$selected"
    warning "No AI providers selected"
else
    set AI_PROVIDERS $selected
    info "Selected AI providers: $(string join ", " $AI_PROVIDERS)"
end
