use std::fs;

fn main() {
    let filename = "input.txt";
    let input = fs::read_to_string(filename).expect("can't read file");
    let numbers: Vec<i32> = input
        .split_whitespace()
        .map(|x| x.parse().unwrap())
        .collect();
    solve_a(&numbers);
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
