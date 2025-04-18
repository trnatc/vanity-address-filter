import re
from multiprocessing import Pool
from pathlib import Path

OUTPUT_DIR = Path("filtered_results")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def check_5same(address):
    match = re.match(r'^0x([0-9a-f])\1{4,}', address)
    if match:
        ch = match.group(1)
        suffix = ch * 5
        if address.endswith(suffix):
            return True
    return False

def check_mirror(address):
    for i in range(8, len(address) // 2 + 1):
        part = address[2:2+i]
        if address.startswith('0x' + part) and address.endswith(part):
            return True
    return False

def check_reverse(address):
    for i in range(8, len(address) // 2 + 1):
        part = address[2:2+i]
        reversed_part = part[::-1]
        if address.endswith(reversed_part):
            return True
    return False

def check_leading_repeat(address):
    return bool(re.match(r'^0x([0-9a-f])\1{8,}', address))

def check_any_repeat(address):
    return bool(re.search(r'([0-9a-f])\1{9,}', address[2:]))

def check_numeric_mirror(address):
    if not re.fullmatch(r'^0x[0-9]+$', address):
        return False
    digits = address[2:]
    for i in range(2, len(digits) // 2 + 1):
        if digits[:i] == digits[-i:]:
            return True
    return False

def check_sequence(address):
    body = address[2:]
    return (body.startswith("123456789") or body.startswith("0123456789") or
            body.endswith("123456789"))

def check_startX_endY(address):
    body = address[2:]
    if not re.fullmatch(r'[0-9]+', body):
        return False
    if len(body) < 10:
        return False
    start = body[:5]
    end = body[-5:]
    return (len(set(start)) == 1 and len(set(end)) == 1 and start != end)

def check_xyxyxy(address):
    body = address[2:]
    return bool(re.match(r'^([0-9]{2})\1{2}', body) and body.endswith(body[:6]))

def check_xxyxxy(address):
    body = address[2:]
    return bool(re.match(r'^([0-9])\1([0-9])\1\2\1\2', body) and body.endswith(body[:6]))

def check_3x4(address):
    body = address[2:]
    blocks = re.findall(r'([0-9])\1{2,}', body)
    if not blocks:
        return False
    counts = {}
    for digit in blocks:
        counts[digit] = counts.get(digit, 0) + 1
    return any(count >= 4 for count in counts.values())

def check_3x5(address):
    body = address[2:]
    blocks = re.findall(r'([0-9])\1{2,}', body)
    if not blocks:
        return False
    counts = {}
    for digit in blocks:
        counts[digit] = counts.get(digit, 0) + 1
    return any(count == 5 for count in counts.values())

def process_line(line):
    try:
        line = line.strip()
        if not line:
            return
        address, _ = line.split()
        results = []

        if check_5same(address):
            results.append(('5same.txt', line))
        elif check_mirror(address):
            results.append(('mirror.txt', line))
        elif check_reverse(address):
            results.append(('reverse.txt', line))
        elif check_leading_repeat(address):
            results.append(('leading_repeat.txt', line))
        elif check_any_repeat(address):
            results.append(('any_repeat.txt', line))
        elif check_numeric_mirror(address):
            results.append(('numeric_mirror.txt', line))
        elif check_sequence(address):
            results.append(('sequence.txt', line))
        elif check_startX_endY(address):
            results.append(('startX_endY.txt', line))
        elif check_xyxyxy(address):
            results.append(('xyxyxy.txt', line))
        elif check_xxyxxy(address):
            results.append(('xxyxxy.txt', line))
        elif check_3x4(address):
            results.append(('3x4.txt', line))
        elif check_3x5(address):
            results.append(('3x5.txt', line))

        for file_name, content in results:
            file_path = OUTPUT_DIR / file_name
            with open(file_path, 'a') as f:
                f.write(content + '\n')

    except Exception:
        pass

def process_file(input_file):
    output_files = [
        '5same.txt', 'mirror.txt', 'reverse.txt', 'leading_repeat.txt',
        'any_repeat.txt', 'numeric_mirror.txt', 'sequence.txt',
        'startX_endY.txt', 'xyxyxy.txt', 'xxyxxy.txt', '3x4.txt', '3x5.txt'
    ]
    for file in output_files:
        file_path = OUTPUT_DIR / file
        if not file_path.exists():
            file_path.write_text("")

    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    with Pool(processes=10) as pool:
        pool.map(process_line, lines)

if __name__ == '__main__':
    input_file = "data/addresses.txt"
    process_file(input_file)
