<script lang="ts">
    // TODO: Connect personal details form fields to student profile store/API
</script>

<div class="step-page">
    <h3>Personal Details</h3>
    <form onsubmit={(e) => e.preventDefault()}>
        <!-- TODO: Form fields for Name, Phone, National ID, Address, etc. -->
        <p>Personal profile fields placeholder.</p>
        <button type="submit" class="btn-save">Save & Continue</button>
    </form>
</div>

<style>
    /* TODO: Add step form styling */
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
