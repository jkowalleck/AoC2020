from os import path
from re import compile as re_compile
from typing import Callable, Dict, List

INPUT_FILE = path.join(path.dirname(__file__), 'input')


def get_input() -> List[str]:
    with open(INPUT_FILE) as fh:
        return [line.rstrip('\n') for line in fh.readlines()]


class Document(Dict[str, str]):
    def set_from_line(self, line) -> None:
        for key_value in line.strip().split(' '):
            key, value = key_value.split(':')
            self[key] = value


class DocumentCollection(List[Document]):
    @classmethod
    def from_raw_lines(cls, lines: List[str]) -> "DocumentCollection":
        docs = cls()
        doc = Document()
        line_index_max = len(lines) - 1
        for line_index, line in enumerate(lines):
            if line == '':
                docs.append(doc)
                doc = Document()
                continue  # for ... in ...
            doc.set_from_line(line)
            if line_index == line_index_max and doc:
                docs.append(doc)
                break
        return docs


_Validation = Callable[[Document], bool]


def solve(validate: _Validation) -> int:
    docs = DocumentCollection.from_raw_lines(get_input())
    valid = 0
    for doc in docs:
        if validate(doc):
            valid += 1
    return valid


PASSPORT_KEYS_REQUIRED = (
    'byr',  # (Birth Year)
    'iyr',  # (Issue Year)
    'eyr',  # (Expiration Year)
    'hgt',  # (Height)
    'hcl',  # (Hair Color)
    'ecl',  # (Eye Color)
    'pid',  # (Passport ID)
    # 'cid',  # (Country ID)
)


def validation1(doc: Document) -> bool:
    return all(key in doc for key in PASSPORT_KEYS_REQUIRED)


_HGT_RE = re_compile(r'^(\d+)(cm|in)$')
_HCL_RE = re_compile(r'^#[0-9a-f]{6}$')
_PID_RE = re_compile(r'^\d{9}$')


def validation2(doc: Document) -> bool:
    if any(key not in doc for key in PASSPORT_KEYS_REQUIRED):
        return False
    if not 1920 <= int(doc['byr']) <= 2002:
        return False
    if not 2010 <= int(doc['iyr']) <= 2020:
        return False
    if not 2020 <= int(doc['eyr']) <= 2030:
        return False
    hgt_match = _HGT_RE.match(doc['hgt'])
    if not hgt_match:
        return False
    hgt_value, hgt_unit = hgt_match.groups()
    if hgt_unit == 'cm' and not 150 <= int(hgt_value) <= 193:
        return False
    if hgt_unit == 'in' and not 59 <= int(hgt_value) <= 76:
        return False
    if not _HCL_RE.match(doc['hcl']):
        return False
    if doc['ecl'] not in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}:
        return False
    if not _PID_RE.match(doc['pid']):
        return False
    return True


if __name__ == '__main__':
    solution_part1 = solve(validation1)
    print(f'solution part 1: {solution_part1}')
    solution_part2 = solve(validation2)
    print(f'solution part 2: {solution_part2}')
