# Challenges

These are the challenges used in the 2019 OpenCTF put on by Neg9 at DEF CON 27.

## Challenge Structure

The source for each challenge is fully contained within its own directory. Each challenge has a common structure, and the top level items of that structure are described below.

| Item | Description |
| -------------- | ----------- |
| `README.md` | Contains name, category, description, and final point value of the challenge. |
| `flag.txt` | Contains the flag so that anyone wanting to check the flag without finding the solution can do so. |
| `dist\` | Contains the files that were distributed on the scoreboard to players during the event. |
| `src\` | Contains the source for anything used in the challenge that wasn't distributed during the event. |
| `SOLUTION.md` | A natural language write-up of how to solve the challenge. |
| `solution/` / `solution.*` / `solve.*` | (Optional) Directory or single-file with a codified solution to the challenge. Sometimes these are hiding within the structure somewhere. |
| `Dockerfile` | A Dockerfile which will create an image that runs the challenge in the same manner it was deployed during the OpenCTF event. |
