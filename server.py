#!/usr/bin/env python3
"""
Simple HTTP server to serve the craft baker CV page on port 8081.
"""

import http.server
import socketserver
import os
import sys
from pathlib import Path

# Configuration
PORT = 8081
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler to serve files from the current directory."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        # Add basic security headers
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('X-Frame-Options', 'DENY')
        super().end_headers()

def main():
    """Start the HTTP server."""
    try:
        # Change to the script directory
        os.chdir(DIRECTORY)
        
        # Check if index.html exists
        if not Path('index.html').exists():
            print("Error: index.html not found in the current directory")
            print(f"Current directory: {DIRECTORY}")
            sys.exit(1)
        
        # Create and start the server
        with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
            print(f"🥖 Craft Baker CV Server")
            print(f"📍 Serving directory: {DIRECTORY}")
            print(f"🌐 Server running at: http://localhost:{PORT}")
            print(f"📄 CV available at: http://localhost:{PORT}/index.html")
            print("\nPress Ctrl+C to stop the server")
            
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\n\n🛑 Server stopped by user")
                
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ Error: Port {PORT} is already in use")
            print("Please stop the other process or choose a different port")
        else:
            print(f"❌ Error starting server: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()