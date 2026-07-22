<script lang="ts">
    // TODO: Fetch and display application status statistics and recent activity
</script>

<div class="dashboard-page">
    <h2>Dashboard</h2>
    <p>Welcome to your ApplyCM dashboard. Track your university applications here!!!.</p>

    <div class="stats-grid">
        <div class="stat-card">
            <h3>Applications</h3>
            <p class="stat-number">0</p>
        </div>
        <div class="stat-card">
            <h3>Favorites</h3>
            <p class="stat-number">0</p>
        </div>
        <div class="stat-card">
            <h3>Required Documents</h3>
            <p class="stat-number">0</p>
        </div>
    </div>
</div>

<style>
    /* TODO: Add dashboard layout and statistics UI styling */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin-top: 2rem;
    }
    .stat-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    .stat-number {
        font-size: 2rem;
        font-weight: bold;
        color: #2b6cb0;
        margin-top: 0.5rem;
    }
</style>
