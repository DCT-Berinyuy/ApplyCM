<script lang="ts">
    let { children } = $props();
    // TODO: Implement authentication guard/redirects using auth store
</script>

<div class="app-layout">
    <nav class="sidebar">
        <div class="logo">ApplyCM</div>
        <ul>
            <li><a href="/dashboard">Dashboard</a></li>
            <li><a href="/discover">Discover Schools</a></li>
            <li><a href="/application/profile">Application Profile</a></li>
            <li><a href="/favorites">Favorites</a></li>
            <li><a href="/settings">Settings</a></li>
        </ul>
    </nav>
    <main class="content">
        {@render children()}
    </main>
</div>

<style>
    /* TODO: Style layout and navigation sidebar */
    .app-layout {
        display: flex;
        min-height: 100vh;
    }
    .sidebar {
        width: 250px;
        background-color: #1a202c;
        color: white;
        padding: 2rem 1rem;
    }
    .sidebar .logo {
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 2rem;
    }
    .sidebar ul {
        list-style: none;
        padding: 0;
    }
    .sidebar ul li {
        margin-bottom: 1rem;
    }
    .sidebar ul li a {
        color: #a0aec0;
        text-decoration: none;
        display: block;
        padding: 0.5rem;
        border-radius: 4px;
    }
    .sidebar ul li a:hover {
        background-color: #2d3748;
        color: white;
    }
    .content {
        flex: 1;
        padding: 2rem;
        background-color: #f7fafc;
    }
</style>
