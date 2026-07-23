<script lang="ts">
    // TODO: Implement school searching, filtering, and apply-to-many selection
</script>

<div class="discover-page">
    <h2>Discover Schools & Programs</h2>
    <p>Search and discover universities in Cameroon. Select multiple to apply at once.</p>

    <div class="search-bar">
        <input type="text" placeholder="Search by school name, location, or program..." />
        <button class="btn-search">Search</button>
    </div>

    <!-- Apply-to-many Action Bar -->
    <div class="batch-apply-bar">
        <span>0 schools selected</span>
        <button class="btn-batch-apply" disabled>Apply to Selected</button>
    </div>

    <div class="schools-grid">
        <!-- TODO: List schools with checkbox selection and details view -->
        <p>Loading schools...</p>
    </div>
</div>

<style>
    /* TODO: Add discover and search page UI styling */
    .search-bar {
        display: flex;
        gap: 1rem;
        margin: 2rem 0;
    }
    .search-bar input {
        flex: 1;
        padding: 0.75rem;
        border: 1px solid #cbd5e0;
        border-radius: 4px;
    }
    .btn-search {
        padding: 0.75rem 1.5rem;
        background-color: #2b6cb0;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
    }
    .batch-apply-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #ebf8ff;
        padding: 1rem;
        border-radius: 6px;
        margin-bottom: 2rem;
    }
    .btn-batch-apply {
        padding: 0.5rem 1rem;
        background-color: #3182ce;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
    }
    .btn-batch-apply:disabled {
        background-color: #a0aec0;
        cursor: not-allowed;
    }
</style>
