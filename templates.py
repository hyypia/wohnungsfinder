from parser import Flat

greeting = """Hi! I'am a Wohnungsfinder Bot!
I'll monitoring new flats in Berlin,
which are provided by the 6 largest
real estate developers in Berlin.

Let's adjust your parametrs!

Have you WBS? (https://inberlinwohnen.de/stichwort-wbs/)"""

from_qm_question = """From what number m² of square?
(Answer for example 25.5 format please)"""

to_qm_question = """Up to how many m² of square?
(Answer for example 75.5 format please)"""

from_rooms_question = "From what number of rooms?"

to_rooms_question = "Up to how many rooms?"

end_conversation = "Great! I starting search!"


def flat_message(flat: Flat) -> str:
    return (
        f"{flat.address}\n"
        f"Zimmeranzahl: {flat.rooms}\n"
        f"Wohnfläche: {flat.square}\n"
        f"{flat.url}"
    )
