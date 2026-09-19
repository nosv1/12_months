# rejected reading
# 1. **The line number in the original file.** Not the index after filtering. We open the file at that line.
# 2. **The reason in plain words.** This goes into a firmware ticket that a vendor engineer reads.
# 3. **The row exactly as it appeared in the file.** Not rebuilt from parsed fields — if it round-trips through your parser we no longer know what the robot actually wrote, and that's the whole evidence for the ticket.
# Group rejected rows **under the robot** when we know which robot it was. When the row is so broken we can't tell — that's what a truncated row looks like — list it **separately**. **Never invent a robot** to file it under, and never file it under a guess.

# Every rejected row carries a **list** of errors, always, even when there is only one.
