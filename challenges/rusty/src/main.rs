/*
 * rustc -O rusty.rs -o rusty -F unsafe_code
 */
use std::io;

struct Book {
    name: String,
    pages: Vec<u64>,
}

fn check_pages(book: Book) -> bool {
    book.pages.len() < 200
}

fn add_book(books: &mut Vec<Book>) {
    let mut name = String::new();
    println!("Enter name: ");
    io::stdin().read_line(&mut name).unwrap();
    name.pop();

    let mut pages:Vec<u64> = Vec::with_capacity(12);


    loop {
        let mut page = String::new();
        println!("Enter damaged page: ");
        io::stdin().read_line(&mut page).unwrap();
        page.pop();

        pages.push(page.parse().expect("Error"));

        let mut choice = String::new();
        println!("More? (y/n): ");
        io::stdin().read_line(&mut choice).unwrap();
        choice.pop();

        match &choice as &str {
            "y" | "Y" => (),
            _ => break,
        }
    }

    if pages.len() > 1 {
        let book = Book { name, pages };
        match book {
            _ if !check_pages(book) => println!("Too many pages"),
            _ => books.push(book),
        }
    } else {
        books.push(Book { name, pages });
    }
}

fn edit_book(books: &mut Vec<Book>) {
    let mut choice = String::new();
    println!("Which book: ");
    io::stdin().read_line(&mut choice).expect("Error");
    choice.pop();
    let index: usize = choice.parse().expect("Error");

    books[index].name.truncate(0);


    let mut name = String::new();
    println!("Enter name: ");
    io::stdin().read_line(&mut name).expect("Error");
    name.pop();
    books[index].name.push_str(&name);

    loop {
        let mut choice = String::new();
        println!("Which page: ");
        io::stdin().read_line(&mut choice).expect("Error");
        choice.pop();

        let page_index: usize = choice.parse().expect("Error");

        let mut page = String::new();
        println!("Enter damaged page: ");
        io::stdin().read_line(&mut page).unwrap();
        page.pop();

        books[index].pages[page_index] = page.parse().expect("Error");

        println!("More? (y/n): ");
        io::stdin().read_line(&mut choice).unwrap();
        choice.pop();

        match &choice as &str {
            "y" | "Y" => (),
            _ => break,
        }
    }
}

fn show_book(books: &Vec<Book>) {
    let mut choice = String::new();
    println!("Which book: ");
    io::stdin().read_line(&mut choice).expect("Error");
    choice.pop();
    let index: usize = choice.parse().expect("Error");

    println!("{} - Title: {}, Pages: {:?}", index, books[index].name, books[index].pages);
}

fn list_books(books: &Vec<Book>) {
    for (i, book) in books.iter().enumerate() {
        println!("{} - Title: {}, Pages: {:?}", i, book.name, book.pages);
    }
}

fn print_menu() {
    println!("1. Add book");
    println!("2. Edit book");
    println!("3. List books");
    println!("4. Show book");
    println!("5. Exit");
    println!("--------------");
}

fn main() {
    let mut books:Vec<Book> = Vec::with_capacity(8);
    println!("Welcome to the Damaged Book Database");

    loop {
        print_menu();
        let mut choice = String::new();
        io::stdin().read_line(&mut choice).expect("Error");
        choice.pop();
        match &choice as &str {
            "1" => add_book(&mut books),
            "2" => edit_book(&mut books),
            "3" => list_books(&books),
            "4" => show_book(&books),
            "5" => break,
            _ => println!("Unknown option"),
       }
    }
}
