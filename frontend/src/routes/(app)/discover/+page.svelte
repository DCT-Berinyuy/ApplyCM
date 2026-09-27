<script lang="ts">
  import { onMount } from "svelte";
  import { API_BASE_URL } from "$lib/config";

  interface Program {
    id: string;
    school_id: string;
    field_of_study: string;
    degree_type: string | null;
    tuition_fee: string | null;
    duration: string | null;
    language_of_instruction: string | null;
    delivery_mode: string | null;
    admission_requirements: string | null;
    required_documents: string | null;
    application_deadline: string | null;
    class_size: number | null;
    description: string | null;
  }

  interface School {
    id: string;
    name: string;
    location: string | null;
    description: string | null;
    website_url: string | null;
    logo_url: string | null;
    contact_email: string | null;
    application_deadline: string | null;
    rolling_admission: boolean;
    created_at?: string;
    programs?: Program[];
  }

  let schools = $state<School[]>([]);
  let loading = $state(true);
  let loadError = $state<string | null>(null);
  let searchQuery = $state("");
  let selectedFilter = $state("All");
  let selectedSchoolId = $state<string | null>(null);
  let favoriteIds = $state<string[]>([]);

  const selectedSchool = $derived(
    schools.find((s) => s.id === selectedSchoolId) || null
  );

  const DEGREE_FILTERS = ["All", "Bachelor", "Engineering", "Master", "Licence Pro", "HND"];

  async function fetchSchools() {
    loading = true;
    loadError = null;
    try {
      const res = await fetch(`${API_BASE_URL}/api/schools`);
      if (!res.ok) {
        throw new Error(`Failed to load schools: HTTP ${res.status}`);
      }
      const data: School[] = await res.json();
      schools = data;

      // Pre-fetch programs for each school in background for instant search matching
      for (const school of schools) {
        fetchProgramsForSchool(school.id);
      }
    } catch (err: any) {
      console.error("Failed to fetch schools from backend API:", err);
      loadError = err.message || "Failed to load universities from server.";
    } finally {
      loading = false;
    }
  }

  async function fetchProgramsForSchool(schoolId: string) {
    try {
      const res = await fetch(`${API_BASE_URL}/api/schools/${schoolId}/programs`);
      if (res.ok) {
        const progs: Program[] = await res.json();
        const index = schools.findIndex((s) => s.id === schoolId);
        if (index !== -1) {
          schools[index] = { ...schools[index], programs: progs };
        }
      }
    } catch (err) {
      console.warn(`Could not load programs for school ${schoolId}:`, err);
    }
  }

  function loadFavorites() {
    if (typeof window !== "undefined") {
      try {
        const stored = localStorage.getItem("favorite_school_ids");
        if (stored) {
          favoriteIds = JSON.parse(stored);
        }
      } catch (err) {
        favoriteIds = [];
      }
    }
  }

  function toggleFavorite(schoolId: string, event: MouseEvent) {
    event.stopPropagation();
    if (favoriteIds.includes(schoolId)) {
      favoriteIds = favoriteIds.filter((id) => id !== schoolId);
    } else {
      favoriteIds = [...favoriteIds, schoolId];
    }

    if (typeof window !== "undefined") {
      localStorage.setItem("favorite_school_ids", JSON.stringify(favoriteIds));
      const favObjects = schools.filter((s) => favoriteIds.includes(s.id));
      localStorage.setItem("favorite_schools_list", JSON.stringify(favObjects));
    }

    fetch(`${API_BASE_URL}/api/favorites`, {
      method: favoriteIds.includes(schoolId) ? "POST" : "DELETE",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ school_id: schoolId }),
    }).catch(() => {});
  }

  function openSchoolDetail(schoolId: string) {
    selectedSchoolId = schoolId;
    const school = schools.find((s) => s.id === schoolId);
    if (school && !school.programs) {
      fetchProgramsForSchool(schoolId);
    }
    if (typeof document !== "undefined") {
      document.body.style.overflow = "hidden";
    }
  }

  function closeSchoolDetail() {
    selectedSchoolId = null;
    if (typeof document !== "undefined") {
      document.body.style.overflow = "";
    }
  }

  onMount(() => {
    loadFavorites();
    fetchSchools();

    return () => {
      if (typeof document !== "undefined") {
        document.body.style.overflow = "";
      }
    };
  });

  const filteredSchools = $derived(
    schools.filter((s) => {
      const query = searchQuery.toLowerCase().trim();
      const hasProgramsMatch = s.programs?.some((p) =>
        p.field_of_study.toLowerCase().includes(query) ||
        (p.degree_type && p.degree_type.toLowerCase().includes(query)) ||
        (p.description && p.description.toLowerCase().includes(query))
      );

      const matchesSearch =
        !query ||
        s.name.toLowerCase().includes(query) ||
        (s.location && s.location.toLowerCase().includes(query)) ||
        (s.description && s.description.toLowerCase().includes(query)) ||
        hasProgramsMatch;

      const matchesDegree =
        selectedFilter === "All" ||
        s.programs?.some((p) => p.degree_type === selectedFilter);

      return matchesSearch && matchesDegree;
    })
  );
