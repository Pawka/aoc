fn main() {
    solve(7347);
}

fn solve(serial: i32) {
    let mut points: Vec<i32> = Vec::new();
    let size = 300;

    for x in 1..=size {
        for y in 1..=size {
            points.push(power(serial, (x, y)));
        }
    }

    let mut max = 0;
    let mut coord = (0, 0);
    for y in 0..size - 3 {
        for x in 0..size - 3 {
            let mut sum = 0;
            for j in 0..3 {
                sum += points[(x + j + y * size) as usize];
                sum += points[(x + j + y * size + size) as usize];
                sum += points[(x + j + y * size + 2 * size) as usize];
            }
            if sum > max {
                max = sum;
                coord = (y + 1, x + 1);
            }
        }
    }
    println!("Power: {}, {:?}", max, coord);
}

fn power(serial: i32, cell: (i32, i32)) -> i32 {
    ((cell.0 + 10) * cell.1 + serial) * (cell.0 + 10) % 1000 / 100 - 5
}

#[test]
fn power_test() {
    assert_eq!(4, power(8, (3, 5)));
    assert_eq!(-5, power(57, (122, 79)));
    assert_eq!(0, power(39, (217, 196)));
    assert_eq!(4, power(71, (101, 153)));
}
