document.addEventListener('DOMContentLoaded', () => {
    const apiUrl = 'http://localhost:8000/todos';
    const todoList = document.getElementById('todo-list');
    const addForm = document.getElementById('add-form');
    const titleInput = document.getElementById('title');
    const descInput = document.getElementById('description');

    // Load todos on start
    loadTodos();

    // Handle new todo submission
    addForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const title = titleInput.value.trim();
        const description = descInput.value.trim();
        if (!title) return;
        const payload = { title, description: description || undefined };
        try {
            const res = await fetch(apiUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
            });
            if (!res.ok) throw new Error('Failed to create todo');
            const newTodo = await res.json();
            addTodoToDOM(newTodo);
            addForm.reset();
        } catch (err) {
            console.error(err);
        }
    });

    async function loadTodos() {
        try {
            const res = await fetch(apiUrl);
            if (!res.ok) throw new Error('Failed to fetch todos');
            const todos = await res.json();
            todoList.innerHTML = '';
            todos.forEach(addTodoToDOM);
        } catch (err) {
            console.error(err);
        }
    }

    function addTodoToDOM(todo) {
        const div = document.createElement('div');
        div.className = 'todo' + (todo.completed ? ' completed' : '');
        div.dataset.id = todo.id;

        const span = document.createElement('span');
        span.textContent = `${todo.title}${todo.description ? ': ' + todo.description : ''}`;
        div.appendChild(span);

        const toggleBtn = document.createElement('button');
        toggleBtn.textContent = todo.completed ? 'Undo' : 'Complete';
        toggleBtn.addEventListener('click', () => toggleComplete(todo.id, !todo.completed));
        div.appendChild(toggleBtn);

        const delBtn = document.createElement('button');
        delBtn.textContent = 'Delete';
        delBtn.addEventListener('click', () => deleteTodo(todo.id));
        div.appendChild(delBtn);

        todoList.appendChild(div);
    }

    async function toggleComplete(id, completed) {
        try {
            const res = await fetch(`${apiUrl}/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ title: document.querySelector(`div[data-id='${id}'] span`).textContent.split(':')[0].trim(), description: null, completed }),
            });
            if (!res.ok) throw new Error('Failed to update todo');
            // Refresh list to reflect changes
            loadTodos();
        } catch (err) {
            console.error(err);
        }
    }

    async function deleteTodo(id) {
        try {
            const res = await fetch(`${apiUrl}/${id}`, { method: 'DELETE' });
            if (!res.ok) throw new Error('Failed to delete todo');
            // Remove element from DOM
            const elem = document.querySelector(`div[data-id='${id}']`);
            if (elem) elem.remove();
        } catch (err) {
            console.error(err);
        }
    }
});