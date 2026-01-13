# PenDocX — Pentest Documentation eXtended

PenDocX is a modern, modular penetration testing documentation and reporting tool. It is designed to streamline the process of recording findings during a penetration test and generating professional reports in multiple formats.

## Features

- **Mission Management**: Initialize and manage penetration testing missions easily.
- **Finding Tracking**: Record findings with detailed descriptions, impacts, and remediations.
- **Artifact Support**: Attach artifacts like screenshots and logs to findings.
- **Multi-format Reporting**: Generate reports in Word (`.docx`), HTML, and Markdown.
- **Offline First**: Designed to work in isolated networks without internet connectivity.
- **Modular Architecture**: Built with Python 3.11+, using Pydantic for data models and Jinja2 for templating.

## Installation

### Prerequisites
- Python 3.11 or higher

### Setup

```bash
# Clone the repository
git clone https://github.com/ismailtsdln/PenDocX.git
cd PenDocX

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install .
```

## CLI Usage

### Initialize a Project
```bash
pendocx init
```

### Add a Finding
```bash
pendocx add-test
```

### Generate a Report
```bash
# Word report (default)
pendocx generate-report --format word

# HTML report
pendocx generate-report --format html

# Markdown report
pendocx generate-report --format md
```

### Export to JSON
```bash
pendocx export-json
```

## Project Structure

- `pendocx/core`: Logging, configuration, and error handling.
- `pendocx/models`: Pydantic data models and storage logic.
- `pendocx/reporter`: Report generation logic for different formats.
- `pendocx/cli`: Command-line interface implementation.

## Tech Stack

- **CLI**: [Click](https://click.palletsprojects.com/)
- **UI**: [Rich](https://github.com/Textualize/rich)
- **Data Validation**: [Pydantic](https://docs.pydantic.dev/)
- **Templating**: [Jinja2](https://jinja.palletsprojects.com/)
- **Word Reports**: [python-docx](https://python-docx.readthedocs.io/)

## License

This project is licensed under the MIT License.
