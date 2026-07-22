<script lang="ts">
    // TODO: Connect personal statement essays and uploads to database
</script>

<div class="step-page">
    <h3>Writing & Personal Statement</h3>
    <form onsubmit={(e) => e.preventDefault()}>
        <!-- TODO: Form fields for Statement of Purpose and other custom essay prompts -->
        <p>Personal statement fields placeholder.</p>
        <button type="submit" class="btn-save">Submit Profile</button>
    </form>
</div>

<style>
    /* TODO: Add writing step form styling */
    .step-page {
        text-align: left;
    }
    .btn-save {
        margin-top: 2rem;
        padding: 0.5rem 1rem;
        background-color: #3182ce;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
    }
</style>
