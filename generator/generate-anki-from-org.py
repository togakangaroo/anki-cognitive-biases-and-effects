import re
import genanki
import os

def generate_deck():
    file_name = 'cognitive_biases.apkg'

    term_model = genanki.Model(
    505739646,
    'Cognitive Biases',
    fields=[
        {'name': 'Question'},
        {'name': 'Answer'},
    ],
    templates=[
        {
        'name': 'Card 1',
        'qfmt': '{{Question}}',
        'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
        },
    ])
    deck = genanki.Deck(1312277299, 'Cognitive Biases')
    two_col_org_row = re.compile('^\\s*\\|\\s*(.*?)\\s*\\|\\s*(.*?)\\s*\\|\\s*$')
    with open(f'../biases.org', 'r') as f:
        extracted_cells = (m.groups()
                        for m in (two_col_org_row.match(l)
                                    for l in f.readlines())
                        if m)
        term_definitions = (g for g in extracted_cells if len(g) == 2)

        notes = (genanki.Note(model=term_model, fields=[term, definition])
                for (term, definition) in term_definitions)
        for note in notes:
            deck.add_note(note)

    genanki.Package(deck).write_to_file(file_name)

    print(f'Wrote {os.path.getsize(file_name)} bytes to {file_name}')

if __name__ == "__main__":
    generate_deck()
