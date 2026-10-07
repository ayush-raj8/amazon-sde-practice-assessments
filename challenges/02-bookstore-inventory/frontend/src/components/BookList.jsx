export default function BookList({ books, editingId, draft, onEdit, onDraftChange, onSave, onCancel, onDelete }) {
  if (!books.length) {
    return <p className="empty">No books match your filters.</p>;
  }

  return (
    <ul className="book-list">
      {books.map((b) => {
        const isEditing = editingId === b.id;
        return (
          <li key={b.id} className="book-card">
            <div className="book-header">
              <h3>{b.title}</h3>
              <span className="category">{b.category}</span>
            </div>
            <p>
              <strong>Author:</strong> {b.author}
            </p>
            <p>
              <strong>ISBN:</strong> {b.isbn}
            </p>

            {isEditing ? (
              <div className="edit-row">
                <label>
                  Price
                  <input
                    type="number"
                    step="0.01"
                    min="0"
                    value={draft.price}
                    onChange={(e) => onDraftChange({ ...draft, price: e.target.value })}
                  />
                </label>
                <label>
                  Stock
                  <input
                    type="number"
                    min="0"
                    value={draft.stock}
                    onChange={(e) => onDraftChange({ ...draft, stock: e.target.value })}
                  />
                </label>
                <div className="edit-actions">
                  <button type="button" onClick={() => onSave(b.id)}>
                    Save
                  </button>
                  <button type="button" className="ghost" onClick={onCancel}>
                    Cancel
                  </button>
                </div>
              </div>
            ) : (
              <>
                <p>
                  <strong>Price:</strong> ${Number(b.price).toFixed(2)}
                </p>
                <p>
                  <strong>Stock:</strong> {b.stock}
                </p>
                <div className="card-actions">
                  <button type="button" onClick={() => onEdit(b)}>
                    Edit price / stock
                  </button>
                  <button type="button" className="danger" onClick={() => onDelete(b.id)}>
                    Delete
                  </button>
                </div>
              </>
            )}
          </li>
        );
      })}
    </ul>
  );
}
