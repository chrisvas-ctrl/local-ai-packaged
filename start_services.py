#!/usr/bin/env python3
"""
start_services.py

This script starts the Supabase stack first, waits for it to initialize, and then starts
the local AI stack. Both stacks use the same Docker Compose project name ("localai")
so they appear together in Docker Desktop.
"""

import os
import subprocess
import shutil
import time
import argparse
import platform
import sys

def run_command(cmd, cwd=None, check=True):
    """Run a shell command and print it."""
    print("Running:", " ".join(cmd))
    return subprocess.run(cmd, cwd=cwd, check=check)

def clone_supabase_repo():
    """Clone the Supabase repository using sparse checkout if not already present."""
    if not os.path.exists("supabase"):
        print("Cloning the Supabase repository...")
        run_command([
            "git", "clone", "--filter=blob:none", "--no-checkout",
            "https://github.com/supabase/supabase.git"
        ])
        os.chdir("supabase")
        run_command(["git", "sparse-checkout", "init", "--cone"])
        run_command(["git", "sparse-checkout", "set", "docker"])
        run_command(["git", "checkout", "master"])
        os.chdir("..")
    else:
        print("Supabase repository already exists, updating...")
        os.chdir("supabase")
        run_command(["git", "pull"])
        os.chdir("..")

def prepare_supabase_env():
    """Copy .env to .env in supabase/docker."""
    env_path = os.path.join("supabase", "docker", ".env")
    env_example_path = os.path.join(".env")
    print("Copying .env in root to .env in supabase/docker...")
    shutil.copyfile(env_example_path, env_path)

def stop_existing_containers():
    """Stop and remove existing containers for our unified project ('localai')."""
    print("Stopping and removing existing containers for the unified project 'localai'...")
    # Stop Supabase services
    run_command([
        "docker", "compose",
        "-p", "localai-supabase",
        "-f", "supabase/docker/docker-compose.yml",
        "down"
    ])
    # Stop local AI services
    run_command([
        "docker", "compose",
        "-p", "localai-services",
        "-f", "docker-compose.yml",
        "down"
    ])
    
    # Check for and remove any lingering containers
    try:
        print("Checking for lingering containers...")
        containers_to_check = ["ollama", "ollama-pull-llama", "n8n", "n8n-import"]
        
        for container in containers_to_check:
            # Check if container exists
            result = subprocess.run(["docker", "ps", "-a", "--filter", f"name=^/{container}$", "--format", "{{.Names}}"], 
                                  capture_output=True, text=True, check=False)
            if result.stdout.strip():
                print(f"Removing lingering container: {container}")
                subprocess.run(["docker", "rm", "-f", container], 
                              check=False, stderr=subprocess.PIPE)
    except Exception as e:
        print(f"Note: Error removing lingering containers: {e}")
    
    # Remove the shared network if it exists
    try:
        print("Removing shared network if it exists...")
        subprocess.run(["docker", "network", "rm", "localai-network"], 
                      check=False, stderr=subprocess.PIPE)
    except Exception as e:
        print(f"Note: Could not remove network (it may not exist): {e}")

def create_shared_network():
    """Create a shared Docker network for all services."""
    print("Creating shared Docker network 'localai-network'...")
    try:
        # Check if network already exists
        result = subprocess.run(["docker", "network", "inspect", "localai-network"], 
                              capture_output=True, check=False)
        if result.returncode != 0:
            # Create network if it doesn't exist
            run_command(["docker", "network", "create", "localai-network"])
        else:
            print("Network 'localai-network' already exists.")
    except Exception as e:
        print(f"Error creating network: {e}")
        raise

