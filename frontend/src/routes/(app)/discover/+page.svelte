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
  let expandedSchoolId = $state<string | null>(null);
  let favoriteIds = $state<string[]>([]);

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

      // Fetch programs for each school
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

  function toggleExpand(schoolId: string) {
    if (expandedSchoolId === schoolId) {
      expandedSchoolId = null;
    } else {
      expandedSchoolId = schoolId;
      const school = schools.find((s) => s.id === schoolId);
      if (school && !school.programs) {
        fetchProgramsForSchool(schoolId);
      }
    }
  }

  onMount(() => {
    loadFavorites();
    fetchSchools();
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

<div class="discover-page">
  <header class="header">
    <h2>Discover Universities & Higher Institutes</h2>
    <p class="subtitle">
      Browse verified higher institutions, accredited degree programs, tuition fees, and admission requirements in Cameroon.
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
        <button class="btn-clear" onclick={() => (searchQuery = "")}>✕</button>
      {/if}
    </div>

    <div class="degree-chips">
      <span class="chips-label">Filter by Degree:</span>
      {#each DEGREE_FILTERS as filter}
        <button
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
      <p>⚠️ {loadError}</p>
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
    <div class="schools-grid">
      {#each filteredSchools as school (school.id)}
        {@const isFav = favoriteIds.includes(school.id)}
        {@const isExpanded = expandedSchoolId === school.id}
        <div
          class="university-card"
          class:expanded={isExpanded}
          onclick={() => toggleExpand(school.id)}
          role="button"
          tabindex="0"
          onkeydown={(e) => {
            if (e.key === "Enter" || e.key === " ") toggleExpand(school.id);
          }}
        >
          <!-- Card Header / Primary Info -->
          <div class="card-main">
            <div class="info-primary">
              <div class="name-row">
                <h3 class="school-name">{school.name}</h3>
                {#if school.rolling_admission}
                  <span class="badge-rolling">⚡ Rolling Admission</span>
                {/if}
              </div>

              {#if school.location}
                <div class="location-badge">
                  <svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor">
                    <path
                      d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5a2.5 2.5 0 110-5 2.5 2.5 0 010 5z"
                    />
                  </svg>
                  <span>{school.location}</span>
                </div>
              {/if}
            </div>

            <!-- Favorite Icon Button -->
            <button
              class="btn-favorite"
              class:favorited={isFav}
              onclick={(e) => toggleFavorite(school.id, e)}
              title={isFav ? "Remove from favorites" : "Add to favorites"}
              aria-label={isFav ? "Remove from favorites" : "Add to favorites"}
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
                  stroke="#64748b"
                  stroke-width="2"
                >
                  <path
                    d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"
                  />
                </svg>
              {/if}
            </button>
          </div>

          <!-- Description preview -->
          {#if school.description}
            <p class="short-description">{school.description}</p>
          {/if}

          <!-- Quick badges -->
          <div class="meta-row">
            {#if school.application_deadline}
              <span class="meta-pill">📅 Deadline: {school.application_deadline}</span>
            {/if}
            {#if school.programs && school.programs.length > 0}
              <span class="meta-pill programs-count">🎓 {school.programs.length} Programs Available</span>
            {/if}
          </div>

          <!-- Reveal Indicator -->
          <div class="reveal-hint">
            <span>{isExpanded ? "Hide programs & details ▲" : "View degree programs & requirements ▼"}</span>
          </div>

          <!-- Expanded Details Section -->
          {#if isExpanded}
            <!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
            <div class="card-details" role="region" aria-label="Institution details" onclick={(e) => e.stopPropagation()} onkeydown={(e) => e.stopPropagation()}>
              <!-- Contact & Link info -->
              <div class="contact-grid">
                {#if school.website_url}
                  <a href={school.website_url} target="_blank" rel="noreferrer" class="link-pill">
                    🌐 Visit Website ↗
                  </a>
                {/if}
                {#if school.contact_email}
                  <a href="mailto:{school.contact_email}" class="link-pill">
                    ✉️ {school.contact_email}
                  </a>
                {/if}
              </div>

              <!-- Programs Section -->
              <div class="programs-container">
                <h4 class="programs-header">Offered Programs</h4>

                {#if !school.programs}
                  <p class="loading-progs">Loading programs...</p>
                {:else if school.programs.length === 0}
                  <p class="empty-progs">No programs listed yet for this institution.</p>
                {:else}
                  <div class="programs-list">
                    {#each school.programs as prog}
                      <div class="program-item">
                        <div class="prog-top">
                          <h5 class="prog-title">{prog.field_of_study}</h5>
                          {#if prog.degree_type}
                            <span class="degree-badge">{prog.degree_type}</span>
                          {/if}
                        </div>

                        <div class="prog-specs">
                          {#if prog.tuition_fee}
                            <span class="spec-tag tuition-tag">💰 {prog.tuition_fee}</span>
                          {/if}
                          {#if prog.duration}
                            <span class="spec-tag">⏱️ {prog.duration}</span>
                          {/if}
                          {#if prog.language_of_instruction}
                            <span class="spec-tag">🗣️ {prog.language_of_instruction}</span>
                          {/if}
                          {#if prog.delivery_mode}
                            <span class="spec-tag">🏫 {prog.delivery_mode}</span>
                          {/if}
                          {#if prog.class_size}
                            <span class="spec-tag">👥 Capacity: {prog.class_size}</span>
                          {/if}
                        </div>

                        {#if prog.description}
                          <p class="prog-desc">{prog.description}</p>
                        {/if}

                        {#if prog.admission_requirements}
                          <div class="prog-meta-block">
                            <strong>Requirements:</strong> {prog.admission_requirements}
                          </div>
                        {/if}

                        {#if prog.required_documents}
                          <div class="prog-meta-block">
                            <strong>Documents:</strong> {prog.required_documents}
                          </div>
                        {/if}
                      </div>
                    {/each}
                  </div>
                {/if}
              </div>
            </div>
          {/if}
        </div>
      {/each}
    </div>
  {/if}
</div>

<style>
  .discover-page {
    max-width: 1000px;
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
  }

  .search-box input {
    width: 100%;
    padding: 0.85rem 2.8rem 0.85rem 3rem;
    border: 1px solid #cbd5e1;
    border-radius: 12px;
    font-size: 0.95rem;
    background: #fff;
    color: #1e293b;
    outline: none;
    transition: border-color 0.2s;
  }

  .search-box input:focus {
    border-color: #2563eb;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
  }

  .btn-clear {
    position: absolute;
    right: 1rem;
    background: none;
    border: none;
    color: #94a3b8;
    cursor: pointer;
    font-size: 1rem;
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
    color: #fff;
    border-color: #2563eb;
  }

  .loading-state,
  .empty-state,
  .error-state {
    text-align: center;
    padding: 4rem 1rem;
    background: #fff;
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
    color: #fff;
    border: none;
    padding: 0.5rem 1.25rem;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
  }

  .schools-grid {
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
  }

  .university-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    cursor: pointer;
    transition: all 0.2s ease-in-out;
    outline: none;
  }

  .university-card:hover {
    border-color: #cbd5e1;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
    transform: translateY(-2px);
  }

  .university-card.expanded {
    border-color: #93c5fd;
    box-shadow: 0 10px 30px rgba(37, 99, 235, 0.08);
  }

  .card-main {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
  }

  .name-row {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    flex-wrap: wrap;
  }

  .school-name {
    font-size: 1.25rem;
    font-weight: 700;
    color: #0f172a;
    margin: 0;
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

  .location-badge {
    display: flex;
    align-items: center;
    gap: 0.35rem;
    font-size: 0.85rem;
    color: #64748b;
    margin-top: 0.35rem;
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
    transition: transform 0.15s;
  }

  .btn-favorite:hover {
    transform: scale(1.15);
  }

  .short-description {
    color: #475569;
    font-size: 0.92rem;
    line-height: 1.5;
    margin: 0.75rem 0 0.5rem;
  }

  .meta-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
    margin-top: 0.75rem;
  }

  .meta-pill {
    font-size: 0.8rem;
    background: #f8fafc;
    color: #475569;
    border: 1px solid #e2e8f0;
    padding: 0.2rem 0.65rem;
    border-radius: 8px;
    font-weight: 500;
  }

  .meta-pill.programs-count {
    background: #eff6ff;
    color: #1d4ed8;
    border-color: #bfdbfe;
    font-weight: 600;
  }

  .reveal-hint {
    margin-top: 1rem;
    text-align: right;
  }

  .reveal-hint span {
    font-size: 0.8rem;
    color: #2563eb;
    font-weight: 600;
  }

  .card-details {
    margin-top: 1.25rem;
    padding-top: 1.25rem;
    border-top: 1px solid #f1f5f9;
    cursor: default;
  }

  .contact-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
    margin-bottom: 1.25rem;
  }

  .link-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    font-size: 0.85rem;
    color: #2563eb;
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    padding: 0.35rem 0.85rem;
    border-radius: 8px;
    text-decoration: none;
    font-weight: 500;
    transition: background 0.15s;
  }

  .link-pill:hover {
    background: #dbeafe;
  }

  .programs-header {
    font-size: 1rem;
    font-weight: 700;
    color: #0f172a;
    margin: 0 0 0.85rem;
  }

  .programs-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .program-item {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 1rem;
    text-align: left;
  }

  .prog-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 0.5rem;
    flex-wrap: wrap;
  }

  .prog-title {
    font-size: 0.98rem;
    font-weight: 600;
    color: #0f172a;
    margin: 0;
  }

  .degree-badge {
    background: #e0e7ff;
    color: #3730a3;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 0.2rem 0.55rem;
    border-radius: 6px;
  }

  .prog-specs {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin: 0.5rem 0;
  }

  .spec-tag {
    font-size: 0.8rem;
    background: #ffffff;
    border: 1px solid #cbd5e1;
    color: #334155;
    padding: 0.2rem 0.55rem;
    border-radius: 6px;
    font-weight: 500;
  }

  .spec-tag.tuition-tag {
    background: #fef3c7;
    border-color: #fde68a;
    color: #92400e;
    font-weight: 600;
  }

  .prog-desc {
    font-size: 0.88rem;
    color: #475569;
    line-height: 1.45;
    margin: 0.35rem 0 0.5rem;
  }

  .prog-meta-block {
    font-size: 0.82rem;
    color: #475569;
    margin-top: 0.25rem;
  }

  .prog-meta-block strong {
    color: #1e293b;
  }

  .loading-progs,
  .empty-progs {
    font-size: 0.9rem;
    color: #64748b;
    font-style: italic;
  }
</style>