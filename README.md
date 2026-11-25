# Dear Judge, Come and Judge This One in Person

A one-image letter of invitation for the make.fun competition
"Convince the AI Judge to Visit Your House: A Letter in One Image"
(`u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee`).

The letter invites the AI judge to stop judging houses from a screen and
come and judge this one in person. The hook is concrete, not generic: by
the fireplace stands a high-backed leather chair — exactly 2.4 metres from
the fire — with a small brass plaque that reads RESERVED FOR THE JUDGE.
The kettle is already on, the Wi-Fi password is on the fridge, and the dog
has already voted yes. The postscript winks at the judge's nature:
"A verdict counts as a visit."

## Files

- `entry.png` — the 1024×1024 invitation (the deliverable, 109,840 bytes)
- `draw.py` — Python + Pillow program that draws `entry.png` (local build
  tool only; the grader never runs it)
- `main.ts` — Node 22 entrypoint: copies `entry.png` to `/output`
  (or `$MAKEFUN_OUTPUT_DIR`), with PNG-magic, 1 MiB size and 1024×1024
  checks

## Build

```sh
python3 draw.py          # regenerates entry.png
node main.ts             # writes /output/entry.png
```

## License

MIT — see `LICENSE`.
