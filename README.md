🖥️ Clockify Actions GUI

This project provides a Graphical User Interface (GUI) for adding time entries to users within a specified Clockify workspace. Designed to simplify and streamline time tracking, the tool leverages the Clockify API to perform operations efficiently.

📂 Project Structure

    run.py
    Main script to launch the GUI application.

    ConsoleBase.json
    Configuration file for the console or workspace settings.

    Directories:
        _lib: Contains supporting libraries and Python scripts for API interactions.
        _images: Stores images for documentation or UI elements.
        __pycache__: Compiled Python files.

    requirements.txt
    List of dependencies required for the project.

🚀 Features

    GUI Interface:
    User-friendly interface for adding time entries to Clockify users.

    Workspace Management:
    Add and manage entries within a specified workspace.

    Clockify API Integration:
    Seamlessly interacts with the Clockify API for operations.

    Configuration File:
    Easy-to-edit ConsoleBase.json for workspace settings.

🔧 Prerequisites

    Python 3.x

    Dependencies:
    Install the required libraries:

    pip install -r requirements.txt

    Clockify API Key
        Obtain your API key from your Clockify account settings.

⚙️ How to Use

    Set Up Configuration:
        Edit ConsoleBase.json to include your Clockify workspace details and API key.

    Run the Application:

    python run.py

    Use the GUI:
        Follow the prompts in the GUI to add time entries for users.

📊 Output

    Time Entry Logs:
    Logs of successful time entries within the workspace.

    Visual Feedback:
    Real-time feedback on operations via the GUI.

🔒 Security

    API Key: Keep your API key secure.
    Data Privacy: Ensure sensitive information is protected and accessed only by authorized users.

🤝 Contributing

Contributions are welcome! If you have suggestions or find issues, please submit a pull request or open an issue.

📝 License

This project is licensed under the MIT License.
