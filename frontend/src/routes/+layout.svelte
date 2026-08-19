<script lang="ts">
	let { children } = $props();
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

{@render children()}

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

		--font-display: 'Fraunces', serif;
		--font-body: 'Inter', sans-serif;
		--font-mono: 'IBM Plex Mono', monospace;

		--header-height: 4.5rem;
	}

	:global(html) {
		scroll-behavior: smooth;
	}
	:global(body) {
		margin: 0;
		font-family: var(--font-body);
		-webkit-font-smoothing: antialiased;
	}
	:global(*) {
		box-sizing: border-box;
	}
	:global(a) {
		color: inherit;
	}
</style>