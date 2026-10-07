import { useCallback, useEffect, useState } from "react";
import { createBook, deleteBook, fetchBooks, updateBook } from "./api/books.js";
import BookList from "./components/BookList.jsx";

const EMPTY_FORM = {
  title: "",
  author: "",
  isbn: "",
  price: "",
  category: "",
  stock: "0",
};

const CATEGORIES = ["", "Fantasy", "Sci-Fi", "Classic", "Memoir", "Nonfiction", "Mystery"];

export default function App() {
  const [books, setBooks] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [category, setCategory] = useState("");
  const [q, setQ] = useState("");
  const [form, setForm] = useState(EMPTY_FORM);
  const [editingId, setEditingId] = useState(null);
  const [draft, setDraft] = useState({ price: "", stock: "" });

  const load = useCallback(async (filters = { category, q }) => {
    setLoading(true);
    setError("");
    try {
      setBooks(await fetchBooks(filters));
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [category, q]);

  useEffect(() => {
    load({ category: "", q: "" });
  }, []);

  async function onFilter(e) {
    e.preventDefault();
    await load({ category, q });
  }

  async function onCreate(e) {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      await createBook({
        ...form,
        price: form.price,
        stock: Number(form.stock),
      });
      setForm(EMPTY_FORM);
      await load({ category, q });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function onEdit(book) {
    setEditingId(book.id);
    setDraft({ price: String(book.price), stock: String(book.stock) });
  }

  async function onSave(id) {
    setLoading(true);
    setError("");
    try {
      await updateBook(id, {
        price: draft.price,
        stock: Number(draft.stock),
      });
      setEditingId(null);
      await load({ category, q });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function onDelete(id) {
    setLoading(true);
    setError("");
    try {
      await deleteBook(id);
      if (editingId === id) setEditingId(null);
      await load({ category, q });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page">
      <header>
        <h1>ShelfStack</h1>
        <p className="tagline">Practice assessment — bookstore inventory CRUD &amp; search</p>
      </header>

      <form className="panel" onSubmit={onFilter}>
        <label>
          Category
          <select value={category} onChange={(e) => setCategory(e.target.value)}>
            <option value="">All categories</option>
            {CATEGORIES.filter(Boolean).map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </select>
        </label>
        <label>
          Search (title or author)
          <input
            value={q}
            onChange={(e) => setQ(e.target.value)}
            placeholder="e.g. Tolkien, Dune"
          />
        </label>
        <button type="submit" disabled={loading}>
          Apply
        </button>
      </form>

      <form className="panel grid" onSubmit={onCreate}>
        <h2 className="form-title">Add book</h2>
        {["title", "author", "isbn", "category"].map((key) => (
          <label key={key}>
            {key}
            <input
              value={form[key]}
              onChange={(e) => setForm({ ...form, [key]: e.target.value })}
              required
            />
          </label>
        ))}
        <label>
          price
          <input
            type="number"
            step="0.01"
            min="0"
            value={form.price}
            onChange={(e) => setForm({ ...form, price: e.target.value })}
            required
          />
        </label>
        <label>
          stock
          <input
            type="number"
            min="0"
            value={form.stock}
            onChange={(e) => setForm({ ...form, stock: e.target.value })}
            required
          />
        </label>
        <button type="submit" disabled={loading}>
          Create
        </button>
      </form>

      {error && <p className="error">{error}</p>}
      {loading && <p className="muted">Loading…</p>}

      <BookList
        books={books}
        editingId={editingId}
        draft={draft}
        onEdit={onEdit}
        onDraftChange={setDraft}
        onSave={onSave}
        onCancel={() => setEditingId(null)}
        onDelete={onDelete}
      />
    </div>
  );
}
