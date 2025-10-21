#!/usr/bin/env python3
"""
Nexus AI Chat Conversation Splitter

This script splits Nexus AI conversation markdown files into structured folders.
Input: Single file or glob pattern (e.g., '*.md', '20250717*.md')
Output: ./output/filename/ folder with:
  - meta_information.md (YAML metadata)
  - 01_first_conversation.md, 02_second_conversation.md, etc.
"""

import glob as glob_module
import logging
import re
import sys
from pathlib import Path


# Constants
DEFAULT_CONVERSATION_NAME = "conversation"
CONVERSATION_SEPARATOR = '\n\n---\n\n'

# Pre-compiled regex patterns for performance
SPECIAL_CHARS_PATTERN = re.compile(r'[>#\[\]!*`]')
NON_WORD_PATTERN = re.compile(r'[^\w\-]')
MULTIPLE_UNDERSCORES_PATTERN = re.compile(r'_+')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)


def extract_metadata(content: str) -> tuple[str, str]:
    """
    Extract YAML metadata from the beginning of the file.

    Args:
        content: Full file content

    Returns:
        Tuple of (metadata, remaining_content)
    """
    # Optimize: Use find to locate markers instead of splitting entire file
    first_marker_pos = content.find('---\n')
    if first_marker_pos != 0:
        # Metadata must start at beginning of file
        return "", content

    # Find second marker after the first
    second_marker_pos = content.find('\n---\n', first_marker_pos + 4)
    if second_marker_pos == -1:
        # Also check for --- at end of line
        second_marker_pos = content.find('\n---', first_marker_pos + 4)
        if second_marker_pos == -1:
            return "", content
        # Check if this is truly the end marker
        end_check = second_marker_pos + 4
        if end_check < len(content) and content[end_check] not in ('\n', '\r'):
            return "", content
        metadata = content[:end_check]
        remaining = content[end_check:].lstrip('\n')
    else:
        metadata = content[:second_marker_pos + 5]  # Include \n---\n
        remaining = content[second_marker_pos + 5:]

    return metadata, remaining


def split_conversations(content: str) -> list[str]:
    """
    Split content into conversation blocks where each block contains:
    - One user request (>[!nexus_user])
    - All following agent responses (>[!nexus_agent]) until the next user request

    Args:
        content: Content after metadata removal

    Returns:
        List of conversation blocks (user + agent responses)
    """
    # Optimize: Split by separator directly, then process blocks
    # Split on standalone --- lines
    parts = content.split('\n---\n')

    # Filter out empty blocks early
    raw_blocks = [block.strip() for block in parts if block.strip()]

    # Group blocks into conversations
    conversations = []
    current_conversation = []
    user_marker = '>[!nexus_user]'

    for block in raw_blocks:
        if user_marker in block:
            # Start new conversation if we have a previous one
            if current_conversation:
                conversations.append(CONVERSATION_SEPARATOR.join(current_conversation))
            current_conversation = [block]
        elif current_conversation:
            # Add to current conversation if one exists
            current_conversation.append(block)

    # Finalize last conversation
    if current_conversation:
        conversations.append(CONVERSATION_SEPARATOR.join(current_conversation))

    return conversations


def extract_user_question(block: str) -> str:
    """
    Extract the user's question from a conversation block.

    Args:
        block: Conversation block text

    Returns:
        First line of user question text
    """
    # Optimize: Find marker position and extract from there
    marker_pos = block.find('>[!nexus_user]')

    if marker_pos != -1:
        # Find the next line with content after the marker
        after_marker = block[marker_pos + len('>[!nexus_user]'):]
        lines = after_marker.split('\n', 10)  # Only split first 10 lines

        for line in lines[1:]:  # Skip first line (rest of marker line)
            text_line = line.strip()
            if text_line and text_line.startswith('>'):
                return text_line.lstrip('> ').strip()

    # Fallback: find first non-empty, non-header line
    for line in block.split('\n', 20):  # Limit search to first 20 lines
        clean_line = line.strip()
        if clean_line and not clean_line.startswith('#'):
            return clean_line

    return DEFAULT_CONVERSATION_NAME


