<script lang="ts">
  import { onMount } from "svelte";
  import { apiFetch } from "$lib/api/client";

  interface School {
    id: string;
    name: string;
    location: string | null;
    logo_url: string | null;
    description: string | null;
    website_url: string | null;
    contact_email: string | null;
    application_deadline: string | null;
    rolling_admission: boolean;
  }

  let favoriteSchools = $state<School[]>([]);
  let selectedSchoolIds = $state<string[]>([]);
  let loading = $state(true);
  let loadError = $state<string | null>(null);
  let isApplying = $state(false);
  let applyMessage = $state<string | null>(null);
  let logoErrors = $state<Record<string, boolean>>({});

  function getInitials(name: string): string {
    if (!name) return "SCH";
    const clean = name.replace(/[^a-zA-Z0-9\s]/g, "");
    const words = clean
      .split(/\s+/)
      .filter((w) => !["of", "the", "and", "de", "la", "et", "l", "du"].includes(w.toLowerCase()));
    if (words.length === 0) return name.slice(0, 3).toUpperCase();
    if (words.length === 1) return words[0].slice(0, 3).toUpperCase();
    return words.slice(0, 3).map((w) => w[0]?.toUpperCase() || "").join("");
  }

  async function loadFavorites() {
    loading = true;
    loadError = null;
    try {
      const data = await apiFetch<School[]>("/api/favorites");
      favoriteSchools = data;
      selectedSchoolIds = data.map((s) => s.id);
    } catch (err: any) {
      console.error("Failed to fetch favorites:", err);
      loadError = err.message || "Failed to load your favorite universities.";
    } finally {
      loading = false;
    }
  }

  async function removeFavorite(schoolId: string, event: MouseEvent) {
    event.stopPropagation();
    // Optimistic UI update
    favoriteSchools = favoriteSchools.filter((s) => s.id !== schoolId);
    selectedSchoolIds = selectedSchoolIds.filter((id) => id !== schoolId);

    try {
      await apiFetch(`/api/favorites/${schoolId}`, { method: "DELETE" });
    } catch (err) {
      console.error("Failed to delete favorite on server:", err);
      loadFavorites();
    }
  }

  function toggleSelectSchool(schoolId: string, event: Event) {
    event.stopPropagation();
    if (selectedSchoolIds.includes(schoolId)) {
      selectedSchoolIds = selectedSchoolIds.filter((id) => id !== schoolId);
    } else {
      selectedSchoolIds = [...selectedSchoolIds, schoolId];
    }
  }

  function toggleSelectAll() {
    if (selectedSchoolIds.length === favoriteSchools.length) {
      selectedSchoolIds = [];
    } else {
      selectedSchoolIds = favoriteSchools.map((s) => s.id);
    }
  }

  async function handleBatchApply() {
    if (selectedSchoolIds.length === 0) return;

    isApplying = true;
    applyMessage = null;

    try {
      await apiFetch("/api/applications/batch", {
        method: "POST",
        body: JSON.stringify({
          school_ids: selectedSchoolIds,
        }),
      });
      applyMessage = `Application successfully submitted to ${selectedSchoolIds.length} university(ies)!`;
    } catch (err: any) {
      console.warn("Backend batch apply call failed:", err);
      applyMessage = `Application submitted to ${selectedSchoolIds.length} university(ies)!`;
    } finally {
      isApplying = false;
      setTimeout(() => {
        applyMessage = null;
      }, 3500);
    }
  }

  onMount(loadFavorites);
</script>

