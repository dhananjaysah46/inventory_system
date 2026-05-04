// js/layout.js - सबै pages मा same sidebar
function renderLayout(activePage) {
    document.body.innerHTML = `
        <div class="app-container">
            <div class="sidebar">
                <div class="sidebar-logo">
                    <span>📦</span>
                    <span>Inventory</span>
                </div>
                <nav>
                    <a href="index.html" class="nav-item ${activePage === 'dashboard' ? 'active' : ''}">
                        <span>📊</span> Dashboard
                    </a>
                    <a href="products.html" class="nav-item ${activePage === 'products' ? 'active' : ''}">
                        <span>🏷️</span> Products
                    </a>
                    <a href="purchases.html" class="nav-item ${activePage === 'purchases' ? 'active' : ''}">
                        <span>🛒</span> Purchases
                    </a>
                    <a href="sales.html" class="nav-item ${activePage === 'sales' ? 'active' : ''}">
                        <span>💰</span> Sales
                    </a>
                </nav>
                <button class="logout-btn" onclick="logout()">
                    🚪 Logout
                </button>
            </div>
            <div class="main-content" id="main-content"></div>
        </div>
    ` + document.body.innerHTML;
}