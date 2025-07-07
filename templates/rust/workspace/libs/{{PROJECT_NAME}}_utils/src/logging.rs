//! Logging utilities

use anyhow::Result;

/// Initialize logging for the application
pub fn init() -> Result<()> {
    // In a real application, you might use tracing-subscriber here
    println!("Logging initialized");
    Ok(())
}

/// Log a message at info level
pub fn info(msg: &str) {
    println!("[INFO] {}", msg);
}

/// Log a message at error level
pub fn error(msg: &str) {
    eprintln!("[ERROR] {}", msg);
}