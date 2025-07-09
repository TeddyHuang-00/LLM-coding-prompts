set PROJECT_NAME (gum input --placeholder "Enter project name" --prompt "Project name: ")
if test -z "$PROJECT_NAME"
    error "Project name is required"
    exit 1
end

set PROJECT_PATH (gum input --placeholder "Enter project path (default: current directory)" --prompt "Project path: ")
set PROJECT_PATH (string trim $PROJECT_PATH | path normalize)
if test -z "$PROJECT_PATH"
    set PROJECT_PATH "$(pwd)/new_project"
end

if test -d "$PROJECT_PATH"
    warning "Directory '$PROJECT_PATH' already exists."
    if not gum confirm "Remove existing directory and create a new one?"
        error "Directory already exists: $PROJECT_PATH"
        exit 1
    end
end

info "Project name: $PROJECT_NAME"
info "Project path: $PROJECT_PATH"
