#[macro_use]
extern crate lazy_static;
use regex::Regex;
use std::collections::HashMap;
use std::fs;

fn main() {
    let filename = "input.txt";
    let contents = fs::read_to_string(filename).expect("can't read file");
    solve(&contents);
}

fn solve(contents: &String) {
    let mut lines: Vec<Line> = contents.lines().map(|line| parse(&line)).collect();
    lines.sort_by(|a, b| a.date.cmp(&b.date));

    let mut hm = HashMap::new();
    let mut guard = 0;
    let mut start = 0;
    for line in &lines {
        match line.content() {
            Some(Content::Guard(id)) => {
                guard = id;
                if hm.contains_key(&guard) == false {
                    hm.insert(id, vec![0; 60]);
                }
            }
            Some(Content::Asleep) => start = line.minute,
            Some(Content::WakeUp) => {
                for i in start..line.minute {
                    hm.get_mut(&guard).unwrap()[i] += 1;
                }
            }
            _ => (),
        };
    }

    let mut max_id: usize = 0;
    let mut max_mins = 0;
    for (id, v) in hm.iter() {
        let mins = v.iter().fold(0, |acc, x| acc + x);
        if mins > max_mins {
            max_mins = mins;
            max_id = *id;
        }
    }

    println!(
        "Day04(a): {}",
        max_id * get_index_of_max(&hm.get(&max_id).unwrap())
    );
    println!(
        "Day04(b): {}",
        hm.iter()
            .max_by(|a, b| {
                let ma = a.1.iter().max().unwrap();
                let mb = b.1.iter().max().unwrap();
                ma.cmp(mb)
            })
            .map(|(id, v)| id * get_index_of_max(v))
            .unwrap()
    );
}

fn get_index_of_max(v: &Vec<usize>) -> usize {
    v.iter()
        .enumerate()
        .max_by(|(_, a), (_, b)| a.cmp(b))
        .map(|(minute, _)| minute)
        .unwrap()
}

#[derive(Debug, PartialEq, Eq)]
enum Content {
    WakeUp,
    Asleep,
    Guard(usize),
}

#[derive(Debug)]
struct Line {
    date: String,
    action: String,
    minute: usize,
}

const GUARD_ID_REGEX: &str = r"#(\d+)";

impl Line {
    fn content(&self) -> Option<Content> {
        lazy_static! {
            static ref RE: Regex = Regex::new(GUARD_ID_REGEX).unwrap();
        }
        match self.action.as_str() {
            "wakes up" => Some(Content::WakeUp),
            "falls asleep" => Some(Content::Asleep),
            _ => {
                let l = RE.captures(&self.action);
                match l {
                    None => None,
                    Some(captures) => Some(Content::Guard(captures[1].parse().unwrap())),
                }
            }
        }
    }
}

fn parse(line: &str) -> Line {
    let re = Regex::new(r"\[([^\]]+:(\d\d))\] (.+)").unwrap();
    let l = re.captures(line).unwrap();
    Line {
        date: l[1].parse().unwrap(),
        minute: l[2].parse().unwrap(),
        action: l[3].parse().unwrap(),
    }
}

#[test]
fn parse_test() {
    let r1 = parse("[1518-09-29 00:35] falls asleep");
    assert_eq!("1518-09-29 00:35", r1.date);
    assert_eq!("falls asleep", r1.action);
    assert_eq!(35, r1.minute);

    assert_eq!(Some(Content::Asleep), r1.content());

    let r2 = parse("[1518-07-20 00:53] wakes up");
    assert_eq!(Some(Content::WakeUp), r2.content());

    let r3 = parse("[1518-10-25 23:50] Guard #181 begins shift");
    assert_eq!(Some(Content::Guard(181)), r3.content())
}
