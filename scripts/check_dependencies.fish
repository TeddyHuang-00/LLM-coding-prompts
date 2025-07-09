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
