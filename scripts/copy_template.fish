function get_license_file_name -a license
    switch $license
        case Unlicense
            echo Unlicense
        case '*'
            set basename (string split -m1 '-' $license)[1]
            echo "LICENSE-$basename"
    end
end

set template_path "$TEMPLATES_DIR/$LANGUAGE/$TEMPLATE"

info "Copying template files..."

if not test -d "$template_path"
    error "Template not found: $template_path"
    exit 1
end

# Copy template files
mkdir -p (path dirname "$PROJECT_PATH")
rm -rf "$PROJECT_PATH"
cp -r "$template_path" "$PROJECT_PATH"
success "Template files copied"

# Add selected licenses
if test -n "$LICENSES"
    for license in $LICENSES
        set cache_key "license_$license"
        set license_json (cache_get "$cache_key")
        if test -z "$license_json"
            # Fetch license content from an online source (e.g., GitHub)
            set license_json (gum spin --spinner dot --show-output --title "Fetching $license license" -- curl -s "https://api.github.com/licenses/$license")
            # Cache for 30 days
            cache_set "$cache_key" "$license_json" (math '60 * 60 * 24 * 30')
        end

        set license_file (get_license_file_name "$license")
        set license_path "$PROJECT_PATH/$license_file"

        echo $license_json | jq -r '.body' >"$license_path"
        success "Added $license license"
    end
end

# Rename directories with template variables (process deepest first)
for dir in (find "$PROJECT_PATH" -type d -name "*{{PROJECT_NAME}}*" | sort -r)
    set new_name (string replace "{{PROJECT_NAME}}" "$PROJECT_NAME" "$dir")
    if test "$dir" != "$new_name"
        mv "$dir" "$new_name"
    end
end

# Generate license-related template variables
if test -z "$LICENSES"
    set LICENSES MIT
end

set main_license $LICENSES[1]

# Set license name for templates
set LICENSE_NAME (string join " OR " $LICENSES)

# Set license classifier for Python pyproject.toml (include all licenses)
set classifier
for license in $LICENSES
    switch $license
        case MIT
            set -a classifier "MIT License"
        case Apache-2.0
            set -a classifier "Apache Software License"
        case GPL-3.0
            set -a classifier "GNU General Public License v3 (GPLv3)"
        case BSD-3-Clause
            set -a classifier "BSD License"
        case MPL-2.0
            set -a classifier "Mozilla Public License 2.0 (MPL 2.0)"
        case Unlicense
            set -a classifier "The Unlicense (Unlicense)"
        case '*'
            set -a classifier "$license License"
    end

end

set LICENSE_CLASSIFIER
for cls in $classifier
    set -a LICENSE_CLASSIFIER "\"License :: OSI Approved :: $cls\","
end
set LICENSE_CLASSIFIER (string join "\\n    " $LICENSE_CLASSIFIER)

# Generate license text for README
if test (count $LICENSES) -eq 1
    set license_file (get_license_file_name "$main_license")
    set LICENSE_TEXT "This project is licensed under the $main_license License. See the [$license_file]($license_file) for details."
else
    set LICENSE_TEXT "This project is licensed under either of\\n"
    for license in $LICENSES
        set license_file (get_license_file_name "$license")
        set -a LICENSE_TEXT "- $license ([$license_file]($license_file))"
    end
    set -a LICENSE_TEXT "\\nat your option."
    set LICENSE_TEXT (string join "\\n" -- $LICENSE_TEXT)
end

# Update template placeholders using sed
for file in (find "$PROJECT_PATH" -type f -not -name ".gitignore" -not -name "LICENSE*" -not -path "*/.jj/*" -not -path "*/.git/*")
    if test -f "$file"
        sed -i.bak "s/{{PROJECT_NAME}}/$PROJECT_NAME/g" "$file"
        sed -i.bak "s/{{AUTHOR_NAME}}/$AUTHOR_NAME/g" "$file"
        sed -i.bak "s/{{AUTHOR_EMAIL}}/$AUTHOR_EMAIL/g" "$file"
        sed -i.bak "s/{{GITHUB_NAME}}/$GITHUB_NAME/g" "$file"
        sed -i.bak "s/{{LICENSE_NAME}}/$LICENSE_NAME/g" "$file"
        sed -i.bak "s/\"{{LICENSE_CLASSIFIER}}\",/$LICENSE_CLASSIFIER/g" "$file"
        sed -i.bak "s/{{LICENSE_TEXT}}/$LICENSE_TEXT/g" "$file"
        rm "$file.bak"
    end
end
# Replace license template strings
for file in (find "$PROJECT_PATH" -type f -name "LICENSE*")
    if test -f "$file"
        sed -i.bak "s/\\[year\\]/$CURRENT_YEAR/g" "$file"
        sed -i.bak "s/\\[yyyy\\]/$CURRENT_YEAR/g" "$file"
        sed -i.bak "s/\\[fullname\\]/$AUTHOR_NAME/g" "$file"
        sed -i.bak "s/\\[name of copyright owner\\]/$AUTHOR_NAME/g" "$file"
        rm "$file.bak"
    end
end

success "Project files updated"
