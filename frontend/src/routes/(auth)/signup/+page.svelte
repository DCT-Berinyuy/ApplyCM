<script lang="ts">
//support@fapshi.com
    let email = "";
    let password = "";
    let confirmPassword = "";
    let isSeen = true;
    let isLoading = false;

    async function signup() {
        if (password.length < 6) {
            alert("Password must be at least 6 characters long!");
            return;
        }
        if (password !== confirmPassword) {
            alert("Passwords do not match!");
            return;
        }
        isLoading = true;
        try {
            const response = await fetch("/api/signup", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ email, password }),
            });

            if (!response.ok) {
                throw new Error("Signup failed");
            }

            // Handle successful signup (e.g., redirect to login page)
            window.location.href = "/dashboard";
        } catch (error) {
            console.error(error);
            alert("An error occurred during signup. Please try again.");
        }
        finally {
            isLoading = false;
        }
    }
</script>

<div class="auth-card">
    <h2 class="auth-card-title">Create your ApplyCM Account</h2>
    <form onsubmit={(event) => { event.preventDefault(); signup(); }}>
        <div class="form-group">
            <label for="email">Email Address</label>
            <input type="email" id="email" required bind:value={email} disabled={isLoading} />
        </div>
        <div class="form-group">
            <label for="password">Password</label>
            <div class="password-container">
                <input type={isSeen ? "text" : "password"} id="password" required bind:value={password}>
                
            </div>
        </div>
        <div class="form-group">
            <label for="confirm-password">Confirm Password</label>
            <input type="password" id="confirm-password" required bind:value={confirmPassword} disabled={isLoading} />
        </div>
        <button type="submit" class="btn-submit" disabled={isLoading}>{#if isLoading}Signing up...{:else}Sign Up{/if}</button>
    </form>
    <p>Already have an account? <a href="/login">Login</a></p>
</div>

<style>

    .auth-card {
        max-width: 400px;
        margin: 7rem auto;
        padding: 2rem;
        border: 1px solid #96bef3;
        border-radius: 40px;
        border-width: 0.5px;
        box-shadow: 0 4px 8px rgb(51, 132, 238)
    }
    .auth-card:hover {
        box-shadow: 0 10px 16px rgba(0, 0, 0, 0.5);
        transition: box-shadow 0.5s ease-in-out;
        transform: translateY(-2px);
    }
    .auth-card-title {
        text-align: center;
        margin-bottom: 1.5rem;
        color: #2b6cb0;
    }
    .form-group {
        margin-bottom: 1.5rem;
        text-align: left;
    }
    .form-group label {
        display: block;
        margin-bottom: 0.5rem;
    }
    .form-group input {
        width: 95%;
        padding: 0.5rem;
        border: 1px solid #cbd5e0;
        border-radius: 50px;
    }
    .btn-submit {
        width: 100%;
        padding: 0.75rem;
        background-color: #38a169;
        color: white;
        border: none;
        border-radius: 50px;
        cursor: pointer;
    }
    .password-container {
        position: relative;
    }
    .eye-btn {
        position: absolute;
        right: 10px;
        top: 50%;
        transform: translateY(-50%);
        background: none;
        border: none;
        cursor: pointer;
        font-size: 1.2rem;
    }
</style>
