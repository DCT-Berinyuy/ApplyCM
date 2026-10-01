<script lang="ts">
  import { onMount } from "svelte";
  import { API_BASE_URL } from "$lib/config";
  import { apiFetch } from "$lib/api/client";
  import SchoolDetail from "$lib/components/SchoolDetail.svelte";

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
    institution_type?: string | null;
    city?: string | null;
    data_source_url?: string | null;
    last_verified_at?: string | null;
    created_at?: string;
    programs?: Program[];
  }

  // State
  let schools = $state<School[]>([]);
  let loading = $state(true);
  let loadError = $state<string | null>(null);
  let selectedSchoolId = $state<string | null>(null);
  let favoriteIds = $state<string[]>([]);
  let logoErrors = $state<Record<string, boolean>>({});

  // Filter state (server-side query params)
  let searchQuery = $state("");
  let selectedInstitutionType = $state("All"); // All, public, ipes, iup
  let selectedCity = $state("");
  let selectedField = $state("");
  let selectedDegree = $state("All"); // All, Bachelor, Engineering, Master, BTS/HND, Doctorat
  let minTuition = $state<number | string>("");
  let maxTuition = $state<number | string>("");
  let selectedLanguage = $state("All"); // All, English, French, Bilingual
  let selectedDeliveryMode = $state("All"); // All, On-Campus, Hybrid

  // UI state
  let showFiltersPanel = $state(false);
  let searchDebounceTimeout: any = null;

  const selectedSchool = $derived(
    schools.find((s) => s.id === selectedSchoolId) || null
  );

  // Filter Options & Presets
  const INSTITUTION_TYPES = ["All", "Public", "IPES", "IUP"];
  const DEGREE_TYPES = [
    { label: "All Degrees", value: "All" },
    { label: "Bachelor / Licence", value: "Bachelor" },
    { label: "Engineering (Ingénieur)", value: "Engineering" },
    { label: "Master / MBA", value: "Master" },
    { label: "BTS / HND", value: "BTS" },
    { label: "Doctorate (Medicine/PhD)", value: "Doctorat" },
  ];
  const CITY_PRESETS = ["All", "Yaoundé", "Douala", "Buea", "Centre"];
  const LANGUAGE_OPTIONS = [
    { label: "All Languages", value: "All" },
    { label: "English", value: "English" },
    { label: "French", value: "French" },
    { label: "Bilingual (FR/EN)", value: "Bilingual" },
  ];
  const DELIVERY_OPTIONS = [
    { label: "All Modes", value: "All" },
    { label: "On-Campus", value: "On-Campus" },
    { label: "Hybrid", value: "Hybrid" },
  ];
  const TUITION_PRESETS = [
    { label: "All", max: "" },
    { label: "≤ 100k FCFA (State)", max: 100000 },
    { label: "≤ 500k FCFA", max: 500000 },
    { label: "≤ 800k FCFA", max: 800000 },
    { label: "≤ 1.2M FCFA", max: 1200000 },
  ];
  const FIELD_SUGGESTIONS = [
    "Computer Science / Software Engineering",
    "Medicine & Healthcare",
    "Civil Engineering",
    "Law & Political Science",
    "Economics & Management",
    "Telecommunications",
    "Journalism & Media",
  ];

  // Active filter count computation
  const activeFiltersCount = $derived(
    (selectedInstitutionType !== "All" ? 1 : 0) +
    (selectedCity.trim() !== "" && selectedCity !== "All" ? 1 : 0) +
    (selectedField.trim() !== "" ? 1 : 0) +
    (selectedDegree !== "All" ? 1 : 0) +
    (minTuition !== "" && Number(minTuition) > 0 ? 1 : 0) +
    (maxTuition !== "" && Number(maxTuition) > 0 ? 1 : 0) +
    (selectedLanguage !== "All" ? 1 : 0) +
    (selectedDeliveryMode !== "All" ? 1 : 0)
  );

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

  // Server-side fetching with all optional filter parameters
  async function fetchSchools() {
    loading = true;
    loadError = null;
    try {
      const params = new URLSearchParams();

      if (searchQuery.trim()) {
        params.set("search", searchQuery.trim());
      }
      if (selectedInstitutionType !== "All") {
        params.set("institution_type", selectedInstitutionType.toLowerCase());
      }
      if (selectedCity.trim() && selectedCity !== "All") {
        params.set("city", selectedCity.trim());
      }
      if (selectedField.trim()) {
        params.set("field_of_study", selectedField.trim());
      }
      if (selectedDegree !== "All") {
        params.set("degree_type", selectedDegree);
      }
      if (minTuition !== "" && !isNaN(Number(minTuition))) {
        params.set("min_tuition", String(minTuition));
      }
      if (maxTuition !== "" && !isNaN(Number(maxTuition))) {
        params.set("max_tuition", String(maxTuition));
      }
      if (selectedLanguage !== "All") {
        params.set("language_of_instruction", selectedLanguage);
      }
      if (selectedDeliveryMode !== "All") {
        params.set("delivery_mode", selectedDeliveryMode);
      }

      const queryString = params.toString();
      const url = `${API_BASE_URL}/api/schools${queryString ? `?${queryString}` : ""}`;

      const res = await fetch(url);
      if (!res.ok) {
        throw new Error(`Failed to load schools: HTTP ${res.status}`);
      }
      const data: School[] = await res.json();
      schools = data;
    } catch (err: any) {
      console.error("Failed to fetch schools from backend API:", err);
      loadError = err.message || "Failed to load universities from server.";
    } finally {
      loading = false;
    }
  }

  function handleSearchInput() {
    if (searchDebounceTimeout) clearTimeout(searchDebounceTimeout);
    searchDebounceTimeout = setTimeout(() => {
      fetchSchools();
    }, 350);
  }

  function applyFilters() {
    fetchSchools();
  }

  function resetAllFilters() {
    searchQuery = "";
    selectedInstitutionType = "All";
    selectedCity = "";
    selectedField = "";
    selectedDegree = "All";
    minTuition = "";
    maxTuition = "";
    selectedLanguage = "All";
    selectedDeliveryMode = "All";
    fetchSchools();
  }

  async function loadFavorites() {
    try {
      const favSchools = await apiFetch<Array<{ id: string }>>("/api/favorites");
      favoriteIds = favSchools.map((s) => s.id);
    } catch (err) {
      console.warn("Could not load favorites from API:", err);
      favoriteIds = [];
    }
  }

  async function toggleFavorite(schoolId: string, event: MouseEvent) {
    event.stopPropagation();
    const isCurrentlyFav = favoriteIds.includes(schoolId);

    // Optimistic UI update
    if (isCurrentlyFav) {
      favoriteIds = favoriteIds.filter((id) => id !== schoolId);
    } else {
      favoriteIds = [...favoriteIds, schoolId];
    }

    try {
      if (isCurrentlyFav) {
        await apiFetch(`/api/favorites/${schoolId}`, { method: "DELETE" });
      } else {
        await apiFetch("/api/favorites", {
          method: "POST",
          body: JSON.stringify({ school_id: schoolId }),
        });
      }
    } catch (err) {
      console.error("Failed to update favorite on server:", err);
      if (isCurrentlyFav) {
        favoriteIds = [...favoriteIds, schoolId];
      } else {
        favoriteIds = favoriteIds.filter((id) => id !== schoolId);
      }
    }
  }

  function openSchoolDetail(schoolId: string) {
    selectedSchoolId = schoolId;
    if (typeof window !== "undefined") {
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  }

  function closeSchoolDetail() {
    selectedSchoolId = null;
    if (typeof window !== "undefined") {
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  }

  onMount(() => {
    loadFavorites();
    fetchSchools();
  });
</script>

<svelte:window
  onkeydown={(e) => {
    if (e.key === "Escape") {
      if (selectedSchoolId) {
        closeSchoolDetail();
      } else if (showFiltersPanel) {
        showFiltersPanel = false;
      }
    }
  }}
/>

<div class="discover-page">
  {#if selectedSchool}
    <!-- ======================================================== -->
    <!-- 2. DETAIL VIEW (Replaces full list, same page, client swap) -->
    <!-- ======================================================== -->
    <SchoolDetail
      school={selectedSchool}
      showBackButton={true}
      onclose={closeSchoolDetail}
      showFavoriteHeart={true}
      isFavorited={favoriteIds.includes(selectedSchool.id)}
      ontogglefavorite={toggleFavorite}
    />
  {:else}
    <!-- ======================================================== -->
    <!-- 1. LIST VIEW (Default State: Common App style search)    -->
    <!-- ======================================================== -->
    <header class="header">
      <div class="header-content">
        <h2>Discover Universities & Higher Institutes</h2>
        <p class="subtitle">
          Browse verified higher education institutions across Cameroon. Filter by institution type, degree level, tuition fee range, location, and study mode.
        </p>
      </div>
    </header>

    <!-- Filter Control Bar -->
    <div class="search-and-filter-bar">
      <!-- Search Input -->
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
          placeholder="Search by institution name, location, or study program..."
          bind:value={searchQuery}
          oninput={handleSearchInput}
        />
        {#if searchQuery}
          <button
            class="btn-clear"
            onclick={() => {
              searchQuery = "";
              fetchSchools();
            }}
            aria-label="Clear search"
          >
            ✕
          </button>
        {/if}
      </div>

      <!-- Filters Toggle Button -->
      <button
        type="button"
        class="btn-filter-toggle"
        class:panel-open={showFiltersPanel}
        class:has-active={activeFiltersCount > 0}
        onclick={() => (showFiltersPanel = !showFiltersPanel)}
        aria-expanded={showFiltersPanel}
      >
        <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2">
          <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3" />
        </svg>
        <span>Filters</span>
        {#if activeFiltersCount > 0}
          <span class="filter-badge">{activeFiltersCount}</span>
        {/if}
        <svg
          class="chevron-icon"
          class:rotated={showFiltersPanel}
          viewBox="0 0 24 24"
          width="16"
          height="16"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
        >
          <polyline points="6 9 12 15 18 9" />
        </svg>
      </button>

      {#if activeFiltersCount > 0 || searchQuery}
        <button
          type="button"
          class="btn-reset-text"
          onclick={resetAllFilters}
          title="Reset all search and filters"
        >
          Reset All
        </button>
      {/if}
    </div>

    <!-- Quick Degree Type Pills -->
    <div class="degree-chips-row">
      <span class="chips-label">Degree Level:</span>
      {#each DEGREE_TYPES as deg}
        <button
          type="button"
          class="chip"
          class:active={selectedDegree === deg.value}
          onclick={() => {
            selectedDegree = deg.value;
            fetchSchools();
          }}
        >
          {deg.label}
        </button>
      {/each}
    </div>

    <!-- ======================================================== -->
    <!-- EXPANDABLE ADVANCED FILTERS PANEL                        -->
    <!-- ======================================================== -->
    {#if showFiltersPanel}
      <div class="filters-panel">
        <div class="filters-panel-header">
          <div class="panel-title-wrap">
            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#2563eb" stroke-width="2">
              <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3" />
            </svg>
            <h3>Advanced Search Filters</h3>
          </div>
          <button
            type="button"
            class="btn-panel-close"
            onclick={() => (showFiltersPanel = false)}
            aria-label="Close filters panel"
          >
            ✕
          </button>
        </div>

        <div class="filters-grid">
          <!-- 1. Institution Type -->
          <div class="filter-card">
            <label class="filter-label" for="filter-type">Institution Type</label>
            <div class="segmented-control">
              {#each INSTITUTION_TYPES as type}
                <button
                  type="button"
                  class="segment-btn"
                  class:active={selectedInstitutionType.toLowerCase() === type.toLowerCase()}
                  onclick={() => {
                    selectedInstitutionType = type;
                    applyFilters();
                  }}
                >
                  {type}
                </button>
              {/each}
            </div>
            <span class="field-hint">Public universities, IPES (Privé), or IUP.</span>
          </div>

          <!-- 2. City / Region -->
          <div class="filter-card">
            <label class="filter-label" for="city-input">City / Region</label>
            <div class="city-input-wrap">
              <input
                id="city-input"
                type="text"
                placeholder="e.g. Yaoundé, Douala, Buea..."
                bind:value={selectedCity}
                onchange={applyFilters}
              />
            </div>
            <div class="quick-preset-chips">
              {#each CITY_PRESETS as preset}
                <button
                  type="button"
                  class="preset-chip"
                  class:selected={selectedCity.toLowerCase() === preset.toLowerCase() || (preset === 'All' && selectedCity === '')}
                  onclick={() => {
                    selectedCity = preset === "All" ? "" : preset;
                    applyFilters();
                  }}
                >
                  {preset}
                </button>
              {/each}
            </div>
          </div>

          <!-- 3. Field of Study -->
          <div class="filter-card">
            <label class="filter-label" for="field-input">Field of Study</label>
            <div class="field-input-wrap">
              <input
                id="field-input"
                type="text"
                placeholder="e.g. Software, Medicine, Law, Telecom..."
                bind:value={selectedField}
                onchange={applyFilters}
              />
            </div>
            <div class="field-suggestions">
              {#each FIELD_SUGGESTIONS as sug}
                <button
                  type="button"
                  class="sug-pill"
                  onclick={() => {
                    selectedField = sug.split(" ")[0];
                    applyFilters();
                  }}
                >
                  {sug}
                </button>
              {/each}
            </div>
          </div>

          <!-- 4. Tuition Fee Range -->
          <div class="filter-card">
            <label class="filter-label" for="tuition-max">Tuition Fee Range (FCFA)</label>
            <div class="tuition-inputs-row">
              <div class="input-with-currency">
                <span class="currency-tag">Min</span>
                <input
                  id="tuition-min"
                  type="number"
                  placeholder="0"
                  bind:value={minTuition}
                  onchange={applyFilters}
                />
              </div>
              <span class="range-separator">—</span>
              <div class="input-with-currency">
                <span class="currency-tag">Max</span>
                <input
                  id="tuition-max"
                  type="number"
                  placeholder="2,000,000"
                  bind:value={maxTuition}
                  onchange={applyFilters}
                />
              </div>
            </div>
            <div class="quick-preset-chips">
              {#each TUITION_PRESETS as preset}
                <button
                  type="button"
                  class="preset-chip"
                  class:selected={maxTuition === preset.max}
                  onclick={() => {
                    maxTuition = preset.max;
                    applyFilters();
                  }}
                >
                  {preset.label}
                </button>
              {/each}
            </div>
          </div>

          <!-- 5. Language of Instruction -->
          <div class="filter-card">
            <label class="filter-label" for="lang-select">Language of Instruction</label>
            <select
              id="lang-select"
              class="filter-select"
              bind:value={selectedLanguage}
              onchange={applyFilters}
            >
              {#each LANGUAGE_OPTIONS as opt}
                <option value={opt.value}>{opt.label}</option>
              {/each}
            </select>
          </div>

          <!-- 6. Delivery Mode -->
          <div class="filter-card">
            <label class="filter-label" for="mode-select">Delivery Mode</label>
            <select
              id="mode-select"
              class="filter-select"
              bind:value={selectedDeliveryMode}
              onchange={applyFilters}
            >
              {#each DELIVERY_OPTIONS as opt}
                <option value={opt.value}>{opt.label}</option>
              {/each}
            </select>
          </div>
        </div>

        <!-- Filter Panel Footer -->
        <div class="filters-panel-footer">
          <div class="active-count-label">
            {#if activeFiltersCount > 0}
              <span><strong>{activeFiltersCount}</strong> active filter{activeFiltersCount > 1 ? "s" : ""} applied</span>
            {:else}
              <span>No filters applied. Showing all institutions.</span>
            {/if}
          </div>
          <div class="panel-actions">
            {#if activeFiltersCount > 0}
              <button type="button" class="btn-clear-filters" onclick={resetAllFilters}>
                Clear All
              </button>
            {/if}
            <button type="button" class="btn-apply-filters" onclick={applyFilters}>
              Apply Filters
            </button>
          </div>
        </div>
      </div>
    {/if}

    <!-- Active Filters Summary Tags (when panel is collapsed) -->
    {#if activeFiltersCount > 0 && !showFiltersPanel}
      <div class="active-pills-bar">
        <span class="active-label">Active:</span>
        {#if selectedInstitutionType !== "All"}
          <button
            type="button"
            class="active-pill"
            onclick={() => {
              selectedInstitutionType = "All";
              fetchSchools();
            }}
          >
            Type: {selectedInstitutionType} ✕
          </button>
        {/if}
        {#if selectedCity.trim()}
          <button
            type="button"
            class="active-pill"
            onclick={() => {
              selectedCity = "";
              fetchSchools();
            }}
          >
            City: {selectedCity} ✕
          </button>
        {/if}
        {#if selectedField.trim()}
          <button
            type="button"
            class="active-pill"
            onclick={() => {
              selectedField = "";
              fetchSchools();
            }}
          >
            Field: {selectedField} ✕
          </button>
        {/if}
        {#if selectedDegree !== "All"}
          <button
            type="button"
            class="active-pill"
            onclick={() => {
              selectedDegree = "All";
              fetchSchools();
            }}
          >
            Degree: {selectedDegree} ✕
          </button>
        {/if}
        {#if maxTuition !== "" && Number(maxTuition) > 0}
          <button
            type="button"
            class="active-pill"
            onclick={() => {
              maxTuition = "";
              fetchSchools();
            }}
          >
            Tuition: ≤ {Number(maxTuition).toLocaleString()} FCFA ✕
          </button>
        {/if}
        {#if selectedLanguage !== "All"}
          <button
            type="button"
            class="active-pill"
            onclick={() => {
              selectedLanguage = "All";
              fetchSchools();
            }}
          >
            Lang: {selectedLanguage} ✕
          </button>
        {/if}
        {#if selectedDeliveryMode !== "All"}
          <button
            type="button"
            class="active-pill"
            onclick={() => {
              selectedDeliveryMode = "All";
              fetchSchools();
            }}
          >
            Mode: {selectedDeliveryMode} ✕
          </button>
        {/if}
        <button type="button" class="btn-clear-all-link" onclick={resetAllFilters}>
          Clear all
        </button>
      </div>
    {/if}

    <!-- Result Count Header -->
    <div class="results-meta-bar">
      <span class="results-count">
        {#if loading}
          Searching institutions...
        {:else}
          Showing <strong>{schools.length}</strong> {schools.length === 1 ? "institution" : "institutions"}
        {/if}
      </span>
    </div>

    <!-- Content States -->
    {#if loading}
      <div class="loading-state">
        <div class="spinner"></div>
        <p>Loading universities matching your filters from server...</p>
      </div>
    {:else if loadError}
      <div class="error-state">
        <p class="error-text">⚠️ {loadError}</p>
        <button class="btn-reset" onclick={fetchSchools}>Retry</button>
      </div>
    {:else if schools.length === 0}
      <div class="empty-state">
        <div class="empty-icon">🔍</div>
        <h3>No universities found</h3>
        <p>We couldn't find any institutions matching your search and filter criteria.</p>
        <button class="btn-reset" onclick={resetAllFilters}>Reset All Filters</button>
      </div>
    {:else}
      <!-- Schools List -->
      <div class="schools-list">
        {#each schools as school (school.id)}
          {@const isFav = favoriteIds.includes(school.id)}
          <div class="school-row">
            <!-- Left section: Boxed container holding logo / fallback -->
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

            <!-- Middle section: School Info -->
            <div class="school-info-col">
              <div class="school-header-line">
                <button
                  type="button"
                  class="school-name-btn"
                  onclick={() => openSchoolDetail(school.id)}
                >
                  {school.name}
                </button>
                {#if school.institution_type}
                  <span class="type-badge" class:public={school.institution_type.toLowerCase() === 'public'}>
                    {school.institution_type.toUpperCase()}
                  </span>
                {/if}
              </div>

              {#if school.location}
                <div class="school-location-line">
                  <svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor">
                    <path
                      d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5a2.5 2.5 0 110-5 2.5 2.5 0 010 5z"
                    />
                  </svg>
                  <span>{school.location}</span>
                </div>
              {/if}

              {#if school.programs && school.programs.length > 0}
                <div class="programs-preview-line">
                  <span class="programs-count-tag">{school.programs.length} {school.programs.length === 1 ? 'Program' : 'Programs'}:</span>
                  <span class="programs-tags-list">
                    {school.programs.slice(0, 3).map(p => p.field_of_study).join(" • ")}
                    {#if school.programs.length > 3}
                      <span class="more-progs">+{school.programs.length - 3} more</span>
                    {/if}
                  </span>
                </div>
              {/if}
            </div>

            <!-- Far-right: Favorite Heart Button -->
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
  {/if}
</div>

<style>
  .discover-page {
    max-width: 1040px;
    margin: 0 auto;
    padding: 2rem 1.5rem 4rem;
    color: #1a2b4a;
    text-align: left;
  }

  /* List Header */
  .header {
    margin-bottom: 1.75rem;
  }

  .header h2 {
    font-size: 2.1rem;
    font-weight: 750;
    margin: 0 0 0.5rem;
    color: #0f172a;
    letter-spacing: -0.025em;
  }

  .subtitle {
    color: #64748b;
    font-size: 1.02rem;
    margin: 0;
    line-height: 1.55;
    max-width: 820px;
  }

  /* Search & Filter Bar */
  .search-and-filter-bar {
    display: flex;
    align-items: center;
    gap: 0.85rem;
    margin-bottom: 1rem;
  }

  .search-box {
    position: relative;
    display: flex;
    align-items: center;
    flex: 1;
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

  /* Filter Toggle Button */
  .btn-filter-toggle {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.85rem 1.25rem;
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 12px;
    font-size: 0.95rem;
    font-weight: 600;
    color: #334155;
    cursor: pointer;
    transition: all 0.2s ease;
    white-space: nowrap;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
  }

  .btn-filter-toggle:hover {
    background: #f8fafc;
    border-color: #94a3b8;
    color: #0f172a;
  }

  .btn-filter-toggle.panel-open {
    background: #eff6ff;
    border-color: #2563eb;
    color: #1d4ed8;
  }

  .btn-filter-toggle.has-active {
    border-color: #2563eb;
    background: #f0f7ff;
    color: #1d4ed8;
  }

  .filter-badge {
    background: #2563eb;
    color: #ffffff;
    font-size: 0.75rem;
    font-weight: 700;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    line-height: 1;
  }

  .chevron-icon {
    transition: transform 0.2s ease;
  }

  .chevron-icon.rotated {
    transform: rotate(180deg);
  }

  .btn-reset-text {
    background: none;
    border: none;
    color: #64748b;
    font-size: 0.88rem;
    font-weight: 600;
    cursor: pointer;
    padding: 0.5rem;
    text-decoration: underline;
    transition: color 0.15s;
    white-space: nowrap;
  }

  .btn-reset-text:hover {
    color: #ef4444;
  }

  /* Degree Chips Row */
  .degree-chips-row {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 1.25rem;
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

  /* ======================================================== */
  /* Advanced Filters Panel                                   */
  /* ======================================================== */
  .filters-panel {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.75rem;
    box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.06);
    animation: slideDown 0.2s ease-out;
  }

  @keyframes slideDown {
    from {
      opacity: 0;
      transform: translateY(-8px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  .filters-panel-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.25rem;
    padding-bottom: 0.85rem;
    border-bottom: 1px solid #f1f5f9;
  }

  .panel-title-wrap {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .panel-title-wrap h3 {
    margin: 0;
    font-size: 1.15rem;
    font-weight: 700;
    color: #0f172a;
  }

  .btn-panel-close {
    background: none;
    border: none;
    color: #94a3b8;
    cursor: pointer;
    font-size: 1.2rem;
    padding: 0.25rem;
    line-height: 1;
    border-radius: 6px;
    transition: all 0.15s;
  }

  .btn-panel-close:hover {
    background: #f1f5f9;
    color: #0f172a;
  }

  .filters-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.25rem;
    margin-bottom: 1.5rem;
  }

  .filter-card {
    display: flex;
    flex-direction: column;
    gap: 0.45rem;
  }

  .filter-label {
    font-size: 0.85rem;
    font-weight: 650;
    color: #334155;
    letter-spacing: -0.01em;
  }

  .field-hint {
    font-size: 0.78rem;
    color: #94a3b8;
  }

  /* Segmented Control */
  .segmented-control {
    display: flex;
    background: #f1f5f9;
    padding: 0.25rem;
    border-radius: 10px;
    border: 1px solid #e2e8f0;
  }

  .segment-btn {
    flex: 1;
    background: none;
    border: none;
    padding: 0.45rem 0.5rem;
    font-size: 0.85rem;
    font-weight: 600;
    color: #64748b;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.15s ease;
  }

  .segment-btn.active {
    background: #ffffff;
    color: #2563eb;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
  }

  /* Inputs & Selects */
  .city-input-wrap input,
  .field-input-wrap input,
  .filter-select {
    width: 100%;
    padding: 0.65rem 0.85rem;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    font-size: 0.9rem;
    color: #1e293b;
    background: #ffffff;
    outline: none;
    transition: border-color 0.15s;
  }

  .city-input-wrap input:focus,
  .field-input-wrap input:focus,
  .filter-select:focus {
    border-color: #2563eb;
  }

  .quick-preset-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 0.35rem;
    margin-top: 0.3rem;
  }

  .preset-chip {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    color: #64748b;
    font-size: 0.78rem;
    padding: 0.2rem 0.55rem;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.15s;
  }

  .preset-chip:hover {
    background: #f1f5f9;
    color: #0f172a;
  }

  .preset-chip.selected {
    background: #eff6ff;
    border-color: #93c5fd;
    color: #1d4ed8;
    font-weight: 600;
  }

  /* Field Suggestions */
  .field-suggestions {
    display: flex;
    flex-wrap: wrap;
    gap: 0.3rem;
    margin-top: 0.3rem;
  }

  .sug-pill {
    background: none;
    border: 1px dashed #cbd5e1;
    color: #64748b;
    font-size: 0.75rem;
    padding: 0.2rem 0.5rem;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.15s;
  }

  .sug-pill:hover {
    border-color: #2563eb;
    color: #2563eb;
    background: #f0f7ff;
  }

  /* Tuition Range */
  .tuition-inputs-row {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .range-separator {
    color: #94a3b8;
    font-weight: 600;
  }

  .input-with-currency {
    position: relative;
    flex: 1;
    display: flex;
    align-items: center;
  }

  .currency-tag {
    position: absolute;
    left: 0.65rem;
    font-size: 0.75rem;
    color: #94a3b8;
    font-weight: 600;
    pointer-events: none;
  }

  .input-with-currency input {
    width: 100%;
    padding: 0.65rem 0.65rem 0.65rem 2.5rem;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    font-size: 0.9rem;
    color: #1e293b;
    outline: none;
  }

  .input-with-currency input:focus {
    border-color: #2563eb;
  }

  /* Panel Footer */
  .filters-panel-footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-top: 1rem;
    border-top: 1px solid #f1f5f9;
    flex-wrap: wrap;
    gap: 0.75rem;
  }

  .active-count-label {
    font-size: 0.88rem;
    color: #64748b;
  }

  .panel-actions {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }

  .btn-clear-filters {
    background: none;
    border: 1px solid #cbd5e1;
    color: #475569;
    padding: 0.55rem 1rem;
    border-radius: 8px;
    font-size: 0.88rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.15s;
  }

  .btn-clear-filters:hover {
    background: #f8fafc;
    border-color: #94a3b8;
    color: #0f172a;
  }

  .btn-apply-filters {
    background: #2563eb;
    border: none;
    color: #ffffff;
    padding: 0.55rem 1.25rem;
    border-radius: 8px;
    font-size: 0.88rem;
    font-weight: 600;
    cursor: pointer;
    box-shadow: 0 1px 2px rgba(37, 99, 235, 0.2);
    transition: background 0.15s;
  }

  .btn-apply-filters:hover {
    background: #1d4ed8;
  }

  /* Active Pills Bar */
  .active-pills-bar {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.45rem;
    margin-bottom: 1rem;
    padding: 0.5rem 0.85rem;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
  }

  .active-label {
    font-size: 0.82rem;
    font-weight: 650;
    color: #64748b;
    margin-right: 0.25rem;
  }

  .active-pill {
    background: #ffffff;
    border: 1px solid #cbd5e1;
    color: #1e293b;
    font-size: 0.8rem;
    font-weight: 550;
    padding: 0.25rem 0.65rem;
    border-radius: 9999px;
    cursor: pointer;
    transition: all 0.15s;
  }

  .active-pill:hover {
    border-color: #ef4444;
    color: #ef4444;
    background: #fef2f2;
  }

  .btn-clear-all-link {
    background: none;
    border: none;
    color: #ef4444;
    font-size: 0.8rem;
    font-weight: 600;
    cursor: pointer;
    text-decoration: underline;
    margin-left: auto;
  }

  /* Results Meta Bar */
  .results-meta-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1rem;
  }

  .results-count {
    font-size: 0.92rem;
    color: #64748b;
  }

  /* ======================================================== */
  /* Common App Style School Rows                             */
  /* ======================================================== */
  .schools-list {
    display: flex;
    flex-direction: column;
    gap: 0.85rem;
  }

  .school-row {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 1.1rem 1.25rem;
    display: flex;
    align-items: center;
    gap: 1.25rem;
    transition: border-color 0.15s, box-shadow 0.15s, background-color 0.15s;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
  }

  .school-row:hover {
    border-color: #cbd5e1;
    background-color: #fafbfc;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  }

  /* Left Section: Logo */
  .logo-box {
    width: 62px;
    height: 62px;
    min-width: 62px;
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
    letter-spacing: 0.03em;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  /* Middle Section */
  .school-info-col {
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
    flex: 1;
    min-width: 0;
  }

  .school-header-line {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    flex-wrap: wrap;
  }

  .school-name-btn {
    background: none;
    border: none;
    padding: 0;
    margin: 0;
    font-size: 1.15rem;
    font-weight: 700;
    color: #0f172a;
    text-align: left;
    cursor: pointer;
    line-height: 1.35;
    transition: color 0.15s;
  }

  .school-name-btn:hover {
    color: #2563eb;
    text-decoration: underline;
    text-underline-offset: 3px;
  }

  .type-badge {
    font-size: 0.68rem;
    font-weight: 700;
    padding: 0.15rem 0.5rem;
    border-radius: 4px;
    background: #f1f5f9;
    color: #475569;
    border: 1px solid #e2e8f0;
    letter-spacing: 0.04em;
  }

  .type-badge.public {
    background: #ecfdf5;
    color: #047857;
    border-color: #a7f3d0;
  }

  .school-location-line {
    display: flex;
    align-items: center;
    gap: 0.35rem;
    font-size: 0.88rem;
    color: #64748b;
  }

  .programs-preview-line {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.82rem;
    color: #475569;
    flex-wrap: wrap;
    margin-top: 0.1rem;
  }

  .programs-count-tag {
    font-weight: 650;
    color: #2563eb;
  }

  .programs-tags-list {
    color: #64748b;
  }

  .more-progs {
    color: #94a3b8;
    font-weight: 500;
  }

  /* Far-right Favorite Heart Button */
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
    margin-left: auto;
  }

  .btn-favorite:hover {
    transform: scale(1.15);
    background-color: #fee2e2;
  }

  /* List View States (Loading, Error, Empty) */
  .loading-state,
  .empty-state,
  .error-state {
    text-align: center;
    padding: 4rem 1.5rem;
    background: #ffffff;
    border-radius: 16px;
    border: 1px dashed #cbd5e1;
  }

  .empty-icon {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
  }

  .empty-state h3 {
    margin: 0.5rem 0;
    font-size: 1.25rem;
    font-weight: 700;
    color: #0f172a;
  }

  .empty-state p {
    color: #64748b;
    font-size: 0.95rem;
    max-width: 480px;
    margin: 0 auto 1.5rem;
    line-height: 1.5;
  }

  .spinner {
    width: 38px;
    height: 38px;
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
    background: #2563eb;
    color: #ffffff;
    border: none;
    padding: 0.6rem 1.4rem;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.15s;
  }

  .btn-reset:hover {
    background: #1d4ed8;
  }

  /* Responsive layout adjustments */
  @media (max-width: 768px) {
    .filters-grid {
      grid-template-columns: 1fr;
    }

    .school-row {
      gap: 0.85rem;
      padding: 0.95rem 1rem;
    }

    .logo-box {
      width: 50px;
      height: 50px;
      min-width: 50px;
    }

    .school-name-btn {
      font-size: 1.02rem;
    }
  }
</style>
