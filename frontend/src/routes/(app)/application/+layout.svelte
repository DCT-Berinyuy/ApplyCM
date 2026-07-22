<script lang="ts">
    let { children } = $props();
    // TODO: Manage step validation and navigation state
</script>

<div class="application-layout">
    <aside class="sub-nav">
        <h3>Shared Profile</h3>
        <ul>
            <li><a href="/application/profile">1. Personal Details</a></li>
            <li><a href="/application/education">2. Education</a></li>
            <li><a href="/application/writing">3. Writing & Statement</a></li>
        </ul>
    </aside>
    <section class="step-content">
        {@render children()}
    </section>
</div>

<style>
    /* TODO: Style application section layout and step progress */
    .application-layout {
        display: flex;
        gap: 2rem;
        background-color: white;
        padding: 2rem;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    .sub-nav {
        width: 200px;
        border-right: 1px solid #e2e8f0;
        padding-right: 1.5rem;
    }
    .sub-nav h3 {
        font-size: 1.1rem;
        color: #4a5568;
        margin-bottom: 1.5rem;
    }
    .sub-nav ul {
        list-style: none;
        padding: 0;
    }
    .sub-nav ul li {
        margin-bottom: 1rem;
    }
    .sub-nav ul li a {
        text-decoration: none;
        color: #4a5568;
        display: block;
        padding: 0.5rem;
        border-radius: 4px;
    }
    .sub-nav ul li a:hover {
        background-color: #f7fafc;
        color: #2b6cb0;
    }
    .step-content {
        flex: 1;
    }
</style>
