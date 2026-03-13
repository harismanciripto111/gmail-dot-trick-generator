#!/usr/bin/env python3
"""
Gmail Dot Trick Generator
==========================
Gmail ignores dots in the local part of email addresses.
This tool generates ALL possible dot-placement variations
for any Gmail address using bit manipulation.

For N characters in the local part, there are N-1 possible
dot positions, yielding 2^(N-1) total variations.

Examples:
  "test" (4 chars) -> 3 dot positions -> 2^3 = 8 variations
  "johndoe" (7 chars) -> 6 dot positions -> 2^6 = 64 variations

Usage:
  python dot_generator.py <email> [options]

Options:
  --count       Show only the total count of variations
  --limit N     Limit output to first N variations
  --output FILE Write variations to a file
  --no-header   Skip the summary header
  -h, --help    Show this help message

Pure Python. Zero dependencies.
"""

import sys
import argparse


def clean_email(email: str) -> tuple:
    """
    Parse and clean a Gmail address.

    Strips existing dots from the local part and validates
    that the domain is a Gmail domain.

    Args:
        email: A Gmail address (e.g., 'j.ohn.doe@gmail.com')

    Returns:
        Tuple of (clean_local_part, domain)

    Raises:
        ValueError: If the email format is invalid or not Gmail
    """
    email = email.strip().lower()

    if "@" not in email:
        # Assume @gmail.com if no domain provided
        local_part = email
        domain = "gmail.com"
    else:
        local_part, domain = email.rsplit("@", 1)

    # Validate Gmail domain
    valid_domains = {"gmail.com", "googlemail.com"}
    if domain not in valid_domains:
        raise ValueError(
            f"Not a Gmail address (domain: {domain}). "
            f"Supported domains: {', '.join(sorted(valid_domains))}"
        )

    # Remove existing dots from local part
    clean_local = local_part.replace(".", "")

    if not clean_local:
        raise ValueError("Local part of email is empty after removing dots")

    if len(clean_local) < 2:
        raise ValueError(
            f"Local part '{clean_local}' is too short. "
            "Need at least 2 characters to generate variations."
        )

    return clean_local, domain


def count_variations(local_part: str) -> int:
    """
    Calculate the total number of dot-placement variations.

    For a string of length N, there are N-1 positions where
    a dot can be placed, and each position is either dot or
    no-dot, giving 2^(N-1) combinations.

    Args:
        local_part: Clean local part (no dots)

    Returns:
        Total number of possible variations
    """
    return 1 << (len(local_part) - 1)


def generate_variations(local_part: str, domain: str, limit: int = 0):
    """
    Generate all dot-placement variations using bit manipulation.

    Each integer from 0 to 2^(N-1)-1 represents a unique
    combination of dot placements. Bit j of integer i
    determines whether a dot is placed after character j.

    Args:
        local_part: Clean local part (no existing dots)
        domain: Email domain (e.g., 'gmail.com')
        limit: Maximum number of variations to yield (0 = all)

    Yields:
        Email variations as strings
    """
    n = len(local_part) - 1  # Number of possible dot positions
    total = 1 << n           # 2^n total combinations

    cap = total if limit <= 0 else min(limit, total)

    for i in range(cap):
        result = [local_part[0]]
        for j in range(n):
            if i & (1 << j):
                result.append(".")
            result.append(local_part[j + 1])
        yield "".join(result) + "@" + domain


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="dot_generator",
        description=(
            "Generate all possible dot-placement variations "
            "of a Gmail address using bit manipulation."
        ),
        epilog=(
            "Examples:\n"
            "  python dot_generator.py test@gmail.com\n"
            "  python dot_generator.py johndoe --limit 10\n"
            "  python dot_generator.py user@gmail.com --count\n"
            "  python dot_generator.py user@gmail.com --output emails.txt\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "email",
        help="Gmail address (e.g., 'user@gmail.com' or just 'user')",
    )
    parser.add_argument(
        "--count",
        action="store_true",
        help="Show only the total count of possible variations",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        metavar="N",
        help="Limit output to first N variations (0 = all)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        metavar="FILE",
        help="Write variations to a file instead of stdout",
    )
    parser.add_argument(
        "--no-header",
        action="store_true",
        help="Skip the summary header in output",
    )

    args = parser.parse_args()

    # Parse and clean the email
    try:
        local_part, domain = clean_email(args.email)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    total = count_variations(local_part)
    dot_positions = len(local_part) - 1

    # Count-only mode
    if args.count:
        if not args.no_header:
            print(f"Email: {local_part}@{domain}")
            print(f"Clean local part: {local_part} ({len(local_part)} chars)")
            print(f"Dot positions: {dot_positions}")
        print(f"Total variations: {total}")
        return

    # Determine how many to generate
    cap = total if args.limit <= 0 else min(args.limit, total)

    # Generate and output variations
    if args.output:
        # Write to file
        written = 0
        with open(args.output, "w") as f:
            for variation in generate_variations(local_part, domain, cap):
                f.write(variation + "\n")
                written += 1
        print(f"Wrote {written} of {total} variations to {args.output}")
    else:
        # Print to stdout
        if not args.no_header:
            if args.limit > 0:
                print(f"Showing {cap} of {total} variations "
                      f"for {local_part}@{domain}:\n")
            else:
                print(f"All {total} variations "
                      f"for {local_part}@{domain}:\n")

        for variation in generate_variations(local_part, domain, cap):
            print(variation)


if __name__ == "__main__":
    main()
