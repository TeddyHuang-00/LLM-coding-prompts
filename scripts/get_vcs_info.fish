set vcs_options "Git:git" "Jujutsu:jj"
set VCS_NAME (gum choose $vcs_options --header "Select version control system (VCS):" --label-delimiter ":")

if not type -q "$VCS_NAME"
    error "'$VCS_NAME' is not installed or recognized. Please install it or choose another VCS."
    exit 1
end

switch $VCS_NAME
    case git
        set AUTHOR_NAME (git config --global user.name 2>/dev/null; or echo "")
        set AUTHOR_EMAIL (git config --global user.email 2>/dev/null; or echo "")
    case jj
        set AUTHOR_NAME (jj config g user.name 2>/dev/null; or echo "")
        set AUTHOR_EMAIL (jj config g user.email 2>/dev/null; or echo "")
end

if test -z "$AUTHOR_NAME"
    warning "No author name configured for $VCS_NAME. Please set it now."
    set AUTHOR_NAME (gum input --placeholder "Enter your name" --prompt "Author name: ")
    if test -z "$AUTHOR_NAME"
        error "Author name is required"
        exit 1
    end

    switch $VCS_NAME
        case git
            git config --global user.name "$AUTHOR_NAME"
        case jj
            jj config s --user user.name "$AUTHOR_NAME"
    end
end

if test -z "$AUTHOR_EMAIL"
    warning "No author email configured for $VCS_NAME. Please set it now."
    set AUTHOR_EMAIL (gum input --placeholder "Enter your email" --prompt "Author email: ")
    if test -z "$AUTHOR_EMAIL"
        error "Author email is required"
        exit 1
    else if not string match -qr '^([a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6})*$' "$AUTHOR_EMAIL"
        error "Invalid email format: $AUTHOR_EMAIL"
        exit 1
    end

    switch $VCS_NAME
        case git
            git config --global user.email "$AUTHOR_EMAIL"
        case jj
            jj config s --user user.email "$AUTHOR_EMAIL"
    end
end

info "VCS: $VCS_NAME"
info "Author: $AUTHOR_NAME <$AUTHOR_EMAIL>"
