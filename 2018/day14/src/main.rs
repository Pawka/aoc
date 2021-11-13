fn main() {
    println!("Day14.a: {}", solve_a(513401));
}

fn solve_a(number: usize) -> String {
    let mut receipes: Vec<usize> = vec![3, 7];

    let mut e1: usize = 0;
    let mut e2: usize = 1;

    for _ in 0..number + 10 {
        receipes.extend(get_new_receipes(receipes[e1] + receipes[e2]));
        e1 = (e1 + receipes[e1] + 1) % receipes.len();
        e2 = (e2 + receipes[e2] + 1) % receipes.len();
    }
    receipes
        .iter()
        .skip(number)
        .take(10)
        .map(|x| x.to_string())
        .collect::<Vec<String>>()
        .join("")
}

fn get_new_receipes(input: usize) -> Vec<usize> {
    match input < 10 {
        true => vec![input],
        false => vec![input / 10, input % 10],
    }
}

#[test]
fn get_new_receipes_test() {
    assert_eq!(vec![9], get_new_receipes(9));
    assert_eq!(vec![1, 9], get_new_receipes(19));
}
