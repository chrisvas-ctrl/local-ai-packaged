#!/usr/bin/env python3
"""
stop_services.py

This script provides a graceful shutdown procedure for the local AI and Supabase services.
It's designed to be used after a successful execution of start_services.py.
"""

import os
import subprocess
import argparse
import time
import sys

def run_command(cmd, cwd=None):
    """Run a shell command and print it."""
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, cwd=cwd, check=True)

def stop_specific_services(services, timeout=30):
    """Stop specific services with a timeout."""
    if not services:
        return
    
    print(f"Stopping specified services: {', '.join(services)} with {timeout}s timeout...")
    try:
        # Try to stop services in localai-services project
        try:
            run_command([
                "docker", "compose", "-p", "localai-services", "stop", "-t", str(timeout)
            ] + services)
            print(f"Successfully stopped services in localai-services project: {', '.join(services)}")
        except subprocess.CalledProcessError as e:
            print(f"Warning: Error stopping services in localai-services project: {e}")
        
        # Try to stop services in localai-supabase project
        try:
            run_command([
                "docker", "compose", "-p", "localai-supabase", "stop", "-t", str(timeout)
            ] + services)
            print(f"Successfully stopped services in localai-supabase project: {', '.join(services)}")
        except subprocess.CalledProcessError as e:
            print(f"Warning: Error stopping services in localai-supabase project: {e}")
            
    except Exception as e:
        print(f"Warning: Error stopping services: {e}")
        print("Continuing with shutdown process...")

def stop_all_services(timeout=30):
    """Stop all services with a timeout before removing them."""
    print(f"Gracefully stopping all services with {timeout}s timeout...")
    try:
        # Stop localai-services project
        try:
            run_command([
                "docker", "compose", "-p", "localai-services", "stop", "-t", str(timeout)
            ])
            print("All services in localai-services project stopped successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Warning: Error stopping services in localai-services project: {e}")
        
        # Stop localai-supabase project
        try:
            run_command([
                "docker", "compose", "-p", "localai-supabase", "stop", "-t", str(timeout)
            ])
            print("All services in localai-supabase project stopped successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Warning: Error stopping services in localai-supabase project: {e}")
            
    except Exception as e:
        print(f"Warning: Error stopping services: {e}")
        print("Continuing with shutdown process...")

def remove_containers_and_networks():
    """Remove containers and networks but preserve volumes."""
    print("Removing containers and networks...")
    
    # Remove localai-services containers and networks
    try:
        print("Removing localai-services containers and networks...")
        run_command([
            "docker", "compose",
            "-p", "localai-services",
            "-f", "docker-compose.yml",
            "down"
        ])
        print("localai-services containers and networks removed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Warning: Error removing localai-services containers and networks: {e}")
    
    # Remove localai-supabase containers and networks
    try:
        print("Removing localai-supabase containers and networks...")
        if os.path.exists("supabase/docker/docker-compose.yml"):
            run_command([
                "docker", "compose",
                "-p", "localai-supabase",
                "-f", "supabase/docker/docker-compose.yml",
                "down"
            ])
            print("localai-supabase containers and networks removed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Warning: Error removing localai-supabase containers and networks: {e}")

def stop_and_remove_lingering_containers():
    """Stop and remove lingering containers that aren't managed by docker-compose."""
    print("Checking for lingering containers...")
    containers_to_check = ["ollama", "ollama-pull-llama", "n8n", "n8n-import"]
    
    for container in containers_to_check:
        try:
            # Check if container exists
            result = subprocess.run(["docker", "ps", "-a", "--filter", f"name=^/{container}$", "--format", "{{.Names}}"], 
                                   capture_output=True, text=True, check=False)
            if result.stdout.strip():
                print(f"Stopping and removing lingering container: {container}")
                # Stop the container first
                subprocess.run(["docker", "stop", container], 
                               check=False, stderr=subprocess.PIPE)
                # Then remove it
                subprocess.run(["docker", "rm", "-f", container], 
                               check=False, stderr=subprocess.PIPE)
                print(f"Container {container} removed.")
        except Exception as e:
            print(f"Note: Error handling container {container}: {e}")
            
    # Also check for any containers with names containing ollama
    try:
        # Find all containers with names containing 'ollama'
        result = subprocess.run(["docker", "ps", "-a", "--filter", "name=ollama", "--format", "{{.Names}}"], 
                               capture_output=True, text=True, check=False)
        container_names = result.stdout.strip().split('\n')
        
        # Stop and remove each found container
        for name in container_names:
            if name and name not in containers_to_check:  # Skip if already handled above
                print(f"Stopping and removing additional container: {name}")
                subprocess.run(["docker", "stop", name], check=False, stderr=subprocess.PIPE)
                subprocess.run(["docker", "rm", "-f", name], check=False, stderr=subprocess.PIPE)
                print(f"Container {name} removed.")
    except Exception as e:
        print(f"Note: Error handling additional containers: {e}")

