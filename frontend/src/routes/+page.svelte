<script lang="ts">
	const steps = [
		{
			number: "01",
			title: "Build your profile",
			body: "Enter your GCE, Probatoire, or Baccalauréat results once. It's reused on every application you send."
		},
		{
			number: "02",
			title: "Explore your options",
			body: "Compare programs, tuition, and admission requirements across public universities and private institutes."
		},
		{
			number: "03",
			title: "Submit applications",
			body: "Apply to as many schools as you want without retyping the same information into a new form each time."
		},
		{
			number: "04",
			title: "Track every decision",
			body: "Follow each application from submitted to under review to admitted — all from one dashboard."
		}
	];
</script>

<section class="hero">
	<p class="eyebrow">Now welcoming Cameroon's founding cohort</p>
	<h1>One profile.<br />Every gate in Cameroon opens with it.</h1>
	<p class="hero-sub">
		Build your academic profile once and apply to public universities, private institutes, and
		professional schools across the country — no more re-typing the same form for every school.
	</p>
	<div class="hero-actions">
		<a href="/signup" class="btn-primary">Create your profile</a>
		<a href="/login" class="btn-text">I already have an account →</a>
	</div>
	<p class="hero-note">Built in Yaoundé, for students in all ten regions.</p>
</section>

<section class="steps" id="how-it-works">
	<p class="eyebrow">The process</p>
	<h2>How ApplyCM works</h2>

	<div class="steps-track">
		<div class="road-line" aria-hidden="true"></div>
		<div class="steps-grid">
			{#each steps as step}
				<div class="step-card">
					<span class="step-number">{step.number}</span>
					<h3>{step.title}</h3>
					<p>{step.body}</p>
				</div>
			{/each}
		</div>
	</div>
</section>

<section class="why">
	<div class="why-inner">
		<p class="eyebrow">Why we're building this</p>
		<h2>Applying to university in Cameroon shouldn't mean filling the same form four times.</h2>
		<p class="why-body">
			Between paper forms, campus queues, and photocopied transcripts, applying to more than one
			school often means starting from zero each time. ApplyCM is an early, growing platform
			putting that process online — one Cameroonian university at a time.
		</p>
		<p class="why-badge">Founding cohort · Yaoundé, Cameroon</p>
	</div>
</section>

<section class="contact">
	<div class="contact-inner">
		<h2>Have a question about applying?</h2>
		<p>Whether you're in Douala, Bamenda, Buea, or Kribi, our team is here to help you get started.</p>
		<a href="/contact" class="btn-light">Contact our team</a>
	</div>
</section>

<footer class="site-footer">
	<div class="footer-top">
		<span class="logo">Apply<span>CM</span></span>
		<nav>
			<a href="/#how-it-works">How it works</a>
			<a href="/signup">Create account</a>
			<a href="/login">Log in</a>
		</nav>
	</div>
	<p class="footer-copy">&copy; {new Date().getFullYear()} ApplyCM. Built in Cameroon.</p>
</footer>

<style>
	.eyebrow {
		font-family: var(--font-mono);
		font-size: 0.75rem;
		letter-spacing: 0.12em;
		text-transform: uppercase;
		color: var(--color-laterite);
		margin: 0 0 0.75rem;
	}

	/* Hero */
	.hero {
		max-width: 760px;
		margin: 0 auto;
		padding: 5rem 2rem 4rem;
		text-align: center;
	}
	.hero h1 {
		font-family: var(--font-display);
		font-size: clamp(2.2rem, 5vw, 3.4rem);
		line-height: 1.1;
		margin: 0 0 1.25rem;
		letter-spacing: -0.01em;
	}
	.hero-sub {
		font-size: 1.05rem;
		color: var(--color-ink-soft);
		line-height: 1.6;
		max-width: 560px;
		margin: 0 auto 2rem;
	}
	.hero-actions {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 1.5rem;
		flex-wrap: wrap;
	}
	.btn-primary {
		background: var(--color-laterite);
		color: #fff;
		text-decoration: none;
		font-weight: 600;
		padding: 0.9rem 1.8rem;
		border-radius: 999px;
		transition: background 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
	}
	.btn-primary:hover {
		background: var(--color-laterite-dark);
		transform: translateY(-3px);
		box-shadow: 0 14px 28px -14px rgba(180, 71, 43, 0.6);
	}
	.btn-text {
		background:#9e9a96;
		text-decoration: none;
		font-weight: 500;
		color: 'black';
		padding: 0.9rem 1.75rem;
		border-radius:500px;
		transition: background cubic-bezeir(0.6,0.04,0.98,0.335);
	}
	.btn-text:hover {
		transform: translatex(3px);
		transition: all 0.3s ease-in-out;
		box-shadow: 0.14px 28px -14px rgba(180, 71, 43,0.6);


	}
	.hero-note {
		margin-top: 2rem;
		font-family: var(--font-mono);
		font-size: 0.75rem;
		color: var(--color-ink-soft);
		letter-spacing: 0.03em;
	}

	/* Steps */
	.steps {
		max-width: 1080px;
		margin: 0 auto;
		padding: 4rem 2rem 5rem;
		text-align: center;
	}
	.steps h2 {
		font-family: var(--font-display);
		font-size: clamp(1.6rem, 3vw, 2.2rem);
		margin: 0 0 3rem;
	}
	.steps-track {
		position: relative;
	}
	.road-line {
		position: absolute;
		top: 1.1rem;
		left: 5%;
		right: 5%;
		height: 2px;
		background-image: repeating-linear-gradient(
			to right,
			var(--color-gold) 0,
			var(--color-gold) 10px,
			transparent 10px,
			transparent 20px
		);
		display: none;
	}
	.steps-grid {
		display: grid;
		grid-template-columns: repeat(4, 1fr);
		gap: 1.5rem;
		position: relative;
	}
	.step-card {
		text-align: left;
		background: #fff;
		border: 1px solid var(--color-line);
		border-radius: 20px;
		padding: 1.75rem 1.5rem;
		transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
	}
	.step-card:hover {
		transform: translateY(-6px);
		box-shadow: 0 20px 32px -20px rgba(32, 26, 20, 0.25);
		border-color: var(--color-gold);
	}
	.step-number {
		font-family: var(--font-mono);
		font-size: 0.85rem;
		color: var(--color-laterite);
		display: inline-block;
		margin-bottom: 0.75rem;
	}
	.step-card h3 {
		font-family: var(--font-display);
		font-size: 1.15rem;
		margin: 0 0 0.5rem;
	}
	.step-card p {
		font-size: 0.9rem;
		color: var(--color-ink-soft);
		line-height: 1.55;
		margin: 0;
	}

	@media (min-width: 860px) {
		.road-line {
			display: block;
		}
	}
	@media (max-width: 860px) {
		.steps-grid {
			grid-template-columns: 1fr;
		}
	}

	/* Why section */
	.why {
		background: #fff;
		border-top: 1px solid var(--color-line);
		border-bottom: 1px solid var(--color-line);
	}
	.why-inner {
		max-width: 680px;
		margin: 0 auto;
		padding: 5rem 2rem;
		text-align: center;
	}
	.why h2 {
		font-family: var(--font-display);
		font-size: clamp(1.5rem, 3vw, 2.1rem);
		line-height: 1.25;
		margin: 0 0 1.25rem;
	}
	.why-body {
		color: var(--color-ink-soft);
		line-height: 1.65;
		margin: 0 0 1.5rem;
	}
	.why-badge {
		display: inline-block;
		font-family: var(--font-mono);
		font-size: 0.75rem;
		letter-spacing: 0.04em;
		color: var(--color-ndole);
		background: rgba(31, 77, 58, 0.08);
		padding: 0.4rem 0.9rem;
		border-radius: 999px;
		margin: 0;
	}

	/* Contact / "have a question" */
	.contact {
		background: var(--color-ndole);
		color: #fff;
	}
	.contact-inner {
		max-width: 560px;
		margin: 0 auto;
		padding: 4.5rem 2rem;
		text-align: center;
	}
	.contact h2 {
		font-family: var(--font-display);
		font-size: clamp(1.5rem, 3vw, 2rem);
		margin: 0 0 0.75rem;
	}
	.contact p {
		opacity: 0.85;
		line-height: 1.6;
		margin: 0 0 2rem;
	}
	.btn-light {
		display: inline-block;
		background: #fff;
		color: var(--color-ndole);
		text-decoration: none;
		font-weight: 600;
		padding: 0.85rem 1.75rem;
		border-radius: 999px;
		transition: transform 0.2s ease, box-shadow 0.2s ease;
	}
	.btn-light:hover {
		transform: translateY(-3px);
		box-shadow: 0 14px 28px -14px rgba(0, 0, 0, 0.4);
	}

	/* Footer */
	.site-footer {
		max-width: 1080px;
		margin: 0 auto;
		padding: 3rem 2rem 2.5rem;
	}
	.footer-top {
		display: flex;
		align-items: center;
		justify-content: space-between;
		flex-wrap: wrap;
		gap: 1.5rem;
		padding-bottom: 1.5rem;
		border-bottom: 1px solid var(--color-line);
	}
	.footer-top .logo {
		font-family: var(--font-display);
		font-weight: 600;
		font-size: 1.15rem;
	}
	.footer-top .logo span {
		color: var(--color-laterite);
	}
	.footer-top nav {
		display: flex;
		gap: 1.5rem;
	}
	.footer-top nav a {
		text-decoration: none;
		font-size: 0.85rem;
		color: var(--color-ink-soft);
		transition: color 0.2s ease;
	}
	.footer-top nav a:hover {
		color: var(--color-ink);
	}
	.footer-copy {
		margin: 1.5rem 0 0;
		font-size: 0.8rem;
		color: var(--color-ink-soft);
	}
</style>