set GITHUB_NAME (gum input --placeholder "Enter your GitHub username" --prompt "GitHub username: ")
if test -z "$GITHUB_NAME"
    error "GitHub username is required"
    exit 1
end

info "GitHub username: $GITHUB_NAME"