def prune_networks():
    """Prune unused Docker networks."""
    print("Pruning unused Docker networks...")
    try:
        run_command(["docker", "network", "prune", "-f"])
        print("Docker networks pruned successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Warning: Failed to prune Docker networks: {e}")

def check_running_containers():
    """Check if there are any running containers in the localai-services or localai-supabase projects."""
    try:
        # Check localai-services project
        services_result = subprocess.run(
            ["docker", "compose", "-p", "localai-services", "ps", "--format", "json"],
            capture_output=True, text=True, check=False
        )
        
        # Check localai-supabase project
        supabase_result = subprocess.run(
            ["docker", "compose", "-p", "localai-supabase", "ps", "--format", "json"],
            capture_output=True, text=True, check=False
        )
        
        # Return True if either project has running containers
        return len(services_result.stdout.strip()) > 0 or len(supabase_result.stdout.strip()) > 0
    except Exception:
        print("Warning: Could not check for running containers.")
        return False

def check_existing_containers():
    """Check if there are any containers (running or stopped) related to our projects."""
    try:
        # Check for any containers (running or stopped) from localai-services project
        services_result = subprocess.run(
            ["docker", "ps", "-a", "--filter", "label=com.docker.compose.project=localai-services", "--format", "{{.Names}}"],
            capture_output=True, text=True, check=False
        )
        
        # Check for any containers (running or stopped) from localai-supabase project
        supabase_result = subprocess.run(
            ["docker", "ps", "-a", "--filter", "label=com.docker.compose.project=localai-supabase", "--format", "{{.Names}}"],
            capture_output=True, text=True, check=False
        )
        
        # Check for ollama containers
        ollama_result = subprocess.run(
            ["docker", "ps", "-a", "--filter", "name=ollama", "--format", "{{.Names}}"],
            capture_output=True, text=True, check=False
        )
        
        # Return True if any containers exist
        has_services = len(services_result.stdout.strip()) > 0
        has_supabase = len(supabase_result.stdout.strip()) > 0
        has_ollama = len(ollama_result.stdout.strip()) > 0
        
        if has_services:
            print(f"Found containers from localai-services project: {services_result.stdout.strip()}")
        if has_supabase:
            print(f"Found containers from localai-supabase project: {supabase_result.stdout.strip()}")
        if has_ollama:
            print(f"Found ollama containers: {ollama_result.stdout.strip()}")
            
        return has_services or has_supabase or has_ollama
    except Exception as e:
        print(f"Warning: Could not check for existing containers: {e}")
        return True  # Assume containers exist if we can't check

def main():
    parser = argparse.ArgumentParser(description='Gracefully stop the local AI and Supabase services.')
    parser.add_argument('--timeout', type=int, default=30,
                      help='Timeout in seconds for graceful shutdown (default: 30)')
    parser.add_argument('--force', action='store_true',
                      help='Force shutdown without confirmation')
    parser.add_argument('--services', nargs='+',
                      help='Specific services to stop (e.g., n8n crawl4ai)')
    args = parser.parse_args()
    
    # Check if any containers exist (running or stopped)
    if not check_existing_containers():
        print("No containers found related to localai-services or localai-supabase projects.")
        sys.exit(0)
        
    # Check if services are running and inform the user
    if not check_running_containers():
        print("Note: No running containers found, but stopped containers exist. Will proceed with cleanup.")
    
    # Confirmation unless --force is used
    if not args.force:
        confirm = input("Are you sure you want to stop all services? [y/N]: ")
        if confirm.lower() != 'y':
            print("Shutdown cancelled.")
            sys.exit(0)
    
    # If specific services are specified, stop only those
    if args.services:
        stop_specific_services(args.services, args.timeout)
    else:
        # Otherwise, stop all services
        stop_all_services(args.timeout)
    
    # Remove containers and networks
    remove_containers_and_networks()
    
    # Stop and remove lingering containers like ollama
    stop_and_remove_lingering_containers()
    
    # Prune networks to clean up
    prune_networks()
    
    print("Shutdown complete. All services have been stopped and containers removed.")
    print("Volumes have been preserved to maintain data.")

if __name__ == "__main__":
    main()
