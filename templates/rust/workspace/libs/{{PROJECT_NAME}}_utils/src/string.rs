//! String utility functions

/// Capitalize the first letter of a string
pub fn capitalize(s: &str) -> String {
    let mut chars = s.chars();
    match chars.next() {
        None => String::new(),
        Some(first) => first.to_uppercase().collect::<String>() + chars.as_str(),
    }
}

/// Check if a string is a valid identifier
pub fn is_valid_identifier(s: &str) -> bool {
    !s.is_empty() 
        && s.chars().next().unwrap().is_alphabetic()
        && s.chars().all(|c| c.is_alphanumeric() || c == '_')
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_capitalize() {
        assert_eq!(capitalize("hello"), "Hello");
        assert_eq!(capitalize(""), "");
        assert_eq!(capitalize("WORLD"), "WORLD");
    }

    #[test]
    fn test_is_valid_identifier() {
        assert!(is_valid_identifier("foo"));
        assert!(is_valid_identifier("foo_bar"));
        assert!(is_valid_identifier("Foo123"));
        assert!(!is_valid_identifier("123foo"));
        assert!(!is_valid_identifier(""));
        assert!(!is_valid_identifier("foo-bar"));
    }
}