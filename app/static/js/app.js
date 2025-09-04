// Dark mode toggle
const themeToggleBtn = document.getElementById('theme-toggle');

if (localStorage.getItem('color-theme') === 'dark' || (!('color-theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    document.documentElement.classList.add('dark');
} else {
    document.documentElement.classList.remove('dark')
}

themeToggleBtn.addEventListener('click', function() {
    if (localStorage.getItem('color-theme')) {
        if (localStorage.getItem('color-theme') === 'light') {
            document.documentElement.classList.add('dark');
            localStorage.setItem('color-theme', 'dark');
        } else {
            document.documentElement.classList.remove('dark');
            localStorage.setItem('color-theme', 'light');
        }
    } else {
        if (document.documentElement.classList.contains('dark')) {
            document.documentElement.classList.remove('dark');
            localStorage.setItem('color-theme', 'light');
        } else {
            document.documentElement.classList.add('dark');
            localStorage.setItem('color-theme', 'dark');
        }
    }
});

// Lightweight Kanban drag & drop for tasks
(function() {
  const board = document.getElementById('kanban-board');
  if (!board) return;

  const csrf = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
  let dragged = null;

  board.addEventListener('dragstart', (e) => {
    const card = e.target.closest('[data-task-id]');
    if (!card) return;
    dragged = card;
    e.dataTransfer.effectAllowed = 'move';
    card.classList.add('opacity-60');
  });

  board.addEventListener('dragend', (e) => {
    if (dragged) dragged.classList.remove('opacity-60');
    dragged = null;
  });

  board.addEventListener('dragover', (e) => {
    const col = e.target.closest('[data-status]');
    if (!col) return;
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
    col.classList.add('ring-2','ring-blue-500');
  });

  board.addEventListener('drop', async (e) => {
    const col = e.target.closest('[data-status]');
    if (!col || !dragged) return;
    e.preventDefault();
    col.classList.remove('ring-2','ring-blue-500');
    col.querySelector('.space-y-2')?.appendChild(dragged);
    const status = col.getAttribute('data-status');
    const taskId = dragged.getAttribute('data-task-id');
    try {
      const body = new URLSearchParams();
      body.append('status', status);
      body.append('csrf_token', csrf);
      const res = await fetch(`/tasks/${taskId}/status`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: body.toString(),
        credentials: 'same-origin'
      });
      if (!res.ok) {
        console.error('Failed to update status');
      }
    } catch (err) {
      console.error(err);
    }
  });

  board.addEventListener('dragleave', (e) => {
    const col = e.target.closest('[data-status]');
    if (!col) return;
    col.classList.remove('ring-2','ring-blue-500');
  });
})();