def start_supabase():
    """Start the Supabase services."""
    print("Starting Supabase services...")
    run_command([
        "docker", "compose", "-p", "localai-supabase", 
        "-f", "supabase/docker/docker-compose.yml",
        "up", "-d"
    ])
    
    # Connect all Supabase containers to our shared network
    print("Connecting Supabase containers to shared network...")
    try:
        # Get all containers from the localai-supabase project
        result = subprocess.run(["docker", "ps", "-q", "--filter", "label=com.docker.compose.project=localai-supabase"], 
                              capture_output=True, text=True, check=True)
        container_ids = result.stdout.strip().split('\n')
        
        # Connect each container to the shared network with appropriate aliases
        for container_id in container_ids:
            if container_id:  # Skip empty lines
                # Get container name
                name_result = subprocess.run(["docker", "inspect", "--format", "{{.Name}}", container_id], 
                                          capture_output=True, text=True, check=True)
                container_name = name_result.stdout.strip().lstrip('/')
                
                print(f"Connecting container {container_name} to shared network...")
                
                # Add special aliases for key containers
                if container_name == "supabase-db":
                    print("Adding 'postgres' alias to the database container...")
                    subprocess.run(["docker", "network", "connect", "--alias", "postgres", 
                                  "localai-network", container_id], 
                                  check=False, stderr=subprocess.PIPE)
                    # Also add supabase-db alias for services that use this name
                    subprocess.run(["docker", "network", "connect", "--alias", "supabase-db", 
                                  "localai-network", container_id], 
                                  check=False, stderr=subprocess.PIPE)
                else:
                    # Connect other containers without special alias
                    subprocess.run(["docker", "network", "connect", "localai-network", container_id], 
                                  check=False, stderr=subprocess.PIPE)
    except Exception as e:
        print(f"Note: Error connecting containers to network: {e}")

def start_local_ai(profile=None):
    """Start the local AI services."""
    print("Starting local AI services...")
    cmd = ["docker", "compose", "-p", "localai-services"]
    if profile and profile != "none":
        cmd.extend(["--profile", profile])
    cmd.extend([
        "-f", "docker-compose.yml",
        "up", "-d"
    ])
    
    # Run the command and capture output to check for specific errors
    print("Running:", " ".join(cmd))
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    
    # Check if there was an error
    if result.returncode != 0:
        # Check if the error is just related to n8n-import (expected failure)
        if "service \"n8n-import\" didn't complete successfully" in result.stderr:
            print("Note: n8n-import service exited as expected. This is normal behavior.")
            print("Continuing with the rest of the startup process...")
        else:
            # This is an unexpected error, print details and raise exception
            print(f"Error starting local AI services:\n{result.stderr}")
            raise subprocess.CalledProcessError(result.returncode, cmd, output=result.stdout, stderr=result.stderr)
    
    # Connect all local AI containers to our shared network
    print("Connecting local AI containers to shared network...")
    try:
        # Get all containers from the localai-services project
        result = subprocess.run(["docker", "ps", "-q", "--filter", "label=com.docker.compose.project=localai-services"], 
                              capture_output=True, text=True, check=True)
        container_ids = result.stdout.strip().split('\n')
        
        # Connect each container to the shared network
        for container_id in container_ids:
            if container_id:  # Skip empty lines
                # Get container name
                name_result = subprocess.run(["docker", "inspect", "--format", "{{.Name}}", container_id], 
                                          capture_output=True, text=True, check=True)
                container_name = name_result.stdout.strip().lstrip('/')
                
                print(f"Connecting container {container_name} to shared network...")
                subprocess.run(["docker", "network", "connect", "localai-network", container_id], 
                              check=False, stderr=subprocess.PIPE)
    except Exception as e:
        print(f"Note: Error connecting containers to network: {e}")
    
    # Ensure n8n container is started properly
    print("Ensuring n8n container is properly started...")
    try:
        # Check if n8n container exists but is not running
        result = subprocess.run(["docker", "ps", "-a", "--filter", "name=n8n$", "--format", "{{.Status}}"], 
                              capture_output=True, text=True, check=True)
        status = result.stdout.strip()
        
        if status and not status.startswith("Up "):
            print("Starting n8n container...")
            subprocess.run(["docker", "start", "n8n"], 
                          check=False, stderr=subprocess.PIPE)
            print("n8n container started.")
    except Exception as e:
        print(f"Note: Error starting n8n container: {e}")

