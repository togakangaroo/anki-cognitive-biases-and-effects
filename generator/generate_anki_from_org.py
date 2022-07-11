import re
import genanki
import os
from contextlib import suppress
from typing import Iterator

org_table_header_row = re.compile('^\\s*\\|' '-+\\+-+\\+-+\\+-+' '\\|\\s*$')
org_table_row = re.compile('^\\s*\\|'
                           '\\s*(.*?)\\s*\\|'
                           '\\s*(.*?)\\s*\\|'
                           '\\s*(.*?)\\s*\\|'
                           '\\s*(.*?)\\s*\\|'
                           '\\s*$')

term_model = genanki.Model(
    505739646,
    'Cognitive Biases',
    fields=[
        {'name': 'Question'},
        {'name': 'Answer'},
        {'name': 'Link'}
    ],
    templates=[{
        'name': 'Card 1',
        'qfmt': '{{Question}}',
        'afmt': '''
            <a href="{{Link}}" target=_blank>{{FrontSide}}</a>
            <hr id="answer">
            {{Answer}}''',

    }],
    css='''
        .card {
            font-size: 150%;
        }
    '''
)


def _fast_forward_past_table_header(lines: Iterator[str]) -> bool:
    for line in lines:
        if org_table_header_row.match(line):
            return True
    return False



def _read_notes(lines: Iterator[str]):

    if not _fast_forward_past_table_header(lines):
        return

    for line in lines:
        m = org_table_row.match(line)
        cells = m and m.groups() or tuple()

        if len(cells) != 4:
            continue

        term, link, definition, guid = cells

        yield genanki.Note(model=term_model, fields=[term, definition, link], guid=guid)


def generate_deck():
    file_name = 'cognitive_biases.apkg'

    deck = genanki.Deck(1312277299, 'Cognitive Biases')
    with open(f'../README.org', 'r') as f:
        for note in _read_notes(iter(f.readlines())):
            deck.add_note(note)

    with suppress(FileNotFoundError):
        os.remove(file_name)
        genanki.Package(deck).write_to_file(file_name)

    print(f'Wrote {os.path.getsize(file_name)} bytes to {file_name}')

if __name__ == "__main__":
    generate_deck()
