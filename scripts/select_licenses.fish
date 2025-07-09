set licenses MIT "Apache-2.0" "GPL-3.0" BSD-3-Clause "MPL-2.0" Unlicense

function show_license_comparison
    # Create a temporary file for the license comparison table
    set temp_file (mktemp)
    set sym_commercial "💼"
    set sym_modifications "🔧"
    set sym_distribution "📦"
    set sym_private_use "🏠"
    set sym_patent_use "🎯"
    set sym_copyright "©"
    set sym_document_changes "📝"
    set sym_disclose_source "🔓"
    set sym_same_license "🔄"
    set sym_same_license_file "📄"
    set sym_liability "⚖️"
    set sym_warranty "🛡️"
    set sym_trademark "™️"
    set sym_permissions "✅"
    set sym_conditions "⚠️"
    set sym_limitations "❌"

    # Header with legend
    echo "# License Comparison" >$temp_file
    echo "" >>$temp_file
    echo "- **Permissions ($sym_permissions)**: $sym_commercial Commercial • $sym_modifications Modifications • $sym_distribution Distribution • $sym_private_use Private Use • $sym_patent_use Patent Use" >>$temp_file
    echo "- **Conditions ($sym_conditions)**: $sym_copyright Copyright • $sym_document_changes Document Changes • $sym_disclose_source Disclose Source • $sym_same_license Same License • $sym_same_license_file Same License (File)" >>$temp_file
    echo "- **Limitations ($sym_limitations)**: $sym_liability Liability • $sym_warranty Warranty • $sym_trademark Trademark Use" >>$temp_file
    echo "" >>$temp_file

    # Table header
    echo "| License | $sym_commercial | $sym_modifications | $sym_distribution | $sym_private_use | $sym_patent_use | $sym_copyright | $sym_document_changes | $sym_disclose_source | $sym_same_license | $sym_same_license_file | $sym_liability | $sym_warranty | $sym_trademark |" >>$temp_file
    echo "|---------|---|---|---|---|---|---|---|---|---|---|---|---|---|" >>$temp_file

    # License information with symbols
    set licenses_info \
        "MIT|✅|✅|✅|✅|❌|⚠️|❌|❌|❌|❌|❌|❌|❌" \
        "Apache-2.0|✅|✅|✅|✅|✅|⚠️|⚠️|❌|❌|❌|❌|❌|❌" \
        "GPL-3.0|✅|✅|✅|✅|✅|⚠️|⚠️|⚠️|⚠️|❌|❌|❌|❌" \
        "BSD-3-Clause|✅|✅|✅|✅|❌|⚠️|❌|❌|❌|❌|❌|❌|❌" \
        "MPL-2.0|✅|✅|✅|✅|✅|⚠️|❌|⚠️|❌|⚠️|❌|❌|❌" \
        "Unlicense|✅|✅|✅|✅|❌|❌|❌|❌|❌|❌|❌|❌|❌"

    for license_info in $licenses_info
        set license_parts (string split "|" $license_info)
        set license_name $license_parts[1]

        # Build the row
        set row "| **$license_name** |"
        for i in (seq 2 14)
            set row "$row $license_parts[$i] |"
        end

        echo $row >>$temp_file
    end

    # Display the table
    gum format <$temp_file
    echo ""

    # Clean up
    rm $temp_file
end

info "License comparison:"
show_license_comparison

set LICENSES (gum choose --ordered --no-limit $licenses --header "Select one or more licenses:")
if test -z "$LICENSES"
    warning "No licenses selected"
else
    info "Selected licenses: $(string join ", " $LICENSES)"
end
