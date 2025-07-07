//! Core functionality for {{PROJECT_NAME}}
//!
//! This library provides the fundamental types and operations
//! used throughout the {{PROJECT_NAME}} project.

#![cfg_attr(not(feature = "std"), no_std)]
#![warn(missing_docs)]
#![warn(clippy::all)]

pub mod error;
pub mod types;

pub use error::{Error, Result};

/// Core functionality module
pub mod core {
    use crate::Result;

    /// Initialize the core system
    pub fn init() -> Result<()> {
        println!("Initializing core system");
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_core_init() {
        assert!(core::init().is_ok());
    }
}