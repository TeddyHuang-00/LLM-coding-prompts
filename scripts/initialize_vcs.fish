switch $VCS_NAME
    case git
        git init $PROJECT_PATH
    case jj
        jj git init $PROJECT_PATH
end
success "$VCS_NAME initialized"
