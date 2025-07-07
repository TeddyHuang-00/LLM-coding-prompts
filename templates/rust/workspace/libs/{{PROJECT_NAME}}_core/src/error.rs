//! Error types and utilities

use thiserror::Error;

/// Core error type for {{PROJECT_NAME}}
#[derive(Error, Debug)]
pub enum Error {
    /// IO error
    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),
    
    /// Configuration error
    #[error("Configuration error: {0}")]
    Config(String),
    
    /// Generic error with message
    #[error("{0}")]
    Other(String),
}

/// Result type alias using our Error
pub type Result<T> = std::result::Result<T, Error>;