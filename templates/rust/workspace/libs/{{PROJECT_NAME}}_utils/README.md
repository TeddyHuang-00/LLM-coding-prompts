# {{PROJECT_NAME}}_utils

Utility functions and helpers for the {{PROJECT_NAME}} project.

## Features

- `std` (default): Standard library support

## Modules

### Logging

Simple logging utilities:

```rust
use {{PROJECT_NAME}}_utils::logging;

// Initialize logging
{{PROJECT_NAME}}_utils::init()?;

// Log messages
logging::info("Application started");
logging::error("Something went wrong");
```

### String Utilities

Common string manipulation functions:

```rust
use {{PROJECT_NAME}}_utils::string;

// Capitalize a string
let capitalized = string::capitalize("hello world");
assert_eq!(capitalized, "Hello world");

// Validate identifiers
assert!(string::is_valid_identifier("my_var"));
assert!(!string::is_valid_identifier("123invalid"));
```