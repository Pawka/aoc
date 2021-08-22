use std::collections::HashMap;
use std::fs;

fn main() {
    let filename = "input.txt";
    part_a(&filename)
}

fn part_a(filename: &str) {
    let contents = fs::read_to_string(filename).expect("Can't read the file");
    let lines = contents.lines().map(|l| {
        let mut hm = HashMap::new();
        for c in l.chars() {
            let value = match hm.get(&c) {
                Some(value) => *value + 1,
                None => 1,
            };
            hm.insert(c, value);
        }
        hm.retain(|_, v| (*v == 3 || *v == 2));
        hm
    });

    let mut two = 0;
    let mut three = 0;

    for hm in lines {
        let mut added2 = false;
        let mut added3 = false;
        for v in hm.values() {
            if added2 && added3 {
                break;
            }

            if !added2 && *v == 2 {
                two += 1;
                added2 = true;
            }

            if !added3 && *v == 3 {
                three += 1;
                added3 = true;
            }
        }
    }

    println!("Day02(A): {}", two * three);
}