def generate_searxng_secret_key():
    """Generate a secret key for SearXNG based on the current platform."""
    print("Checking SearXNG settings...")
    
    # Define paths for SearXNG settings files
    settings_path = os.path.join("searxng", "settings.yml")
    settings_base_path = os.path.join("searxng", "settings-base.yml")
    
    # Check if settings-base.yml exists
    if not os.path.exists(settings_base_path):
        print(f"Warning: SearXNG base settings file not found at {settings_base_path}")
        return
    
    # Check if settings.yml exists, if not create it from settings-base.yml
    if not os.path.exists(settings_path):
        print(f"SearXNG settings.yml not found. Creating from {settings_base_path}...")
        try:
            shutil.copyfile(settings_base_path, settings_path)
            print(f"Created {settings_path} from {settings_base_path}")
        except Exception as e:
            print(f"Error creating settings.yml: {e}")
            return
    else:
        print(f"SearXNG settings.yml already exists at {settings_path}")
    
    print("Generating SearXNG secret key...")
    
    # Detect the platform and run the appropriate command
    system = platform.system()
    
    try:
        if system == "Windows":
            print("Detected Windows platform, using PowerShell to generate secret key...")
            # PowerShell command to generate a random key and replace in the settings file
            ps_command = [
                "powershell", "-Command",
                "$randomBytes = New-Object byte[] 32; " +
                "(New-Object Security.Cryptography.RNGCryptoServiceProvider).GetBytes($randomBytes); " +
                "$secretKey = -join ($randomBytes | ForEach-Object { \"{0:x2}\" -f $_ }); " +
                "(Get-Content searxng/settings.yml) -replace 'ultrasecretkey', $secretKey | Set-Content searxng/settings.yml"
            ]
            subprocess.run(ps_command, check=True)
            
        elif system == "Darwin":  # macOS
            print("Detected macOS platform, using sed command with empty string parameter...")
            # macOS sed command requires an empty string for the -i parameter
            openssl_cmd = ["openssl", "rand", "-hex", "32"]
            random_key = subprocess.check_output(openssl_cmd).decode('utf-8').strip()
            sed_cmd = ["sed", "-i", "", f"s|ultrasecretkey|{random_key}|g", settings_path]
            subprocess.run(sed_cmd, check=True)
            
        else:  # Linux and other Unix-like systems
            print("Detected Linux/Unix platform, using standard sed command...")
            # Standard sed command for Linux
            openssl_cmd = ["openssl", "rand", "-hex", "32"]
            random_key = subprocess.check_output(openssl_cmd).decode('utf-8').strip()
            sed_cmd = ["sed", "-i", f"s|ultrasecretkey|{random_key}|g", settings_path]
            subprocess.run(sed_cmd, check=True)
            
        print("SearXNG secret key generated successfully.")
        
    except Exception as e:
        print(f"Error generating SearXNG secret key: {e}")
        print("You may need to manually generate the secret key using the commands:")
        print("  - Linux: sed -i \"s|ultrasecretkey|$(openssl rand -hex 32)|g\" searxng/settings.yml")
        print("  - macOS: sed -i '' \"s|ultrasecretkey|$(openssl rand -hex 32)|g\" searxng/settings.yml")
        print("  - Windows (PowerShell):")
        print("    $randomBytes = New-Object byte[] 32")
        print("    (New-Object Security.Cryptography.RNGCryptoServiceProvider).GetBytes($randomBytes)")
        print("    $secretKey = -join ($randomBytes | ForEach-Object { \"{0:x2}\" -f $_ })")
        print("    (Get-Content searxng/settings.yml) -replace 'ultrasecretkey', $secretKey | Set-Content searxng/settings.yml")

