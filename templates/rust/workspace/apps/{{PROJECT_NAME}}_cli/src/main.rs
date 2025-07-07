//! Command-line interface for {{PROJECT_NAME}}

use anyhow::Result;
use clap::{Parser, Subcommand};
use {{PROJECT_NAME}}_core::{core, types::Config};
use {{PROJECT_NAME}}_utils::{logging, string};

#[derive(Parser)]
#[command(name = "{{PROJECT_NAME}}")]
#[command(about = "A modern Rust workspace project")]
#[command(version)]
struct Cli {
    /// Enable debug mode
    #[arg(short, long)]
    debug: bool,
    
    /// Configuration file path
    #[arg(short, long)]
    config: Option<String>,
    
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Initialize the project
    Init {
        /// Project name
        #[arg(short, long)]
        name: Option<String>,
    },
    /// Run the main application
    Run {
        /// Input file
        #[arg(short, long)]
        input: Option<String>,
    },
    /// Show project status
    Status,
}

fn main() -> Result<()> {
    let cli = Cli::parse();
    
    // Initialize utilities
    {{PROJECT_NAME}}_utils::init()?;
    
    // Configure logging based on debug flag
    if cli.debug {
        logging::info("Debug mode enabled");
    }
    
    // Load configuration
    let config = if let Some(config_path) = cli.config {
        logging::info(&format!("Loading config from: {}", config_path));
        Config::default() // In real app, load from file
    } else {
        Config::default()
    };
    
    // Initialize core
    core::init()?;
    
    // Handle commands
    match cli.command {
        Commands::Init { name } => {
            let project_name = name.unwrap_or_else(|| "my_project".to_string());
            let capitalized = string::capitalize(&project_name);
            logging::info(&format!("Initializing project: {}", capitalized));
            
            if !string::is_valid_identifier(&project_name) {
                anyhow::bail!("Invalid project name: {}", project_name);
            }
            
            println!("Project '{}' initialized successfully!", capitalized);
        }
        Commands::Run { input } => {
            logging::info("Running application");
            if let Some(input_file) = input {
                println!("Processing input file: {}", input_file);
            } else {
                println!("Running with default configuration");
            }
            println!("Application completed successfully!");
        }
        Commands::Status => {
            println!("{{PROJECT_NAME}} Status:");
            println!("  Version: {}", env!("CARGO_PKG_VERSION"));
            println!("  Debug: {}", cli.debug);
            println!("  Config: {:?}", config);
        }
    }
    
    Ok(())
}