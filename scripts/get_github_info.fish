set cache_key "github_username"

# Try to get cached username
set cached_username (cache_get "$cache_key")

# Use cached username as default if available
set GITHUB_NAME (gum input --placeholder "Enter your GitHub username" --prompt "GitHub username: " --value "$cached_username")

if test -z "$GITHUB_NAME"
    error "GitHub username is required"
    exit 1
end

# Set cache if expired or different from cached value
if test -z "$cached_username" -o "$GITHUB_NAME" != "$cached_username"
    # Cache the username for future use (cache for 1 year)
    cache_set "$cache_key" "$GITHUB_NAME" (math '60 * 60 * 24 * 365')
end

info "GitHub username: $GITHUB_NAME"
