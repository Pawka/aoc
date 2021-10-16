use regex::Regex;
use std::collections::{HashMap, HashSet};
use std::fs;

type SetMap = HashMap<char, HashSet<char>>;

fn main() {
    let filename = "input.txt";
    let input = fs::read_to_string(filename).expect("can't read file");

    let re = Regex::new(r"^Step (.) must be finished before step (.) can begin.$").unwrap();

    let mut childs: SetMap = HashMap::new();
    let mut dependencies: SetMap = HashMap::new();

    for line in input.lines() {
        let c = re.captures(line).unwrap();
        let from = c[1].parse().unwrap();
        let to = c[2].parse().unwrap();

        dependencies.entry(from).or_insert(HashSet::new());
        dependencies
            .entry(to)
            .or_insert(HashSet::new())
            .insert(from);
        childs.entry(to).or_insert(HashSet::new());
        childs.entry(from).or_insert(HashSet::new()).insert(to);
    }
    solve_a(dependencies.clone(), &childs);
    solve_b(dependencies.clone(), &childs);
}

fn solve_a(mut dependencies: SetMap, childs: &SetMap) {
    let mut queue = get_independent(&dependencies);
    let mut result = String::new();
    loop {
        queue.sort();
        if queue.len() == 0 {
            break;
        }
        let current = queue[0];
        queue.remove(0);

        for child in childs.get(&current).unwrap() {
            let deps = dependencies.get_mut(&child).unwrap();
            deps.remove(&current);

            if deps.len() == 0 {
                queue.push(*child);
            }
        }

        result.push(current);
    }
    println!("Day07(a): {}", result);
}

fn get_independent(dependencies: &SetMap) -> Vec<char> {
    let mut queue: Vec<char> = Vec::new();
    for (ch, d) in dependencies {
        if d.len() == 0 {
            queue.push(*ch);
        }
    }
    queue
}

const WORKERS: usize = 5;
const STEP_DURATION: u8 = 60;

fn solve_b(mut dependencies: SetMap, childs: &SetMap) {
    let mut workers: Vec<Option<Task>> = Vec::new();
    for _ in 0..WORKERS {
        workers.push(None);
    }
    let mut queue = get_independent(&dependencies);
    let mut in_progress: HashSet<char> = HashSet::new();
    let mut ticks = 0;
    loop {
        if queue.is_empty() && in_progress.is_empty() {
            break;
        }
        ticks += 1;
        for i in 0..workers.len() {
            if workers[i].is_none() && !queue.is_empty() {
                workers[i] = Some(Task::new(queue[0]));
                in_progress.insert(queue[0]);
                queue.remove(0);
            }
        }

        for i in 0..workers.len() {
            if let Some(ref mut task) = workers[i] {
                task.work();
                if task.work == 0 {
                    in_progress.remove(&task.val);
                    for child in childs.get(&task.val).unwrap() {
                        let deps = dependencies.get_mut(&child).unwrap();
                        deps.remove(&task.val);
                    }
                    if dependencies.get(&task.val).unwrap().is_empty() {
                        dependencies.remove(&task.val);
                    }
                    workers[i] = None;
                    if !queue.is_empty() {
                        workers[i] = Some(Task::new(queue[0]));
                        in_progress.insert(queue[0]);
                        queue.remove(0);
                    }
                }
            }
        }
        queue = get_independent(&dependencies)
            .iter()
            .filter(|x| !in_progress.contains(x))
            .map(|x| *x)
            .collect();
        queue.sort();
    }

    println!("Day07(b): {}", ticks);
}

#[derive(Debug)]
struct Task {
    val: char,
    work: u8,
}

impl Task {
    fn new(ch: char) -> Task {
        Task {
            val: ch,
            work: (ch as u8 - 64 + STEP_DURATION),
        }
    }

    fn work(&mut self) -> Option<()> {
        if self.work == 0 {
            return None;
        }
        self.work -= 1;
        Some(())
    }
}

#[test]
fn task_work_test() {
    let mut t = Task::new('A');
    assert_eq!(61, t.work);
    t.work();
    assert_eq!(60, t.work);
}
