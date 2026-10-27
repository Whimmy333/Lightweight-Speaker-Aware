"""Hand-written demo dialogues. Each pairs with another to show the same words read differently in context.

Gold labels are our own intended readings (MELD label set), shown only as a guide in the demo.
"""

EXAMPLES = {
    "“Fine.” after an argument": [
        ("Maya", "You forgot my birthday. Again.", "anger"),
        ("Leo", "I'm sorry, work has been insane this week.", "sadness"),
        ("Maya", "You said exactly the same thing last year.", "anger"),
        ("Leo", "I'll make it up to you, I promise.", "neutral"),
        ("Maya", "Fine.", "anger"),
    ],
    "“Fine.” after good news": [
        ("Nina", "Guess who just got the job!", "joy"),
        ("Tom", "No way! That's amazing!", "surprise"),
        ("Nina", "I start on Monday. Anyway, how are you doing?", "joy"),
        ("Tom", "Fine.", "neutral"),
    ],
    "“Really?” as shock": [
        ("Chris", "Did you hear back from the doctor?", "neutral"),
        ("Pat", "Yeah. They want to run more tests.", "fear"),
        ("Chris", "What? Why?", "fear"),
        ("Pat", "They found something on the scan.", "sadness"),
        ("Chris", "Really?", "fear"),
    ],
    "“Really?” as delight": [
        ("Sam", "Close your eyes and hold out your hands.", "neutral"),
        ("Alex", "Okay... what is it?", "neutral"),
        ("Sam", "Two tickets to the concert next week.", "joy"),
        ("Alex", "Really?", "surprise"),
        ("Alex", "You're the best, I can't believe it!", "joy"),
    ],
    "A same-speaker mood swing": [
        ("Jordan", "I finally finished the report.", "joy"),
        ("Riley", "Great, the boss just moved the deadline up anyway.", "neutral"),
        ("Jordan", "Wait, what? Since when?", "surprise"),
        ("Riley", "Since this morning. And she wants a second version.", "neutral"),
        ("Jordan", "Oh, that's just perfect.", "anger"),
    ],
}
