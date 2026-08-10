<script lang="ts">
	let { children } = $props();
	let searchQuery = $state("");
	let scrolled = $state(false);

	function handleSearch(event: Event) {
		event.preventDefault();
		if (searchQuery.trim() === "") return;
		console.log("Searching for:", searchQuery);
	}

	function handleScroll() {
		scrolled = window.scrollY > 8;
	}
</script>

<svelte:head>
	<link rel="icon" href="/favicon.png" />
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
	<link
		href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@500&display=swap"
		rel="stylesheet"
	/>
</svelte:head>

<svelte:window onscroll={handleScroll} />

<div class="app-shell">
	<header class="site-header" class:scrolled>
		<a href="/" class="logo">Apply<span>CM</span></a>

		<form class="search-form" onsubmit={handleSearch}>
			<svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true">
				<circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="2" />
				<path d="M20 20l-3.5-3.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
			</svg>
			<input type="text" placeholder="Search programs, universities..." bind:value={searchQuery} />
		</form>

		<nav class="site-nav">
			<a href="/#how-it-works">How it works</a>
			<a href="/login" class="nav-login">Log in</a>
			<a href="/signup" class="nav-cta">Get started</a>
		</nav>
	</header>

	<main>
		{@render children()}
	</main>
</div>

<style>
	:global(:root) {
		--color-paper: #faf6ee;
		--color-ink: #201a14;
		--color-ink-soft: #7c715b;
		--color-laterite: #163880;
		--color-laterite-dark: #3342a1;
		--color-ndole: #1f4d3a;
		--color-ndole-light: #2b6a4d;
		--color-gold: #e0a458;
		--color-line: #e4dcc9;

		--font-display: "Fraunces", serif;
		--font-body: "Inter", sans-serif;
		--font-mono: "IBM Plex Mono", monospace;

		--header-height: 4.5rem;
	}

	:global(html) {
		scroll-behavior: smooth;
	}

	:global(body) {
		margin: 0;
		background: var(--color-paper);
		color: var(--color-ink);
		font-family: var(--font-body);
		-webkit-font-smoothing: antialiased;
	}

	:global(*) {
		box-sizing: border-box;
	}

	:global(a) {
		color: inherit;
	}

	.app-shell {
		min-height: 100vh;
	}

	.site-header {
		position: sticky;
		top: 0;
		z-index: 50;
		display: flex;
		align-items: center;
		gap: 1.5rem;
		height: var(--header-height);
		padding: 0 2rem;
		background: var(--color-paper);
		border-bottom: 1px solid var(--color-line);
		transition: box-shadow 0.3s ease;
	}

	.site-header.scrolled {
		box-shadow: 0 8px 20px -14px rgba(32, 26, 20, 0.35);
	}

	.logo {
		font-family: var(--font-display);
		font-weight: 600;
		font-size: 1.35rem;
		text-decoration: none;
		color: var(--color-ink);
		letter-spacing: -0.01em;
		flex-shrink: 0;
	}
	.logo span {
		color: var(--color-laterite);
	}

	.search-form {
		flex: 1;
		max-width: 420px;
		display: flex;
		align-items: center;
		gap: 0.5rem;
		background: #fff;
		border: 1px solid var(--color-line);
		border-radius: 999px;
		padding: 0.5rem 1rem;
		transition: border-color 0.2s ease, box-shadow 0.2s ease;
	}
	.search-form:focus-within {
		border-color: var(--color-laterite);
		box-shadow: 0 0 0 3px rgba(180, 71, 43, 0.12);
	}
	.search-icon {
		color: var(--color-ink-soft);
		flex-shrink: 0;
	}
	.search-form input {
		flex: 1;
		border: none;
		outline: none;
		background: transparent;
		font-family: var(--font-body);
		font-size: 0.9rem;
		color: var(--color-ink);
	}
	.search-form input::placeholder {
		color: #a89d87;
	}

	.site-nav {
		display: flex;
		align-items: center;
		gap: 1.5rem;
		margin-left: auto;
		flex-shrink: 0;
	}
	.site-nav a {
		text-decoration: none;
		font-size: 0.9rem;
		font-weight: 500;
	}
	.site-nav a:not(.nav-cta):not(.nav-login) {
		color: var(--color-ink-soft);
		position: relative;
	}
	.site-nav a:not(.nav-cta):not(.nav-login)::after {
		content: "";
		position: absolute;
		left: 0;
		bottom: -4px;
		width: 0;
		height: 2px;
		background: var(--color-laterite);
		transition: width 0.25s ease;
	}
	.site-nav a:not(.nav-cta):not(.nav-login):hover::after {
		width: 100%;
	}
	.site-nav a:not(.nav-cta):not(.nav-login):hover {
		color: var(--color-ink);
	}

	.nav-login {
		color: var(--color-ink);
	}
	.nav-cta {
		background: var(--color-laterite);
		color: #fff;
		padding: 0.55rem 1.1rem;
		border-radius: 999px;
		transition: background 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
	}
	.nav-cta:hover {
		background: var(--color-laterite-dark);
		transform: translateY(-2px);
		box-shadow: 0 10px 20px -10px rgba(180, 71, 43, 0.6);
	}

	@media (max-width: 720px) {
		.search-form {
			display: none;
		}
		.site-nav a:not(.nav-cta):not(.nav-login) {
			display: none;
		}
	}
</style>