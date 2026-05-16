const API = 'http://127.0.0.1:5000/api';

function setTab(type, el) {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    el.classList.add('active');
    document.getElementById('logins-view').style.display = type === 'logins' ? 'block' : 'none';
    document.getElementById('requests-view').style.display = type === 'requests' ? 'block' : 'none';
    fetchData(type);
}

function copyText(text, btn) {
    navigator.clipboard.writeText(text).then(() => {
        btn.classList.add('copied');
        btn.textContent = '✅ Copied';
        setTimeout(() => { btn.classList.remove('copied'); btn.textContent = '📋 Copy'; }, 1500);
    });
}

function renderCards(data, isLogin) {
    if(!data.length) return '<p class="empty">No data found.</p>';
    return data.map(d => isLogin ? `
        <div class="data-card">
            <div class="row"><span>User: <b>${d.username}</b> (${d.role})</span></div>
            <div class="row"><span>Pass: ${d.password}</span> <button class="copy-btn" onclick="copyText('${d.password}', this)">📋 Copy</button></div>
        </div>` : `
        <div class="data-card">
            <div class="row"><span>User: <b>${d.username}</b></span></div>
            <div class="row"><span>Name: ${d.name}</span> <button class="copy-btn" onclick="copyText('${d.name}', this)">📋</button></div>
            <div class="row"><span>Mobile: ${d.mobile}</span> <button class="copy-btn" onclick="copyText('${d.mobile}', this)">📋</button></div>
            <div class="row"><span>Email: ${d.email}</span> <button class="copy-btn" onclick="copyText('${d.email}', this)">📋</button></div>
            <div class="row"><span>Pass: ${d.service_password}</span> <button class="copy-btn" onclick="copyText('${d.service_password}', this)">📋</button></div>
        </div>`).join('');
}

async function fetchData(type) {
    const res = await fetch(`${API}/admin/${type === 'logins' ? 'login-data' : 'requests'}`);
    const data = await res.json();
    document.getElementById(type === 'logins' ? 'logins-view' : 'requests-view').innerHTML = renderCards(data, type === 'logins');
}

async function handleAdminLogin() {
    const res = await fetch(`${API}/login`, {
        method:'POST', headers:{'Content-Type':'application/json'},
        body: JSON.stringify({username: document.getElementById('a-user').value, password: document.getElementById('a-pass').value})
    });
    const data = await res.json();
    if(data.success && data.role === 'admin') {
        document.getElementById('admin-login').classList.remove('active');
        document.getElementById('admin-dash').classList.add('active');
        fetchData('logins');
    } else alert('Invalid Admin Credentials');
}