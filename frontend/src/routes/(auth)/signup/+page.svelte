<script lang="ts">
    // TODO: Implement signup form submission and validation
</script>

<div class="auth-card">
    <h2>Create your ApplyCM Account</h2>
    <form onsubmit={(e) => e.preventDefault()}>
        <div class="form-group">
            <label for="email">Email Address</label>
            <input type="email" id="email" required />
        </div>
        <div class="form-group">
            <label for="password">Password</label>
            <input type="password" id="password" required />
        </div>
        <div class="form-group">
            <label for="confirm-password">Confirm Password</label>
            <input type="password" id="confirm-password" required />
        </div>
        <button type="submit" class="btn-submit">Sign Up</button>
    </form>
    <p>Already have an account? <a href="/login">Login</a></p>
</div>

<style>
    /* TODO: Add signup page specific styling */
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
        background-color: #38a169;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
    }
</style>
