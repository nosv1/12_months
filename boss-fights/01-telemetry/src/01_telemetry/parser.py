# FAIL LOUDLY WHEN config.py KNOWN HEADER NOT PRESENT

# row column count needs to match header column count
# When the count is wrong, the message must carry **both** numbers, e.g. `Expected 5 columns, found 4.` — that text gets pasted into a firmware ticket, and the ticket is useless without both.

# If the tool hits a failure it doesn't have a category for, put it in an **unrecognized** bucket with a count, and report that count every time — it should always be zero.
# **Quarantine the row, don't crash.** A
