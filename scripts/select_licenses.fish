set licenses MIT "Apache-2.0" "GPL-3.0" BSD-3-Clause "MPL-2.0" Unlicense

# Set symbols
set sym_commercial 
set sym_modifications 
set sym_distribution 
set sym_private_use 
set sym_patent_use 
set sym_copyright 
set sym_document_changes 
set sym_disclose_source 
set sym_same_license 
set sym_same_license_file 
set sym_liability 
set sym_warranty 
set sym_trademark 
set sym_permissions 
set sym_conditions 
set sym_limitations 

function fetch_license_data -a license_key
    # Fetch license data from GitHub API
    set license_json (gum spin --spinner dot --show-output --title "Fetching license data" -- curl -s "https://api.github.com/licenses/$license_key")

    # Parse permissions, conditions, and limitations
    set permissions (echo $license_json | jq -r '.permissions[]?' | tr '\n' ' ' | string trim)
    set conditions (echo $license_json | jq -r '.conditions[]?' | tr '\n' ' ' | string trim)
    set limitations (echo $license_json | jq -r '.limitations[]?' | tr '\n' ' ' | string trim)

    # Return as space-separated values
    echo "$permissions|$conditions|$limitations"
end

# Create a temporary file for the license comparison table
set temp_file (mktemp)

# Header with legend
echo "# License Comparison" >$temp_file
echo "" >>$temp_file
echo "- **$sym_permissions Permissions** (Can do): $sym_commercial Commercial • $sym_modifications Modifications • $sym_distribution Distribution • $sym_private_use Private Use • $sym_patent_use Patent Use" >>$temp_file
echo "- **$sym_conditions Conditions** (Only if): $sym_copyright Copyright • $sym_document_changes Document Changes • $sym_disclose_source Disclose Source • $sym_same_license Same License • $sym_same_license_file Same License (File)" >>$temp_file
echo "- **$sym_limitations Limitations** (Must not): $sym_liability Liability • $sym_warranty Warranty • $sym_trademark Trademark Use" >>$temp_file
echo "" >>$temp_file

# Table header
echo "| License | $sym_commercial | $sym_modifications | $sym_distribution | $sym_private_use | $sym_patent_use | $sym_copyright | $sym_document_changes | $sym_disclose_source | $sym_same_license | $sym_same_license_file | $sym_liability | $sym_warranty | $sym_trademark |" >>$temp_file
echo "|-|-|-|-|-|-|-|-|-|-|-|-|-|-|" >>$temp_file

# Fetch and display license data
for license in $licenses
    set license_data (fetch_license_data $license)

    # Build the row with dynamic data
    set row "| **$license** |"

    # Permissions
    for field in commercial-use modifications distribution private-use patent-use
        # Check if the permission exists in the license data
        if string match -q "*$field*" $license_data
            set row "$row $sym_permissions|"
        else
            set row "$row |"
        end
    end

    # Conditions
    for field in copyright document-changes disclose-source same-license same-license--file
        # Check if the condition exists in the license data
        if string match -q "*$field*" $license_data
            set row "$row $sym_conditions|"
        else
            set row "$row |"
        end
    end

    # Limitations
    for field in liability warranty trademark-use
        # Check if the limitation exists in the license data
        if string match -q "*$field*" $license_data
            set row "$row $sym_limitations|"
        else
            set row "$row |"
        end
    end

    echo $row >>$temp_file
end

# Display the table
gum format <$temp_file
echo ""

# Clean up
rm $temp_file

set LICENSES (gum choose --ordered --no-limit $licenses --header "Select one or more licenses:")
if test -z "$LICENSES"
    warning "No licenses selected"
else
    info "Selected licenses: $(string join ", " $LICENSES)"
end
