# AWS Services Flash Cards

The `cards.pdf` or the `cards_small.pdf` files in this repository contain print templates for flash cards for all available AWS Services.

## Usage

Print the `cards.pdf` or the `cards_small.pdf` file. Cut out the cards and fold them along the dashed line.

## Use custom print settings

Open the `index.html` file in your web browser. Open the print dialog and adjust the print settings.

## Update the cards

If the cards in this repository are out of date, the generator script can be run to update them. Run these commands in the repository folder.

```bash
# Create a virtual environment
python3 -m venv .venv

# Activate the environment
source .venv/bin/activate

# Install dependencies
python -m pip install -r requirements.txt

# Generate the new index.html file
python generator/main.py
```
