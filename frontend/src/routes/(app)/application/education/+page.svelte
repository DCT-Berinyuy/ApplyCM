<script lang="ts">
    // TODO: Connect education fields (high school, grades, diploma url) to student profile API
</script>

<div class="step-page">
    <h3>Education History</h3>
    <form onsubmit={(e) => e.preventDefault()}>
        <!-- TODO: Form fields for High School, Baccalaureate/A-Level results, and documents upload -->
        <p>Education history fields placeholder.</p>
        <button type="submit" class="btn-save">Save & Continue</button>
    </form>
</div>

<style>
    /* TODO: Add education step form styling */
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