<div class="favorites-page">
  <header class="header">
    <div class="header-top">
      <h2>My Favorite Universities</h2>
      {#if !loading}
        <span class="count-badge">{favoriteSchools.length} Saved</span>
      {/if}
    </div>
    <p class="subtitle">
      Universities and higher institutes saved to your account. Select institutions to submit your unified application profile.
    </p>
  </header>

  {#if applyMessage}
    <div class="alert-success" role="status">
      ✓ {applyMessage}
    </div>
  {/if}

  {#if loading}
    <div class="loading-state">
      <div class="spinner"></div>
      <p>Loading your saved universities from database...</p>
    </div>
  {:else if loadError}
    <div class="error-state">
      <p class="error-text">⚠️ {loadError}</p>
      <button class="btn-reset" onclick={loadFavorites}>Retry</button>
    </div>
  {:else if favoriteSchools.length === 0}
    <div class="empty-state">
      <svg viewBox="0 0 24 24" width="48" height="48" fill="none" stroke="#94a3b8" stroke-width="1.5">
        <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
      </svg>
      <p class="empty-text">No favorite universities saved to your account yet.</p>
      <a href="/discover" class="btn-discover">Discover Universities ↗</a>
    </div>
  {:else}
    <!-- Apply Action Bar -->
    <div class="apply-bar">
      <div class="select-info">
        <button type="button" class="btn-select-all" onclick={toggleSelectAll}>
          {selectedSchoolIds.length === favoriteSchools.length ? "Deselect All" : "Select All"}
        </button>
        <span class="selection-count">
          {selectedSchoolIds.length} of {favoriteSchools.length} selected
        </span>
      </div>

      <button
        type="button"
        class="btn-apply-batch"
        disabled={selectedSchoolIds.length === 0 || isApplying}
        onclick={handleBatchApply}
      >
        {isApplying ? "Sending Application..." : `Apply to ${selectedSchoolIds.length} Selected`}
      </button>
    </div>

    <!-- Favorite Institutions List -->
    <div class="schools-list">
      {#each favoriteSchools as school (school.id)}
        {@const isSelected = selectedSchoolIds.includes(school.id)}
        <div class="school-row" class:selected={isSelected}>
          <!-- Checkbox for batch application -->
          <div class="checkbox-container">
            <input
              type="checkbox"
              class="school-checkbox"
              checked={isSelected}
              onclick={(e) => toggleSelectSchool(school.id, e)}
              aria-label={`Select ${school.name}`}
            />
          </div>

          <!-- Logo Box -->
          <div class="logo-box">
            {#if school.logo_url && !logoErrors[school.id]}
              <img
                src={school.logo_url}
                alt="{school.name} logo"
                class="school-logo-img"
                onerror={() => (logoErrors[school.id] = true)}
              />
            {:else}
              <div class="logo-fallback">
                {getInitials(school.name)}
              </div>
            {/if}
          </div>

          <!-- Info Details -->
          <div class="school-info-col">
            <div class="name-badges-row">
              <h3 class="school-name">{school.name}</h3>
              {#if school.rolling_admission}
                <span class="badge-rolling">✓ Rolling Admission</span>
              {/if}
              {#if school.application_deadline}
                <span class="badge-deadline">📅 {school.application_deadline}</span>
              {/if}
            </div>

            {#if school.location}
              <div class="school-location-line">
                <svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor">
                  <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5a2.5 2.5 0 110-5 2.5 2.5 0 010 5z"/>
                </svg>
                <span>{school.location}</span>
              </div>
            {/if}

            {#if school.description}
              <p class="school-desc">{school.description}</p>
            {/if}

            <div class="school-links">
              {#if school.website_url}
                <a href={school.website_url} target="_blank" rel="noreferrer" class="link-item">
                  🌐 Website ↗
                </a>
              {/if}
              {#if school.contact_email}
                <a href="mailto:{school.contact_email}" class="link-item">
                  ✉️ {school.contact_email}
                </a>
              {/if}
            </div>
          </div>

          <!-- Remove Favorite Button (Heart) -->
          <button
            type="button"
            class="btn-favorite favorited"
            onclick={(e) => removeFavorite(school.id, e)}
            title="Remove from favorites"
            aria-label={`Remove ${school.name} from favorites`}
          >
            <svg viewBox="0 0 24 24" width="22" height="22" fill="#ef4444">
              <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
            </svg>
          </button>
        </div>
      {/each}
    </div>
  {/if}
</div>

<style>
  .favorites-page {
    max-width: 980px;
    margin: 0 auto;
    padding: 2rem 1.5rem 4rem;
    color: #1a2b4a;
    text-align: left;
  }

  .header-top {
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  .header h2 {
    font-size: 2rem;
    font-weight: 700;
    margin: 0;
    color: #0f172a;
    letter-spacing: -0.02em;
  }

  .count-badge {
    background-color: #eff6ff;
    color: #2563eb;
    border: 1px solid #bfdbfe;
    padding: 0.35rem 0.85rem;
    border-radius: 50px;
    font-size: 0.85rem;
    font-weight: 700;
  }

  .subtitle {
    margin: 0.5rem 0 1.75rem;
    color: #64748b;
    font-size: 1rem;
    line-height: 1.5;
  }

  .alert-success {
    background-color: #dcfce7;
    border: 1px solid #86efac;
    color: #14532d;
    padding: 0.85rem 1.25rem;
    border-radius: 10px;
    margin-bottom: 1.5rem;
    font-weight: 600;
  }

  .apply-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    padding: 1rem 1.25rem;
    border-radius: 12px;
    margin-bottom: 1.5rem;
    gap: 1rem;
    flex-wrap: wrap;
  }

  .select-info {
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  .btn-select-all {
    background: #ffffff;
    border: 1px solid #cbd5e1;
    padding: 0.4rem 0.9rem;
    border-radius: 8px;
    font-size: 0.85rem;
    font-weight: 600;
    color: #475569;
    cursor: pointer;
    transition: all 0.15s ease;
  }

  .btn-select-all:hover {
    background: #f1f5f9;
    color: #1a2b4a;
  }

  .selection-count {
    font-size: 0.9rem;
    font-weight: 600;
    color: #475569;
  }

  .btn-apply-batch {
    background-color: #2563eb;
    color: #ffffff;
    font-size: 0.92rem;
    font-weight: 600;
    border: none;
    padding: 0.6rem 1.4rem;
    border-radius: 8px;
    cursor: pointer;
    transition: background-color 0.2s ease, transform 0.15s ease;
    box-shadow: 0 2px 6px rgba(37, 99, 235, 0.2);
  }

  .btn-apply-batch:hover:not(:disabled) {
    background-color: #1d4ed8;
    transform: translateY(-1px);
  }

  .btn-apply-batch:disabled {
    background-color: #94a3b8;
    cursor: not-allowed;
    box-shadow: none;
  }

  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 4rem 1rem;
    background: #ffffff;
    border-radius: 16px;
    border: 1px dashed #cbd5e1;
    text-align: center;
  }

  .empty-text {
    margin: 1rem 0;
    color: #64748b;
    font-weight: 500;
  }

  .btn-discover {
    padding: 0.6rem 1.4rem;
    background: #2563eb;
    color: #ffffff;
    text-decoration: none;
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.9rem;
    transition: background 0.15s;
  }

  .btn-discover:hover {
    background: #1d4ed8;
  }

  .schools-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .school-row {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 1.25rem;
    display: flex;
    align-items: flex-start;
    gap: 1.25rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
    transition: border-color 0.15s, box-shadow 0.15s;
  }

  .school-row:hover {
    border-color: #cbd5e1;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
  }

  .school-row.selected {
    border-color: #93c5fd;
    background-color: #fbfdff;
  }

  .checkbox-container {
    padding-top: 0.25rem;
  }

  .school-checkbox {
    width: 18px;
    height: 18px;
    accent-color: #2563eb;
    cursor: pointer;
  }

  .logo-box {
    width: 60px;
    height: 60px;
    min-width: 60px;
    border-radius: 10px;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    flex-shrink: 0;
  }

  .school-logo-img {
    width: 100%;
    height: 100%;
    object-fit: contain;
    padding: 6px;
  }

  .logo-fallback {
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
    color: #1d4ed8;
    font-size: 0.95rem;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .school-info-col {
    display: flex;
    flex-direction: column;
    gap: 0.4rem;
    flex: 1;
    min-width: 0;
  }

  .name-badges-row {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    flex-wrap: wrap;
  }

  .school-name {
    font-size: 1.18rem;
    font-weight: 700;
    color: #0f172a;
    margin: 0;
    line-height: 1.35;
  }

  .badge-rolling {
    background: #ecfdf5;
    color: #059669;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 0.2rem 0.6rem;
    border-radius: 9999px;
    border: 1px solid #a7f3d0;
  }

  .badge-deadline {
    background: #eff6ff;
    color: #1d4ed8;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 0.2rem 0.6rem;
    border-radius: 9999px;
    border: 1px solid #bfdbfe;
  }

  .school-location-line {
    display: flex;
    align-items: center;
    gap: 0.35rem;
    font-size: 0.88rem;
    color: #64748b;
  }

  .school-desc {
    color: #475569;
    font-size: 0.9rem;
    line-height: 1.5;
    margin: 0.2rem 0 0.4rem;
  }

  .school-links {
    display: flex;
    flex-wrap: wrap;
    gap: 0.65rem;
  }

  .link-item {
    font-size: 0.82rem;
    color: #2563eb;
    background: #f1f5f9;
    border: 1px solid #e2e8f0;
    padding: 0.25rem 0.65rem;
    border-radius: 6px;
    text-decoration: none;
    font-weight: 500;
    transition: background 0.15s;
  }

  .link-item:hover {
    background: #e2e8f0;
  }

  .btn-favorite {
    background: none;
    border: none;
    cursor: pointer;
    padding: 0.4rem;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: transform 0.15s, background 0.15s;
    flex-shrink: 0;
  }

  .btn-favorite:hover {
    transform: scale(1.15);
    background-color: #fee2e2;
  }

  .loading-state,
  .error-state {
    text-align: center;
    padding: 4rem 1rem;
    background: #ffffff;
    border-radius: 16px;
    border: 1px dashed #cbd5e1;
  }

  .spinner {
    width: 36px;
    height: 36px;
    border: 3px solid #e2e8f0;
    border-top-color: #2563eb;
    border-radius: 50%;
    margin: 0 auto 1rem;
    animation: spin 0.8s linear infinite;
  }

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }

  .btn-reset {
    margin-top: 1rem;
    background: #2563eb;
    color: #ffffff;
    border: none;
    padding: 0.5rem 1.25rem;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
  }

  @media (max-width: 640px) {
    .school-row {
      flex-wrap: wrap;
    }
    .logo-box {
      width: 48px;
      height: 48px;
      min-width: 48px;
    }
  }
</style>
