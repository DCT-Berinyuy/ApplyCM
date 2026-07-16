<script lang="ts">
    // TODO: Implement login form submission and state management using auth store
</script>

<div class="auth-card">
    <h2>Login to ApplyCM</h2>
    <form onsubmit={(e) => e.preventDefault()}>
        <div class="form-group">
            <label for="email">Email Address</label>
            <input type="email" id="email" required />
        </div>
        <div class="form-group">
            <label for="password">Password</label>
            <input type="password" id="password" required />
        </div>
        <button type="submit" class="btn-submit">Login</button>
    </form>
    <p>Don't have an account? <a href="/signup">Sign up</a></p>
</div>

<style>
    /* TODO: Add auth styling */
    .auth-card {
        max-width: 400px;
        margin: 4rem auto;
        padding: 2rem;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
    }
    .form-group {
        margin-bottom: 1rem;
        text-align: left;
    }
    .form-group label {
        display: block;
        margin-bottom: 0.5rem;
    }
    .form-group input {
        width: 100%;
        padding: 0.5rem;
        border: 1px solid #cbd5e0;
        border-radius: 4px;
    }
    .btn-submit {
        width: 100%;
        padding: 0.75rem;
        background-color: #3182ce;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
    }
</style>