def sanitize_filename(text: str, max_words: int = 4, word_separator: str = ' ') -> str:
    """
    Create a safe filename from text.

    Args:
        text: Input text
        max_words: Maximum number of words to include
        word_separator: Separator to join words (default: space)

    Returns:
        Sanitized filename
    """
    # Optimize: Use pre-compiled regex patterns
    text = SPECIAL_CHARS_PATTERN.sub('', text)
    words = text.split()
    selected_words = words[:max_words]
    filename = word_separator.join(selected_words)
    filename = NON_WORD_PATTERN.sub('_', filename)
    filename = MULTIPLE_UNDERSCORES_PATTERN.sub('_', filename)
    filename = filename.strip('_')

    if not filename:
        return DEFAULT_CONVERSATION_NAME

    if len(filename) > 50:
        filename = filename[:50].rstrip('_')

    return filename.lower()


def split_file(input_path: Path, folder_suffix: str = '', output_dir: Path = None) -> None:
    """
    Split a Nexus conversation file into a structured folder.

    Args:
        input_path: Path to input markdown file
        folder_suffix: Optional suffix to append to output folder name
        output_dir: Base output directory (defaults to ./output)
    """
    if not input_path.exists():
        logging.error(f"File '{input_path}' not found")
        sys.exit(1)

    if not input_path.suffix == '.md':
        logging.error("File must be a .md file")
        sys.exit(1)

    logging.info(f"Reading file: {input_path}")
    content = input_path.read_text()

    logging.info("Extracting metadata...")
    metadata, remaining = extract_metadata(content)

    logging.info("Splitting conversations...")
    blocks = split_conversations(remaining)
    logging.info(f"Found {len(blocks)} conversation blocks")

    # Default output directory is ./output
    if output_dir is None:
        output_dir = Path.cwd() / "output"

    folder_name = input_path.stem + folder_suffix if folder_suffix else input_path.stem
    output_folder = output_dir / folder_name
    logging.info(f"Creating output folder: {output_folder}")
    output_folder.mkdir(parents=True, exist_ok=True)

    if metadata:
        meta_file = output_folder / "meta_information.md"
        logging.info(f"Saving metadata to: {meta_file.name}")
        meta_file.write_text(metadata)

    for i, block in enumerate(blocks, start=1):
        question = extract_user_question(block)
        safe_name = sanitize_filename(question)
        filename = f"{i:02d}_{safe_name}.md"
        file_path = output_folder / filename

        logging.info(f"Saving: {filename}")
        file_path.write_text(block)

    logging.info(f"\nSuccessfully split into {len(blocks)} files in: {output_folder}")


def main():
    """Main entry point."""
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python splitter.py <input_pattern> [folder_suffix]")
        print("\nInput can be a single file or glob pattern (e.g., '*.md')")
        print("Output folders will be created in: ./output/filename/")
        print("\nExamples:")
        print("  python splitter.py 'conversation.md'")
        print("  python splitter.py '*.md'")
        print("  python splitter.py '20250717*.md'")
        print("  python splitter.py 'conversation.md' '_backup'")
        sys.exit(1)

    input_pattern = sys.argv[1]
    folder_suffix = sys.argv[2] if len(sys.argv) == 3 else ''

    # Handle glob patterns
    matched_files = glob_module.glob(input_pattern)

    if not matched_files:
        logging.error(f"No files found matching pattern: {input_pattern}")
        sys.exit(1)

    # Filter for .md files only
    md_files = [Path(f) for f in matched_files if f.endswith('.md')]

    if not md_files:
        logging.error(f"No .md files found matching pattern: {input_pattern}")
        sys.exit(1)

    logging.info(f"Found {len(md_files)} file(s) to process\n")

    for file_path in md_files:
        logging.info(f"{'='*60}")
        logging.info(f"Processing: {file_path.name}")
        logging.info(f"{'='*60}")
        split_file(file_path, folder_suffix)
        logging.info("")


if __name__ == "__main__":
    main()
