
# Ethereum Vanity Address Filter

This Python script filters Ethereum addresses based on specific patterns often sought in *vanity* address generation. It supports multiprocessing for performance and writes matches to categorized `.txt` files.

### 🔍 What It Does

The script reads a list of Ethereum addresses (in the format: `address privatekey` on each line), then applies multiple pattern-matching filters to classify vanity-style addresses.

### ✅ Filters Included

Each matching address is saved into a separate file under the `filtered_results/` directory.

| Filter File         | Description                                                      | Example Match                       |
|---------------------|------------------------------------------------------------------|-------------------------------------|
| `5same.txt`         | Address starts and ends with the same character repeated 5+ times | `0xaaaaaa...aaaaa`                  |
| `mirror.txt`        | Starts and ends with the same exact byte pattern                 | `0xabc123...abc123`                 |
| `reverse.txt`       | Ends with the reversed beginning                                | `0x123abc...cba321`                 |
| `leading_repeat.txt`| Starts with the same character repeated 9+ times                | `0xaaaaaaaaa...`                    |
| `any_repeat.txt`    | Contains 10+ consecutive repeated characters anywhere           | `0x1234bbbbbbbbbb5678`              |
| `numeric_mirror.txt`| Fully numeric and mirrored (start == end)                      | `0x123456...123456`                 |
| `sequence.txt`      | Sequential patterns like `123456789` or `0123456789`           | `0x123456789abcd...`                |
| `startX_endY.txt`   | Starts and ends with 5+ same digits, but different (e.g. `00000...99999`) | `0x00000...99999`        |
| `xyxyxy.txt`        | Repeating two-digit pattern                                     | `0x121212...121212`                 |
| `xxyxxy.txt`        | Custom pattern like `112233112233`                             | `0x112233...112233`                 |
| `3x4.txt`           | At least four blocks of the same digit repeated 3+ times       | `0x444...555...444...555`           |
| `3x5.txt`           | Exactly five such 3-digit repetition blocks                    | Same as above, with exact count     |

### 📁 Input File Format

The input file should be located at:
```
data/addresses.txt
```
Each line must contain:
```
<ethereum_address> <private_key>
```

### ⚙️ Usage

Just run the script:
```bash
python3 filter_script.py
```

Output will be saved in:
```
filtered_results/
```

### 🚀 Performance

- Utilizes Python’s `multiprocessing` with 10 processes for fast filtering.
- Efficient for large address lists (e.g., 1M+ entries).

With the power of the Mac Mini M4 (10 CPU cores and 10 GPUs), the filter script can process and filter 6 million Ethereum addresses in just 12 seconds, making it a highly optimized solution for large-scale address filtering.