def check_and_fix_docker_compose_for_searxng():
    """Check and modify docker-compose.yml for SearXNG first run."""
    docker_compose_path = "docker-compose.yml"
    if not os.path.exists(docker_compose_path):
        print(f"Warning: Docker Compose file not found at {docker_compose_path}")
        return
    
    try:
        # Read the docker-compose.yml file
        with open(docker_compose_path, 'r') as file:
            content = file.read()
        
        # Default to first run
        is_first_run = True
        
        # Check if Docker is running and if the SearXNG container exists
        try:
            # Check if the SearXNG container is running
            container_check = subprocess.run(
                ["docker", "ps", "--filter", "name=searxng", "--format", "{{.Names}}"],
                capture_output=True, text=True, check=True
            )
            searxng_containers = container_check.stdout.strip().split('\n')
            
            # If SearXNG container is running, check inside for uwsgi.ini
            if any(container for container in searxng_containers if container):
                container_name = next(container for container in searxng_containers if container)
                print(f"Found running SearXNG container: {container_name}")
                
                # Check if uwsgi.ini exists inside the container
                container_check = subprocess.run(
                    ["docker", "exec", container_name, "sh", "-c", "[ -f /etc/searxng/uwsgi.ini ] && echo 'found' || echo 'not_found'"],
                    capture_output=True, text=True, check=True
                )
                
                if "found" in container_check.stdout:
                    print("Found uwsgi.ini inside the SearXNG container - not first run")
                    is_first_run = False
                else:
                    print("uwsgi.ini not found inside the SearXNG container - first run")
                    is_first_run = True
            else:
                print("No running SearXNG container found - assuming first run")
        except Exception as e:
            print(f"Error checking Docker container: {e} - assuming first run")
        
        if is_first_run and "cap_drop: - ALL" in content:
            print("First run detected for SearXNG. Temporarily removing 'cap_drop: - ALL' directive...")
            # Temporarily comment out the cap_drop line
            modified_content = content.replace("cap_drop: - ALL", "# cap_drop: - ALL  # Temporarily commented out for first run")
            
            # Write the modified content back
            with open(docker_compose_path, 'w') as file:
                file.write(modified_content)
                
            print("Note: After the first run completes successfully, you should re-add 'cap_drop: - ALL' to docker-compose.yml for security reasons.")
        elif not is_first_run and "# cap_drop: - ALL  # Temporarily commented out for first run" in content:
            print("SearXNG has been initialized. Re-enabling 'cap_drop: - ALL' directive for security...")
            # Uncomment the cap_drop line
            modified_content = content.replace("# cap_drop: - ALL  # Temporarily commented out for first run", "cap_drop: - ALL")
            
            # Write the modified content back
            with open(docker_compose_path, 'w') as file:
                file.write(modified_content)
    
    except Exception as e:
        print(f"Error checking/modifying docker-compose.yml for SearXNG: {e}")

def main():
    parser = argparse.ArgumentParser(description='Start the local AI and Supabase services.')
    parser.add_argument('--profile', choices=['cpu', 'gpu-nvidia', 'gpu-amd', 'none'], default='cpu',
                      help='Profile to use for Docker Compose (default: cpu)')
    args = parser.parse_args()

    clone_supabase_repo()
    prepare_supabase_env()
    
    # Generate SearXNG secret key and check docker-compose.yml
    generate_searxng_secret_key()
    check_and_fix_docker_compose_for_searxng()
    
    stop_existing_containers()
    
    # Create a shared network
    create_shared_network()
    
    # Start Supabase first
    start_supabase()
    
    # Give Supabase some time to initialize
    print("Waiting for Supabase to initialize...")
    time.sleep(10)
    
    # Then start the local AI services
    start_local_ai(args.profile)

if __name__ == "__main__":
    main()