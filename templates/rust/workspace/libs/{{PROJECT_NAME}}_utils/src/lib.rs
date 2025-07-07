//! Utility functions for {{PROJECT_NAME}}
//!
//! This library provides common utility functions and helpers
//! used across the {{PROJECT_NAME}} project.

#![cfg_attr(not(feature = "std"), no_std)]
#![warn(missing_docs)]
#![warn(clippy::all)]

pub mod logging;
pub mod string;

/// Initialize utilities
pub fn init() -> anyhow::Result<()> {
    logging::init()?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_init() {
        assert!(init().is_ok());
    }
}