# Gmail Dot Trick Generator

Simple CLI tool to generate all possible dot-placement variations of any Gmail address. Pure Python, zero dependencies.

## How It Works

Gmail ignores dots (`.`) in the local part of email addresses. This means:
- `johndoe@gmail.com`
- `john.doe@gmail.com`
- `j.o.h.n.d.o.e@gmail.com`

All deliver to the **same inbox**. Many websites treat these as different emails.

For a local part with N characters, there are N-1 possible dot positions, giving **2^(N-1)** total variations.

| Local Part | Characters | Dot Positions | Variations |
|-----------|------------|---------------|------------|
| `ab` | 2 | 1 | 2 |
| `test` | 4 | 3 | 8 |
| `johndoe` | 7 | 6 | 64 |
| `username` | 8 | 7 | 128 |

## Installation

```bash
git clone https://github.com/harismanciripto111/gmail-dot-trick-generator.git
cd gmail-dot-trick-generator
```

No dependencies to install -- pure Python 3.

## Usage

### Generate All Variations

```bash
python dot_generator.py test@gmail.com
```

Output:
```
All 8 variations for test@gmail.com:

test@gmail.com
t.est@gmail.com
te.st@gmail.com
t.e.st@gmail.com
tes.t@gmail.com
t.es.t@gmail.com
te.s.t@gmail.com
t.e.s.t@gmail.com
```

### Count Variations Only

```bash
python dot_generator.py test@gmail.com --count
```

Output:
```
Email: test@gmail.com
Clean local part: test (4 chars)
Dot positions: 3
Total variations: 8
```

### Limit Output

```bash
python dot_generator.py johndoe@gmail.com --limit 5
```

### Save to File

```bash
python dot_generator.py johndoe@gmail.com --output emails.txt
```

### Shorthand (Domain Optional)

```bash
# These are equivalent:
python dot_generator.py johndoe@gmail.com
python dot_generator.py johndoe
```

## CLI Options

| Option | Description |
|--------|-------------|
| `email` | Gmail address or just the local part |
| `--count` | Show only the total count of variations |
| `--limit N` | Limit output to first N variations |
| `--output FILE` | Write variations to a file |
| `--no-header` | Skip the summary header |
| `-h, --help` | Show help message |

## Algorithm

Uses **bit manipulation** for efficient generation:
- Each integer from `0` to `2^(N-1) - 1` maps to a unique dot pattern
- Bit `j` of integer `i` determines if a dot is placed after character `j`
- Generates variations lazily using Python generators (memory efficient)

## Supported Domains

- `gmail.com`
- `googlemail.com`

## License

MIT License -- see [LICENSE](LICENSE) for details.
