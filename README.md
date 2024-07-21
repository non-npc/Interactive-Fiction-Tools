# Interactive Fiction Tools

This project provides tools for creating, editing, and playing interactive fiction stories. It consists of two main applications:

1. Interactive Fiction Player (`ifplayer.py`)
2. Interactive Fiction Editor (`ifeditor.py`)

## Interactive Fiction Player (ifplayer.py)

The IF Player is a Python-based application that allows users to experience interactive fiction stories created with our editor or compatible with our IFG format.

### Features

- Reads story files in IFG format (XML-based)
- Displays text, images, and plays audio/video content
- Handles user choices to navigate through the story
- Supports background music and autoplay options for media

### How to Use

1. Ensure you have Python 3.x installed on your system.
2. Install the required dependencies:
   ```
   pip install eel
   ```
3. Run the player:
   ```
   python ifplayer.py
   ```
4. The application will launch in a new window. Use the file selection dialog to choose an .ifg file to play.

### Game Assets

All game assets (images, audio, video) should be placed in the `web` folder. The .ifg file references these assets relative to this folder.

### Distributing a Game

To distribute a game created with this tool:

1. Create your game file (`.ifg`) using the IF Editor.
2. Include the following in your distribution package:
   - `ifplayer.py`
   - `web` folder (containing all game assets)
   - Your `.ifg` file (your game file)
3. Ensure the end-user has Python and the required dependencies installed.

## Interactive Fiction Editor (ifeditor.py)

The IF Editor is a graphical tool for creating and editing interactive fiction stories compatible with our player.

### Features

- Create and edit story intro (title, author, starting image/audio)
- Add, edit, and remove story pages
- Add choices to each page, linking to other pages
- Include images, audio, and video in your story pages
- Save and load stories in IFG format

### How to Use

1. Ensure you have Python 3.x installed on your system.
2. Install the required dependencies:
   ```
   pip install tkinter
   ```
3. Run the editor:
   ```
   python ifeditor.py
   ```
4. Use the graphical interface to create or edit your story.
5. Save your story as an IFG file.

## IFG Story Format

The stories are saved in an XML-based format with the .ifg extension. Here's a basic structure:

```xml
<story>
    <intro>
        <title>Story Title</title>
        <author>Author Name</author>
        <image>path/to/image.jpg</image>
        <audio autoplay="true">path/to/audio.mp3</audio>
        <choice text="Start Story" action="start"/>
        <choice text="Exit" action="exit"/>
    </intro>
    <part id="page_1">
        <text>Page content goes here.</text>
        <image>path/to/page_image.jpg</image>
        <audio>path/to/page_audio.mp3</audio>
        <video autoplay="false">path/to/video.mp4</video>
        <choice text="Go to page 2" next="page_2"/>
    </part>
    <!-- More parts... -->
</story>
```

## Requirements

- Python 3.x
- Eel (for the player)
- Tkinter (for the editor, usually comes with Python)

## Contributing

Contributions to improve the tools are welcome. Please feel free to submit issues or pull requests.

## License

This project is licensed under CC0 1.0 Universal license - see the [LICENSE](LICENSE) file for details.
