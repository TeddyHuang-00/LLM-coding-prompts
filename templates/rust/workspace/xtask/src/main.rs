//! Build automation for {{PROJECT_NAME}}
//!
//! Run with: cargo xtask <command>

use anyhow::Result;
use std::env;
use std::process::Command;

fn main() -> Result<()> {
    let task = env::args().nth(1);
    match task.as_deref() {
        Some("ci") => ci(),
        Some("fmt") => fmt(),
        Some("lint") => lint(),
        Some("test") => test(),
        Some("build") => build(),
        Some("clean") => clean(),
        _ => print_help(),
    }
}

fn print_help() -> Result<()> {
    println!("xtask - Build automation for {{PROJECT_NAME}}");
    println!();
    println!("USAGE:");
    println!("    cargo xtask <TASK>");
    println!();
    println!("TASKS:");
    println!("    ci      Run complete CI pipeline");
    println!("    fmt     Format code");
    println!("    lint    Run clippy lints");
    println!("    test    Run tests");
    println!("    build   Build all crates");
    println!("    clean   Clean build artifacts");
    Ok(())
}

fn ci() -> Result<()> {
    println!("Running CI pipeline...");
    fmt()?;
    lint()?;
    test()?;
    build()?;
    println!("CI pipeline completed successfully!");
    Ok(())
}

fn fmt() -> Result<()> {
    println!("Formatting code...");
    let status = Command::new("cargo")
        .args(["fmt", "--all"])
        .status()?;
    
    if !status.success() {
        anyhow::bail!("cargo fmt failed");
    }
    Ok(())
}

fn lint() -> Result<()> {
    println!("Running lints...");
    let status = Command::new("cargo")
        .args(["clippy", "--all-targets", "--all-features", "--", "-D", "warnings"])
        .status()?;
    
    if !status.success() {
        anyhow::bail!("cargo clippy failed");
    }
    Ok(())
}

fn test() -> Result<()> {
    println!("Running tests...");
    let status = Command::new("cargo")
        .args(["test", "--all-features"])
        .status()?;
    
    if !status.success() {
        anyhow::bail!("cargo test failed");
    }
    Ok(())
}

fn build() -> Result<()> {
    println!("Building all crates...");
    let status = Command::new("cargo")
        .args(["build", "--all-targets", "--all-features"])
        .status()?;
    
    if !status.success() {
        anyhow::bail!("cargo build failed");
    }
    Ok(())
}

fn clean() -> Result<()> {
    println!("Cleaning build artifacts...");
    let status = Command::new("cargo")
        .args(["clean"])
        .status()?;
    
    if !status.success() {
        anyhow::bail!("cargo clean failed");
    }
    Ok(())
}