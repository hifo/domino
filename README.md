# Domino Spellbook Maker

A lightweight Flask app for assembling a printable spellbook reference sheet. The project is designed around a spell-selection interface with multiple columns, making it easy to organize and select spells.

## Overview

Domino is a simple web application for managing and reviewing spells in a format that feels like a tabletop reference page. It is intentionally easy to extend, making it a strong foundation for future features such as spell filtering, custom book layouts, and printable export options.

## Features

- Flask-based web application
- Multi-column spell selection layout
- Circle-based spell organization
- Clean, readable spellbook-style interface
- Easy to extend with real spell data and additional logic

## Screenshot

This project is designed to evolve into a polished spellbook UI.

## Getting Started

1. Create and activate a virtual environment.
2. Install dependencies:
   `pip install -r requirements.txt`
3. Start the app:
   `python main.py`
4. Open `http://127.0.0.1:5000` in your browser.

## Usage

The home page shows a set of spell dropdowns arranged in multiple columns. Each dropdown starts with a default value of `Choose A Spell`, making the layout ready for expansion with actual spell data, custom spell lists, or a full spellbook builder workflow.

## Project Structure

- `main.py`: Starts the Flask application.
- `app/__init__.py`: Creates the app and defines the home route.
- `app/templates/index.html`: Main page layout for the spellbook interface.
- `app/static/style.css`: Styling for the page and spell columns.
- `requirements.txt`: Python dependencies for the app.

## Future Enhancements

- Add real spell data and categories
- Add print-friendly output for spellbook pages
- Include save/load functionality for custom spell lists
- Add search and sorting tools for quick lookup

## Notes

This project is a flexible starter for a  spellbook tool and is intended to grow into a more complete spell management application.
