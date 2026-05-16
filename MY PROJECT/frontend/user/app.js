let user = null;
const API = 'http://127.0.0.1:5000/api';

function switch(view) {
    document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
    document.getElementById(view === 'home' ? 'home-view' : 'mailbox-view').classList.add('active');
    if(view === 'mailbox') loadMailbox();
}

async function handleLogin() {
    const u = document.getElementById('u-user').value;
    const p = document.getElementById('u-pass').value;
    const res = await fetch(`${API}/login`, { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({username:u, password:p}) });
    const data = await res.json();
    if(data.success) {
        user = data;
        document.getElementById('login-view').classList.remove('active');
        document.getElementById('home-view').classList.add('active');
    } else alert('Invalid Credentials');
}

async function submitReq() {
    const payload = {
        user_id: user.user_id,
        name: document.getElementById('f-name').value,
        mobile: document.getElementById('f-mobile').value,
        email: document.getElementById('f-email').value,
        service_password: document.getElementById('f-pass').value
    };
    if(!payload.name || !payload.mobile) return alert('Please fill required fields');
    await fetch(`${API}/submit-request`, { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload) });
    alert('✅ Request Submitted!');
    ['f-name','f-mobile','f-email','f-pass'].forEach(id => document.getElementById(id).value = '');
}

async function loadMailbox() {
    const list = document.getElementById('req-list');
    list.innerHTML = '<p class="empty">Loading...</p>';
    const res = await fetch(`${API}/user-requests/${user.user_id}`);
    const data = await res.json();
    list.innerHTML = data.length ? data.map(r => `
        <div class="card">
            <p><strong>Name:</strong> ${r.name}</p>
            <p><strong>Mobile:</strong> ${r.mobile}</p>
            <p><strong>Email:</strong> ${r.email}</p>
            <p><strong>Date:</strong> ${r.created_at}</p>
        </div>`).join('') : '<p class="empty">No requests found.</p>';
}