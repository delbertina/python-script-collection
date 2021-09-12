# delbertina's Python Script Collection

## UUID Convert to Int Array
- Select an input file with 1 command per line
- Commands are Minecraft give player head commands that use the <1.16 format of UUIDs
- Outputs a file with the commands changed over to the new 1.16 UUID int array format using 2's compliment

## Give Head Int Array UUID to VotingPlugin Item Head
- Select an input file with 1 command per line
- Commands are Minecraft give player head commands with custom texture data
- Outputs a file in JSON format with the command converted to a random item from list of heads
- Give file intended to be used with the Spigot VotingPlugin
- Commands do not need to have a specific UUID format as that is ignored

## Polygon to SQL Queries
- Currently very rigid ... TODO: Fix that
- Select an input file that has lists of cartesian points one per line
- Each list of points should have a header line in format `some-name:`
- Outputs a list of SQL queries to delete data found within the polygons from a database
- Each output query is essentially a line. Would be way faster SQL-wise to find rectangles instead.
- Originally made to delete data from a CoreProtect's (Spigot plugin) database
