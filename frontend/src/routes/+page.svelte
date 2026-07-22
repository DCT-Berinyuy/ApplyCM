<script lang="ts">
    // TODO: Implement landing page state and interactive animations if needed
</script>

<div class="landing-container">
    <header>
        <h1>ApplyCM</h1>
        <p>Apply to multiple Cameroonian schools with one shared profile.</p>
    </header>

    <main class="hero-section">
        <h2>Simplify Your University Applications</h2>
        <p>Discover programs, save your favorites, build your profile once, and apply to multiple universities in Cameroon.</p>
        <div class="actions">
            <a href="/login" class="btn btn-primary">Login</a>
            <a href="/signup" class="btn btn-secondary">Get Started</a>
        </div>
    </main>

    <footer>
        <p>&copy; {new Date().getFullYear()} ApplyCM. All rights reserved.</p>
    </footer>
</div>

<style>
    /* TODO: Implement beautiful themed landing page styling */
    .landing-container {
        font-family: sans-serif;
        text-align: center;
        max-width: 800px;
        margin: 0 auto;
        padding: 2rem;
    }
    header h1 {
        font-size: 3rem;
        color: #2b6cb0;
    }
    .hero-section {
        margin: 4rem 0;
    }
    .actions {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin-top: 2rem;
    }
    .btn {
        padding: 0.75rem 1.5rem;
        text-decoration: none;
        border-radius: 4px;
        font-weight: bold;
    }
    .btn-primary {
        background-color: #3182ce;
        color: white;
    }
    .btn-secondary {
        background-color: #edf2f7;
        color: #2d3748;
    }
</style>
