set template_dir "$TEMPLATES_DIR/$LANGUAGE"
if not test -d "$template_dir"
    error "No templates found for $LANGUAGE"
    exit 1
end

set templates
for template_path in $template_dir/*
    if test -d "$template_path"
        set -a templates (basename $template_path)
    end
end

if test (count $templates) -eq 0
    error "No templates found in $template_dir"
    exit 1
end

set TEMPLATE (gum choose $templates --header "Select project template:")
info "Template: $TEMPLATE"
