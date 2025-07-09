set deps
set opt_deps
set -a deps "gum|https://github.com/charmbracelet/gum"
set -a deps "jq|https://stedolan.github.io/jq"
set -a deps "curl|https://curl.se"
set -a deps "sed|https://www.gnu.org/software/sed"
set -a deps "find|https://www.gnu.org/software/findutils"
set -a deps "mktemp|https://www.gnu.org/software/coreutils"
set -a opt_deps "git|https://git-scm.com"
set -a opt_deps "jj|https://jj-vcs.github.io/jj"

set missing_deps
set missing_opt_deps

for dep in $deps
    set dep_name (string split '|' $dep)[1]
    set dep_url (string split '|' $dep)[2]

    if not type -q $dep_name
        set -a missing_deps "$dep_name ($dep_url)"
    end
end

for dep in $opt_deps
    set dep_name (string split '|' $dep)[1]
    set dep_url (string split '|' $dep)[2]

    if not type -q $dep_name
        set -a missing_opt_deps "$dep_name ($dep_url)"
    end
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

if test (count $missing_opt_deps) -gt 0
    warning "Missing optional dependencies:"
    for dep in $missing_opt_deps
        echo "  - $dep"
    end
    echo ""
    echo "Optional dependencies are not required but may provide additional functionality."
end
