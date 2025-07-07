//! Common types used throughout the project

/// Configuration structure
#[derive(Debug, Clone)]
pub struct Config {
    /// Application name
    pub name: String,
    /// Debug mode enabled
    pub debug: bool,
    /// Maximum concurrent operations
    pub max_concurrent: usize,
}

impl Default for Config {
    fn default() -> Self {
        Self {
            name: "{{PROJECT_NAME}}".to_string(),
            debug: false,
            max_concurrent: 4,
        }
    }
}

/// Application state
#[derive(Debug)]
pub struct AppState {
    /// Current configuration
    pub config: Config,
    /// Number of active operations
    pub active_operations: usize,
}

impl AppState {
    /// Create new application state with config
    pub fn new(config: Config) -> Self {
        Self {
            config,
            active_operations: 0,
        }
    }
}