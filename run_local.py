import subprocess
import sys
import os
import http.server
import socketserver

def kill_previous_instances(port=8000):
    """Kill any previous instances of the server running on the specified port"""
    try:
        # Find processes using the port
        if sys.platform == "darwin":  # macOS
            result = subprocess.run(['lsof', '-ti', f':{port}'], 
                                  capture_output=True, text=True)
            if result.stdout.strip():
                pids = result.stdout.strip().split('\n')
                for pid in pids:
                    try:
                        subprocess.run(['kill', '-9', pid], check=True)
                        print(f"Killed previous instance with PID {pid}")
                    except subprocess.CalledProcessError:
                        pass
        elif sys.platform == "linux":
            result = subprocess.run(['fuser', '-k', f'{port}/tcp'], 
                                  capture_output=True, text=True)
        elif sys.platform == "win32":
            result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True)
            lines = result.stdout.split('\n')
            for line in lines:
                if f':{port}' in line and 'LISTENING' in line:
                    parts = line.split()
                    if len(parts) > 4:
                        pid = parts[4]
                        try:
                            subprocess.run(['taskkill', '/PID', pid, '/F'], check=True)
                            print(f"Killed previous instance with PID {pid}")
                        except subprocess.CalledProcessError:
                            pass
    except Exception as e:
        print(f"Error killing previous instances: {e}")

def main():
    # Kill any previous instances
    kill_previous_instances(port=8000)
    
    # Update data
    print("Updating momentum data...")
    try:
        subprocess.run([sys.executable, 'fetch_data.py'], check=True)
        print("Data updated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error updating data: {e}")
        return
    
    # Start server
    port = 8000
    os.chdir('.')
    with socketserver.TCPServer(("", port), http.server.SimpleHTTPRequestHandler) as httpd:
        print(f"Serving momentum site on http://localhost:{port}")
        print("Press Ctrl+C to stop.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Server stopped.")

if __name__ == '__main__':
    main()
