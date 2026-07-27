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
        <div class="start">
            <a href="/signup" class="newBtn">Get Started</a>
        </div>
        <div class="actions">
            <p> Already have an account ?</p>
            <a href="/login" class="btn btn-primary">Login</a>
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
    .start {
        margin-top: 100px;
        padding: 15px;
        background-color: #2b6cb0;
        border-radius: 50px;
    }
    .hero-section {
        margin: 4rem 0;
    }
    .actions {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin-top: 1rem;
        align-items: center;
    }
    .btn {
        padding: 0.75rem 1.5rem;
        text-decoration: none;
        border-radius: 4px;
        font-weight: bold;
    }
    .btn-primary {
        color: #3182ce;

    }
    .newBtn {
        color: #ffffff;
    }
    a {
        transition: color 0.3s ease;
    }

    h1:hover {
        color: #63b3ed;
    }

    h2:hover {
        color: #2b6cb0;
    }

    p:hover {
        color: #4a5568;
    }
    .start,
    .btn-primary {
        transition: all 0.3s ease;
    }
    .start:hover {
        background: #3182ce;
        transform: translateY(-4px);
        box-shadow: 0 12px 25px rgba(49, 130, 206, 0.35);
    }
    .btn-primary:hover {
        background: #3182ce;
        color: #ffffff;
        transform: scale(1.05);
    }
</style>
