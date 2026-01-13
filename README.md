<p align="center">
  <img src="assets/logo.svg" width="200" alt="PenDocX Logo">
</p>

# PenDocX — Pentest Documentation eXtended

PenDocX is a modern, modular penetration testing documentation and reporting tool. It is designed to streamline the process of recording findings during a penetration test and generating professional reports in multiple formats.

## Features

- **Mission Management**: Initialize and manage penetration testing missions easily.
- **Finding Tracking**: Record findings with detailed descriptions, impacts, and remediations.
- **CVSS v3.1 Scoring**: Integrated CVSS calculation logic to automatically determine severity.
- **Compliance Mapping**: Map findings to industry standards like OWASP Top 10 (2021) and SANS Top 25 (CWE).
- **Artifact Support**: Attach artifacts like screenshots and logs to findings.
- **Multi-format Premium Reporting**: Generate reports in Word (`.docx`), HTML, Markdown, and PDF.
- **Offline First**: Designed to work in isolated networks without internet connectivity.
- **Modern CLI & UX**: Powered by Click and Rich for a beautiful, interactive terminal experience.

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

### List Findings

```bash
pendocx list-findings
```

### Generate a Report

```bash
# Premium PDF (default/recommended)
pendocx generate-report --format pdf

# Premium Word report
pendocx generate-report --format word

# Premium HTML report
pendocx generate-report --format html
```

### Export to JSON

```bash
pendocx export-json
```

## Project Structure

- `pendocx/core`: Logging, configuration, CVSS utils, and error handling.
- `pendocx/models`: Pydantic data models and storage logic.
- `pendocx/reporter`: Premium Word, HTML, PDF, and Markdown exporters.
- `pendocx/cli`: Command-line interface implementation.

## Tech Stack

- **CLI**: [Click](https://click.palletsprojects.com/)
- **UI & UX**: [Rich](https://github.com/Textualize/rich)
- **Data Validation**: [Pydantic](https://docs.pydantic.dev/)
- **Templating**: [Jinja2](https://jinja.palletsprojects.com/)
- **Reports**: [python-docx](https://python-docx.readthedocs.io/), [xhtml2pdf](https://github.com/xhtml2pdf/xhtml2pdf)
- **Security**: [cvss](https://pypi.org/project/cvss/)

## License

This project is licensed under the MIT License.