</script>

<svelte:window
  onkeydown={(e) => {
    if (e.key === "Escape" && selectedSchoolId) {
      closeSchoolDetail();
    }
  }}
/>

<div class="discover-page">
  <header class="header">
    <h2>Discover Universities & Higher Institutes</h2>
    <p class="subtitle">
      Browse verified higher institutions across Cameroon. Select an institution to view its full profile, accredited degree programs, tuition fees, and admission criteria.
    </p>
  </header>

  <div class="filter-section">
    <div class="search-box">
      <svg class="search-icon" viewBox="0 0 24 24" width="20" height="20">
        <path
          d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
          stroke="#64748b"
          stroke-width="2"
          stroke-linecap="round"
          fill="none"
        />
      </svg>
      <input
        type="text"
        placeholder="Search by school name, location, degree type, or field of study..."
        bind:value={searchQuery}
      />
      {#if searchQuery}
        <button class="btn-clear" onclick={() => (searchQuery = "")} aria-label="Clear search">✕</button>
      {/if}
    </div>

    <div class="degree-chips">
      <span class="chips-label">Filter by Degree:</span>
      {#each DEGREE_FILTERS as filter}
        <button
          type="button"
          class="chip"
          class:active={selectedFilter === filter}
          onclick={() => (selectedFilter = filter)}
        >
          {filter}
        </button>
      {/each}
    </div>
  </div>

  {#if loading}
    <div class="loading-state">
      <div class="spinner"></div>
      <p>Loading schools and programs from database...</p>
    </div>
  {:else if loadError}
    <div class="error-state">
      <p class="error-text">⚠️ {loadError}</p>
      <button class="btn-reset" onclick={fetchSchools}>Retry</button>
    </div>
  {:else if filteredSchools.length === 0}
    <div class="empty-state">
      <p>No universities found matching your filter.</p>
      <button
        class="btn-reset"
        onclick={() => {
          searchQuery = "";
          selectedFilter = "All";
        }}>Reset Filters</button
      >
    </div>
  {:else}
    <!-- 1. List view (default state: Minimal card showing Name, Location, and Heart icon) -->
    <div class="schools-list">
      {#each filteredSchools as school (school.id)}
        {@const isFav = favoriteIds.includes(school.id)}
        <div class="school-list-card">
          <div class="card-content">
            <button
              type="button"
              class="school-name-link"
              onclick={() => openSchoolDetail(school.id)}
            >
              {school.name}
            </button>

            {#if school.location}
              <div class="location-line">
                <svg viewBox="0 0 24 24" width="15" height="15" fill="currentColor">
                  <path
                    d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5a2.5 2.5 0 110-5 2.5 2.5 0 010 5z"
                  />
                </svg>
                <span>{school.location}</span>
              </div>
            {/if}
          </div>

          <!-- Favorite (heart) button stays on the list card only -->
          <button
            type="button"
            class="btn-favorite"
            class:favorited={isFav}
            onclick={(e) => toggleFavorite(school.id, e)}
            title={isFav ? "Remove from favorites" : "Add to favorites"}
            aria-label={isFav ? `Remove ${school.name} from favorites` : `Add ${school.name} to favorites`}
          >
            {#if isFav}
              <svg viewBox="0 0 24 24" width="22" height="22" fill="#ef4444">
                <path
                  d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"
                />
              </svg>
            {:else}
              <svg
                viewBox="0 0 24 24"
                width="22"
                height="22"
                fill="none"
                stroke="#94a3b8"
                stroke-width="2"
              >
                <path
                  d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"
                />
              </svg>
            {/if}
          </button>
        </div>
      {/each}
    </div>
  {/if}
</div>

<!-- 2. Detail View (slide-over drawer panel on the same page, no route navigation) -->
{#if selectedSchool}
  <div
    class="drawer-backdrop"
    onclick={closeSchoolDetail}
    role="presentation"
  ></div>

  <div
    class="detail-drawer"
    role="dialog"
    aria-modal="true"
    aria-labelledby="drawer-school-name"
  >
    <div class="drawer-header">
      <div class="drawer-header-top">
        <span class="drawer-category">Higher Education Institution</span>
        <button
          type="button"
          class="btn-close-drawer"
          onclick={closeSchoolDetail}
          aria-label="Close detail panel"
        >
          ✕
        </button>
      </div>

      <h3 id="drawer-school-name" class="drawer-title">{selectedSchool.name}</h3>

      {#if selectedSchool.location}
        <div class="drawer-location">
          <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
            <path
              d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5a2.5 2.5 0 110-5 2.5 2.5 0 010 5z"
            />
          </svg>
          <span>{selectedSchool.location}</span>
        </div>
      {/if}

      <!-- Status badges: Rolling Admission, Application Deadline -->
      <div class="drawer-badges">
        {#if selectedSchool.rolling_admission}
          <span class="badge-rolling">✓ Rolling Admission</span>
        {/if}
        {#if selectedSchool.application_deadline}
          <span class="badge-deadline">📅 Deadline: {selectedSchool.application_deadline}</span>
        {/if}
      </div>

      <!-- Action links: Website link, Contact email -->
      <div class="drawer-actions">
        {#if selectedSchool.website_url}
          <a
            href={selectedSchool.website_url}
            target="_blank"
            rel="noreferrer"
            class="link-action-pill"
          >
            🌐 Visit Website ↗
          </a>
        {/if}
        {#if selectedSchool.contact_email}
          <a
            href="mailto:{selectedSchool.contact_email}"
            class="link-action-pill"
          >
            ✉️ {selectedSchool.contact_email}
          </a>
        {/if}
      </div>
    </div>

    <div class="drawer-body">
      <!-- Full Description -->
      {#if selectedSchool.description}
        <section class="drawer-section">
          <h4 class="section-title">Overview</h4>
          <p class="drawer-desc">{selectedSchool.description}</p>
        </section>
      {/if}

      <!-- All Offered Programs -->
      <section class="drawer-section">
        <div class="section-header-row">
          <h4 class="section-title">Offered Academic Programs</h4>
          {#if selectedSchool.programs}
            <span class="program-count-tag">{selectedSchool.programs.length} Available</span>
          {/if}
        </div>

        {#if !selectedSchool.programs}
          <div class="loading-progs">
            <div class="spinner-small"></div>
            <span>Loading programs...</span>
          </div>
        {:else if selectedSchool.programs.length === 0}
          <p class="empty-progs">No academic programs currently listed for this institution.</p>
        {:else}
          <div class="programs-stack">
            {#each selectedSchool.programs as prog}
              <div class="program-card">
                <div class="prog-title-row">
                  <h5 class="prog-name">{prog.field_of_study}</h5>
                  {#if prog.degree_type}
                    <span class="degree-badge">{prog.degree_type}</span>
                  {/if}
                </div>

                <div class="prog-chips">
                  {#if prog.tuition_fee}
                    <span class="spec-pill tuition-pill">💰 {prog.tuition_fee}</span>
                  {/if}
                  {#if prog.duration}
                    <span class="spec-pill">⏱️ {prog.duration}</span>
                  {/if}
                  {#if prog.language_of_instruction}
                    <span class="spec-pill">🗣️ {prog.language_of_instruction}</span>
                  {/if}
                  {#if prog.delivery_mode}
                    <span class="spec-pill">🏫 {prog.delivery_mode}</span>
                  {/if}
                  {#if prog.class_size}
                    <span class="spec-pill">👥 Class Size: {prog.class_size}</span>
                  {/if}
                  {#if prog.application_deadline}
                    <span class="spec-pill">📅 Program Deadline: {prog.application_deadline}</span>
                  {/if}
                </div>

                {#if prog.description}
                  <p class="prog-description">{prog.description}</p>
                {/if}

                {#if prog.admission_requirements}
                  <div class="prog-detail-item">
                    <span class="detail-label">Admission Requirements:</span>
                    <span class="detail-text">{prog.admission_requirements}</span>
                  </div>
                {/if}

                {#if prog.required_documents}
                  <div class="prog-detail-item">
                    <span class="detail-label">Required Documents:</span>
                    <span class="detail-text">{prog.required_documents}</span>
                  </div>
                {/if}
              </div>
            {/each}
          </div>
        {/if}
      </section>
    </div>
  </div>
{/if}

<style>
  .discover-page {
    max-width: 960px;
    margin: 0 auto;
    padding: 2rem 1.5rem 4rem;
    color: #1a2b4a;
    text-align: left;
  }

  .header h2 {
    font-size: 2rem;
    font-weight: 700;
    margin: 0 0 0.5rem;
    color: #0f172a;
    letter-spacing: -0.02em;
  }

  .subtitle {
    color: #64748b;
    font-size: 1rem;
    margin-bottom: 2rem;
    line-height: 1.5;
  }

  .filter-section {
    margin-bottom: 2rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .search-box {
    position: relative;
    display: flex;
    align-items: center;
  }

  .search-icon {
    position: absolute;
    left: 1rem;
    pointer-events: none;
  }

  .search-box input {
    width: 100%;
    padding: 0.85rem 2.8rem 0.85rem 3rem;
    border: 1px solid #cbd5e1;
    border-radius: 12px;
    font-size: 0.95rem;
    background: #ffffff;
    color: #1e293b;
    outline: none;
    transition: border-color 0.2s, box-shadow 0.2s;
  }

  .search-box input:focus {
    border-color: #2563eb;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
  }

  .btn-clear {
    position: absolute;
    right: 1rem;
    background: none;
    border: none;
    color: #94a3b8;
    cursor: pointer;
    font-size: 1rem;
    padding: 0.25rem;
    line-height: 1;
  }

  .degree-chips {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.5rem;
  }

  .chips-label {
    font-size: 0.85rem;
    font-weight: 600;
    color: #64748b;
    margin-right: 0.25rem;
  }

  .chip {
    background: #f1f5f9;
    border: 1px solid #e2e8f0;
    color: #475569;
    padding: 0.35rem 0.85rem;
    border-radius: 9999px;
    font-size: 0.85rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
  }

  .chip:hover {
    background: #e2e8f0;
  }

  .chip.active {
    background: #2563eb;
    color: #ffffff;
    border-color: #2563eb;
  }

  /* List view: minimal card showing Name, Location, and Heart */
  .schools-list {
    display: flex;
    flex-direction: column;
    gap: 0.85rem;
  }

  .school-list-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1.5rem;
    transition: border-color 0.2s, box-shadow 0.2s, transform 0.15s;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
  }

  .school-list-card:hover {
    border-color: #93c5fd;
    box-shadow: 0 4px 14px rgba(37, 99, 235, 0.08);
    transform: translateY(-1px);
  }

  .card-content {
    display: flex;
    flex-direction: column;
    gap: 0.4rem;
    flex: 1;
    min-width: 0;
  }

  .school-name-link {
    background: none;
    border: none;
    padding: 0;
    margin: 0;
    font-size: 1.18rem;
    font-weight: 700;
    color: #0f172a;
    text-align: left;
    cursor: pointer;
    line-height: 1.35;
    transition: color 0.15s;
  }

  .school-name-link:hover {
    color: #2563eb;
    text-decoration: underline;
    text-underline-offset: 3px;
  }

  .location-line {
    display: flex;
    align-items: center;
    gap: 0.35rem;
    font-size: 0.88rem;
    color: #64748b;
  }

  .btn-favorite {
    background: none;
    border: none;
    cursor: pointer;
    padding: 0.5rem;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: transform 0.15s, background-color 0.15s;
    flex-shrink: 0;
  }

  .btn-favorite:hover {
    transform: scale(1.15);
    background-color: #fee2e2;
  }

  .btn-favorite.favorited:hover {
    background-color: #fee2e2;
  }

  /* States */
  .loading-state,
  .empty-state,
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

  .spinner-small {
    width: 18px;
    height: 18px;
    border: 2px solid #e2e8f0;
    border-top-color: #2563eb;
    border-radius: 50%;
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

  /* Detail View: Slide-Over Drawer Overlay */
  .drawer-backdrop {
    position: fixed;
    inset: 0;
    background: rgba(15, 23, 42, 0.45);
    backdrop-filter: blur(3px);
    z-index: 1000;
    animation: fadeIn 0.2s ease-out;
  }

  @keyframes fadeIn {
    from {
      opacity: 0;
    }
    to {
      opacity: 1;
    }
  }

  .detail-drawer {
    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
    width: 620px;
    max-width: 95vw;
    background: #ffffff;
    z-index: 1001;
    box-shadow: -8px 0 32px rgba(15, 23, 42, 0.15);
    display: flex;
    flex-direction: column;
    overflow-y: auto;
    animation: slideIn 0.28s cubic-bezier(0.16, 1, 0.3, 1);
  }

  @keyframes slideIn {
    from {
      transform: translateX(100%);
    }
    to {
      transform: translateX(0);
    }
  }

  .drawer-header {
    padding: 1.75rem 2rem 1.5rem;
    background: #f8fafc;
    border-bottom: 1px solid #e2e8f0;
    position: sticky;
    top: 0;
    z-index: 10;
  }

  .drawer-header-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.65rem;
  }

  .drawer-category {
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #2563eb;
  }

  .btn-close-drawer {
    background: #e2e8f0;
    border: none;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #475569;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.15s, color 0.15s;
  }

  .btn-close-drawer:hover {
    background: #cbd5e1;
    color: #0f172a;
  }

  .drawer-title {
    font-size: 1.6rem;
    font-weight: 800;
    color: #0f172a;
    margin: 0 0 0.5rem;
    line-height: 1.25;
  }

  .drawer-location {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.92rem;
    color: #64748b;
    margin-bottom: 0.85rem;
  }

  .drawer-badges {
    display: flex;
    flex-wrap: wrap;
    gap: 0.6rem;
    margin-bottom: 1rem;
  }

  .badge-rolling {
    background: #ecfdf5;
    color: #059669;
    font-size: 0.78rem;
    font-weight: 600;
    padding: 0.25rem 0.7rem;
    border-radius: 9999px;
    border: 1px solid #a7f3d0;
  }

  .badge-deadline {
    background: #eff6ff;
    color: #1d4ed8;
    font-size: 0.78rem;
    font-weight: 600;
    padding: 0.25rem 0.7rem;
    border-radius: 9999px;
    border: 1px solid #bfdbfe;
  }

  .drawer-actions {
    display: flex;
    flex-wrap: wrap;
    gap: 0.65rem;
  }

  .link-action-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.85rem;
    color: #1d4ed8;
    background: #ffffff;
    border: 1px solid #bfdbfe;
    padding: 0.4rem 0.9rem;
    border-radius: 8px;
    text-decoration: none;
    font-weight: 600;
    transition: background 0.15s, border-color 0.15s;
  }

  .link-action-pill:hover {
    background: #eff6ff;
    border-color: #93c5fd;
  }

  .drawer-body {
    padding: 1.75rem 2rem 3rem;
    display: flex;
    flex-direction: column;
    gap: 2rem;
  }

  .drawer-section {
    display: flex;
    flex-direction: column;
    gap: 0.85rem;
  }

  .section-header-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .section-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #0f172a;
    margin: 0;
  }

  .program-count-tag {
    font-size: 0.8rem;
    font-weight: 600;
    background: #f1f5f9;
    color: #475569;
    padding: 0.2rem 0.6rem;
    border-radius: 6px;
  }

  .drawer-desc {
    color: #334155;
    font-size: 0.95rem;
    line-height: 1.65;
    margin: 0;
  }

  .loading-progs {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    font-size: 0.9rem;
    color: #64748b;
    padding: 1rem 0;
  }

  .empty-progs {
    font-size: 0.9rem;
    color: #64748b;
    font-style: italic;
    margin: 0;
  }

  .programs-stack {
    display: flex;
    flex-direction: column;
    gap: 1.15rem;
  }

  .program-card {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 1.25rem;
    display: flex;
    flex-direction: column;
    gap: 0.65rem;
    text-align: left;
  }

  .prog-title-row {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 0.75rem;
    flex-wrap: wrap;
  }

  .prog-name {
    font-size: 1.05rem;
    font-weight: 700;
    color: #0f172a;
    margin: 0;
    line-height: 1.35;
  }

  .degree-badge {
    background: #e0e7ff;
    color: #3730a3;
    font-size: 0.76rem;
    font-weight: 600;
    padding: 0.2rem 0.6rem;
    border-radius: 6px;
    white-space: nowrap;
  }

  .prog-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 0.45rem;
    margin: 0.15rem 0;
  }

  .spec-pill {
    font-size: 0.8rem;
    background: #ffffff;
    border: 1px solid #cbd5e1;
    color: #334155;
    padding: 0.2rem 0.55rem;
    border-radius: 6px;
    font-weight: 500;
  }

  .spec-pill.tuition-pill {
    background: #fef3c7;
    border-color: #fde68a;
    color: #92400e;
    font-weight: 600;
  }

  .prog-description {
    font-size: 0.9rem;
    color: #475569;
    line-height: 1.5;
    margin: 0.2rem 0;
  }

  .prog-detail-item {
    font-size: 0.85rem;
    line-height: 1.45;
    color: #334155;
    background: #ffffff;
    border: 1px solid #f1f5f9;
    padding: 0.55rem 0.75rem;
    border-radius: 8px;
  }

  .prog-detail-item .detail-label {
    font-weight: 700;
    color: #0f172a;
    display: block;
    margin-bottom: 0.2rem;
  }

  .prog-detail-item .detail-text {
    color: #475569;
  }
</style>
