"""
Telegram Message Splitter
Splits Telegram JSON export into multiple markdown files based on greeting detection.
"""

import json
import re
import os
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict


GREETINGS = [
    'привет', 'приветик', 'приветствую', 'здравствуй', 'здравствуйте',
    'доброе утро', 'добрый день', 'добрый вечер', 'хай', 'ку', 'салют',
    'здорово', 'дарова', 'приветули', 'hi', 'hello', 'hey', 'hiya',
    'howdy', 'greetings', 'good morning', 'good afternoon', 'good evening',
    'yo', 'sup', "what's up", 'whatsup', 'hello there', 'hi there',
]


def extract_text(text_field: any) -> str:
    """Extract plain text from message text field (string or list of entities)."""
    if isinstance(text_field, str):
        return text_field
    elif isinstance(text_field, list):
        result = []
        for item in text_field:
            if isinstance(item, str):
                result.append(item)
            elif isinstance(item, dict) and 'text' in item:
                result.append(item['text'])
        return ''.join(result)
    return ''


def process_telegram_export(json_path: str, min_gap: int = 10) -> None:
    """Main processing function."""
    # Compile greeting pattern
    escaped_greetings = [re.escape(g) for g in GREETINGS]
    pattern = r'\b(' + '|'.join(escaped_greetings) + r')\b'
    greeting_pattern = re.compile(pattern, re.IGNORECASE | re.UNICODE)

    # Load JSON
    print(f"Loading {json_path}...")
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    name = data.get('name', 'unknown')
    chat_id = data.get('id', 0)
    messages = data.get('messages', [])

    print(f"Chat: {name} (ID: {chat_id})")
    print(f"Total messages: {len(messages)}")

    # Filter messages with text
    messages = [msg for msg in messages if extract_text(msg.get('text', '')).strip()]
    if not messages:
        print("No messages with text found")
        return

    # Merge consecutive messages from same sender within 30 minutes
    merged_messages = []
    for msg in messages:
        # Skip if has reply - don't merge reply messages
        if msg.get('reply_to_message_id'):
            merged_messages.append(msg)
            continue

        # Check if can merge with previous
        if merged_messages and not merged_messages[-1].get('reply_to_message_id'):
            prev = merged_messages[-1]

            # Same sender?
            if prev.get('from') == msg.get('from'):
                try:
                    prev_time = datetime.fromisoformat(prev.get('date', ''))
                    curr_time = datetime.fromisoformat(msg.get('date', ''))
                    time_diff = (curr_time - prev_time).total_seconds() / 60  # minutes

                    if time_diff <= 30:
                        # Merge: concat texts
                        prev_text = extract_text(prev.get('text', ''))
                        curr_text = extract_text(msg.get('text', ''))
                        prev['text'] = f"{prev_text}\n{curr_text}"
                        continue
                except (ValueError, TypeError, KeyError):
                    pass

        merged_messages.append(msg)

    messages = merged_messages
    print(f"After merging consecutive messages: {len(messages)}")

    # Split by greetings first
    print(f"\nSplitting messages (min gap: {min_gap})...")
    greeting_splits = []
    current_group = []
    last_greeting_idx = -min_gap - 1

    for idx, msg in enumerate(messages):
        text = extract_text(msg.get('text', ''))

        if greeting_pattern.search(text[:100].strip()):
            gap = idx - last_greeting_idx
            if gap > min_gap and current_group:
                greeting_splits.append(current_group)
                current_group = [msg]
                last_greeting_idx = idx
            else:
                current_group.append(msg)
                if gap > min_gap:
                    last_greeting_idx = idx
        else:
            current_group.append(msg)

    if current_group:
        greeting_splits.append(current_group)

    # Further split each greeting group by day
    final_splits = []
    for split in greeting_splits:
        if not split:
            continue

        # Group by date
        daily_groups = {}
        for msg in split:
            try:
                msg_date = datetime.fromisoformat(msg.get('date', '')).date()
                if msg_date not in daily_groups:
                    daily_groups[msg_date] = []
                daily_groups[msg_date].append(msg)
            except (ValueError, TypeError, KeyError):
                # If no valid date, add to last group or create new
                if daily_groups:
                    last_date = max(daily_groups.keys())
                    daily_groups[last_date].append(msg)
                else:
                    daily_groups[datetime.now().date()] = [msg]

        # Convert to sorted list of groups
        for date in sorted(daily_groups.keys()):
            final_splits.append(daily_groups[date])

    # Merge splits that have reply relationships
    merged = True
    while merged:
        merged = False
        i = 1
        while i < len(final_splits):
            # Get all message IDs from previous split
            prev_ids = {msg['id'] for msg in final_splits[i-1]}

            # Check if any message in current split replies to previous split
            has_reply_to_prev = any(
                msg.get('reply_to_message_id') in prev_ids
                for msg in final_splits[i]
            )

            if has_reply_to_prev:
                # Merge current split into previous
                final_splits[i-1].extend(final_splits[i])
                final_splits.pop(i)
                merged = True
            else:
                i += 1

    print(f"Created {len(final_splits)} splits")

    # Create output folder
    safe_name = re.sub(r'[^\w\s-]', '', name).strip().replace(' ', '_')
    output_path = Path(f"output_telegram_{safe_name}_{chat_id}")
    output_path.mkdir(exist_ok=True)
    print(f"\nOutput folder: {output_path}")

    # Process each split
    for idx, msgs in enumerate(final_splits):
        print(f"\nProcessing split {idx+1}/{len(final_splits)} ({len(msgs)} messages)...")

        # Reorder by reply threads
        msg_by_id = {msg['id']: msg for msg in msgs}
        replies = defaultdict(list)
        root_messages = []

        for msg in msgs:
            reply_to = msg.get('reply_to_message_id')
            if reply_to and reply_to in msg_by_id:
                replies[reply_to].append(msg)
            else:
                root_messages.append(msg)

        def collect_thread(msg):
            result = [msg]
            if msg['id'] in replies:
                for reply in sorted(replies[msg['id']], key=lambda m: m['id']):
                    result.extend(collect_thread(reply))
            return result

        ordered = []
        for root in sorted(root_messages, key=lambda m: m['id']):
            ordered.extend(collect_thread(root))

        # Generate filename from message content
        words = []
        for msg in ordered[:5]:
            text = extract_text(msg.get('text', ''))
            text = greeting_pattern.sub('', text)
            words.extend(re.findall(r'[a-zа-яё0-9]+', text.lower(), re.UNICODE))
            if len(words) >= 10:
                break

        stop_words = {'a', 'an', 'the', 'is', 'are', 'was', 'were', 'и', 'в', 'на', 'с', 'по'}
        meaningful = [w for w in words if w not in stop_words and len(w) > 2][:4]
        filename_part = '_'.join(meaningful if meaningful else ['dialog'])[:50]
        filename = f"{idx+1:02d}_dialog_{filename_part}.md"

        # Format as markdown
        try:
            first_date = datetime.fromisoformat(ordered[0].get('date', ''))
            last_date = datetime.fromisoformat(ordered[-1].get('date', ''))
            date_range = f"{first_date.strftime('%Y-%m-%d')} - {last_date.strftime('%Y-%m-%d')}"
        except (ValueError, TypeError, KeyError):
            date_range = 'Date unknown'

        lines = [
            f"# Dialog ({date_range})",
            '',
            f"*{len(ordered)} messages*",
            '',
            '---',
            ''
        ]

        current_date = None
        for msg in ordered:
            if not extract_text(msg.get('text', '')).strip():
                continue

            # Add date separator
            try:
                msg_date = datetime.fromisoformat(msg.get('date', '')).date()
                if msg_date != current_date:
                    if current_date is not None:
                        lines.append('')
                    lines.append(f"### {msg_date.strftime('%Y-%m-%d')}")
                    lines.append('')
                    current_date = msg_date
            except (ValueError, TypeError, KeyError):
                pass

            # Format message
            sender = msg.get('from', 'Unknown')
            text = extract_text(msg.get('text', ''))
            indent = '  ' if msg.get('reply_to_message_id') else ''

            try:
                dt = datetime.fromisoformat(msg.get('date', ''))
                time_str = dt.strftime('%H:%M')
                lines.append(f"{indent}**{sender}** [{time_str}]: {text}")
            except (ValueError, TypeError):
                lines.append(f"{indent}**{sender}**: {text}")

        # Write file
        output_file = output_path / filename
        output_file.write_text('\n'.join(lines), encoding='utf-8')
        print(f"  ✓ {filename}")

    print(f"\n✓ Done! Created {len(final_splits)} markdown files in {output_path}")


def main():
    """Main entry point."""
    json_path = sys.argv[1] if len(sys.argv) > 1 else 'result.json'

    min_gap = 10
    if len(sys.argv) > 2:
        try:
            min_gap = int(sys.argv[2])
        except ValueError:
            print(f"Warning: Invalid min_gap value, using default: {min_gap}")

    if not os.path.exists(json_path):
        print(f"Error: File not found: {json_path}")
        print(f"\nUsage: python telegram_splitter.py [json_file] [min_gap]")
        print(f"  json_file: Path to Telegram JSON export (default: result.json)")
        print(f"  min_gap: Minimum message gap for split (default: 10)")
        sys.exit(1)

    process_telegram_export(json_path, min_gap)


if __name__ == '__main__':
    main()
