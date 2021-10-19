use std::fs;

fn main() {
    let filename = "input.txt";
    let input = fs::read_to_string(filename).expect("can't read file");
    let numbers: Vec<i32> = input
        .split_whitespace()
        .map(|x| x.parse().unwrap())
        .collect();
    solve_a(&numbers);
    solve_b(&numbers);
}

fn solve_a(numbers: &Vec<i32>) {
    let mut childs = Vec::new();
    let mut meta = Vec::new();
    let mut sum: i32 = 0;
    let mut iter = numbers.iter();
    while let Some(n) = iter.next() {
        childs.push(*n);
        meta.push(iter.next().unwrap());

        while let Some(0) = childs.last() {
            let m = meta.pop().unwrap();
            sum += iter.by_ref().take(*m as usize).sum::<i32>();
            childs.pop();
        }

        if let Some(n) = childs.last_mut() {
            *n -= 1;
        }
    }

    println!("Day08(a): {}", sum);
}

fn solve_b(numbers: &Vec<i32>) {
    let mut childs = Vec::new();
    let mut meta = Vec::new();
    let mut sum: i32 = 0;
    let mut iter = numbers.iter();
    let mut values: Vec<Vec<i32>> = Vec::new();

    let mut depth = 0;
    while let Some(n) = iter.next() {
        let mcount = iter.next().unwrap();
        if *n > 0 {
            values.push(Vec::new());
            childs.push(*n);
            meta.push(mcount);
            depth += 1;
        } else if *n == 0 {
            let sum = iter.by_ref().take(*mcount as usize).sum::<i32>();
            values.get_mut(depth - 1).unwrap().push(sum);
            if let Some(n) = childs.last_mut() {
                *n -= 1;
            }
        }

        while let Some(0) = childs.last() {
            let m = meta.pop().unwrap();
            let mut s = 0;
            for i in iter.by_ref().take(*m as usize) {
                if *i <= values[(depth - 1) as usize].len() as i32 {
                    s += values[(depth - 1) as usize][(*i - 1) as usize];
                }
            }
            depth -= 1;
            if depth > 0 {
                values.get_mut(depth - 1).unwrap().push(s);
            } else {
                sum = s;
            }
            childs.pop();

            if let Some(n) = childs.last_mut() {
                *n -= 1;
            }
        }
    }
    println!("{:?}", childs);
    println!("{:?}", meta);
    println!("{:?}", values);

    println!("Day08(b): {}", sum);
}
