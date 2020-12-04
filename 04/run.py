import re


def read(filename):
    data = []
    with open(filename, 'r') as reader:
        for line in reader.readlines():
            data.append(line.strip())
    return data


def solve(lines):
    valid = 0
    for passport in parse(lines):
        if (len(passport) == 8 or
                len(passport) == 7 and passport.get('cid') is None):
            valid += 1
    return valid


def parse(lines):
    passports = []
    passport = {}
    for line in lines:
        if line == "":
            passports.append(passport)
            passport = {}
            continue
        parts = line.split(" ")
        for p in parts:
            token = p.split(":")
            passport[token[0]] = token[1]
    passports.append(passport)
    return passports


def solve2(lines):
    valid = 0
    for passport in parse(lines):
        if (len(passport) == 8 or
                len(passport) == 7 and passport.get('cid') is None):
            byr = passport.get('byr')
            if (re.match('^[0-9]{4}$', byr) is None or
                    (int(byr) >= 1920 and int(byr) <= 2002) is False):
                continue

            iyr = passport.get('iyr')
            if (re.match('^[0-9]{4}$', iyr) is None or
                    (int(iyr) >= 2010 and int(iyr) <= 2020) is False):
                continue

            eyr = passport.get('eyr')
            if (re.match('^[0-9]{4}$', eyr) is None or
                    (int(eyr) >= 2020 and int(eyr) <= 2030) is False):
                continue

            height = passport.get('hgt')
            if re.match('^[0-9]+(cm|in)$', height) is None:
                continue

            h = int(height[:-2])
            ending = height[-2:]
            if ending == 'cm' and (h < 150 or h > 193):
                continue
            elif ending == 'in' and (h < 59 or h > 76):
                continue

            hair = passport.get('hcl')
            if re.match('^#[0-9a-f]{6}$', hair) is None:
                continue

            eye = passport.get('ecl')
            if eye not in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']:
                continue

            passport_id = passport.get('pid')
            if re.match('^\d{9}$', passport_id) is None:
                continue

            valid += 1
    return valid


if __name__ == "__main__":
    data = read('input.txt')
    print(solve(data))
    print(solve2(data))
