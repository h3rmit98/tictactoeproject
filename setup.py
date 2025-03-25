import PyInstaller.__main__
import os

# Determine the platform-specific icon extension
icon_extension = '.ico' if os.name == 'nt' else '.icns'
icon_path = f'icon{icon_extension}' if os.path.exists(f'icon{icon_extension}') else None

# Base arguments for PyInstaller
args = [
    'tictactoe.py',  # Your main Python file
    '--onefile',     # Create a single executable file
    '--windowed',    # Don't show the console window (for GUI applications)
    '--name=TicTacToe',  # Name of the output executable
]

# Add icon if it exists
if icon_path:
    args.append(f'--icon={icon_path}')

# Run PyInstaller
PyInstaller.__main__.run(args)
# ------------------ end of setup.py ------------------

# Step 5: Run the setup script
# python setup.py

