import streamlit as st
import json
import os

BOOK_FILE = "library_data.json"

# Load books from file
def load_books():
    if os.path.exists(BOOK_FILE):
        with open(BOOK_FILE, "r") as file:
            return json.load(file)
    return []

# Save books to file
def save_books(books):
    with open(BOOK_FILE, "w") as file:
        json.dump(books, file, indent=4)

# Add book to list
def add_book(title, author, year, genre, read):
    books = load_books()
    books.append({
        "title": title,
        "author": author,
        "year": year,
        "genre": genre,
        "read": read
    })
    save_books(books)

# Remove a book
def remove_book(title):
    books = load_books()
    books = [book for book in books if book["title"].lower() != title.lower()]
    save_books(books)

# Toggle read status
def toggle_read(title):
    books = load_books()
    for book in books:
        if book["title"].lower() == title.lower():
            book["read"] = not book["read"]
            break
    save_books(books)

# Search books
def search_books(keyword):
    keyword = keyword.lower()
    return [book for book in load_books() if keyword in book["title"].lower() or keyword in book["author"].lower()]

# Streamlit UI
st.set_page_config(page_title="📚 Personal Library Manager", layout="wide")
st.title("📚 Personal Library Manager")
st.subheader("👩‍💻 Created by Sana Akhlaq")

# Tabs for navigation
tabs = st.tabs(["➕ Add Book", "📖 View Library", "🔍 Search", "📊 Stats"])

# ➕ Add Book Tab
with tabs[0]:
    st.header("Add a New Book")
    title = st.text_input("Title")
    author = st.text_input("Author")
    year = st.number_input("Year", min_value=1000, max_value=2100, value=2024)
    genre = st.text_input("Genre")
    read = st.checkbox("Mark as Read")

    if st.button("Add Book"):
        if title and author:
            add_book(title, author, year, genre, read)
            st.success(f"Book '{title}' added!")
        else:
            st.warning("Please enter both title and author.")

# 📖 View All Books Tab
with tabs[1]:
    st.header("Your Library")
    books = load_books()
    if books:
        for idx, book in enumerate(books):
            col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
            with col1:
                st.markdown(f"**{book['title']}** by {book['author']} ({book['year']})")
                st.caption(f"Genre: {book['genre']}")
            with col2:
                status = "✅ Read" if book["read"] else "📖 Unread"
                st.markdown(f"**Status:** {status}")
            with col3:
                if st.button("Toggle Read", key=f"toggle_{idx}"):
                    toggle_read(book["title"])
                    st.rerun()
            with col4:
                if st.button("❌ Remove", key=f"remove_{idx}"):
                    remove_book(book["title"])
                    st.rerun()
    else:
        st.info("No books added yet.")

# 🔍 Search Tab
with tabs[2]:
    st.header("Search Books")
    query = st.text_input("Enter title or author to search")
    if query:
        results = search_books(query)
        if results:
            for book in results:
                st.write(f"📖 {book['title']} by {book['author']} ({book['year']}) - {'✅ Read' if book['read'] else '📖 Unread'}")
        else:
            st.warning("No matching books found.")

# 📊 Stats Tab
with tabs[3]:
    st.header("Library Stats")
    books = load_books()
    total = len(books)
    read_count = sum(1 for book in books if book["read"])
    unread_count = total - read_count

    st.metric("Total Books", total)
    st.metric("Books Read", read_count)
    st.metric("Unread Books", unread_count)

    if total > 0:
        st.progress(read_count / total)
