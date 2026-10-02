<script lang="ts">
  let {
    size = 28,
    showText = true,
    textColor = "inherit",
    cmColor = "#01CCC9",
    class: customClass = ""
  } = $props<{
    size?: number;
    showText?: boolean;
    textColor?: string;
    cmColor?: string;
    class?: string;
  }>();
</script>

<div class="applycm-logo {customClass}" style="--logo-size: {size}px;">
  <svg
    class="logo-mark"
    width={size}
    height={size}
    viewBox="0 0 100 100"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    aria-hidden="true"
  >
    <!-- Rounded Square Container -->
    <rect width="100" height="100" rx="25" fill="#0254A1" />
    <!-- Left White Angled 3D Panel -->
    <path
      d="M 20 29.5 L 43.8 19.5 L 43.8 81.5 L 20 71.5 Z"
      fill="#FFFFFF"
      stroke="#FFFFFF"
      stroke-width="2"
      stroke-linejoin="round"
      stroke-linecap="round"
    />
    <!-- Center Teal Pill -->
    <rect x="50.8" y="20.5" width="11.2" height="60.7" rx="5.6" fill="#01CCC9" />
    <!-- Right Orange Pill -->
    <rect x="68.7" y="26.3" width="9.3" height="48.4" rx="4.65" fill="#FCA72A" />
  </svg>

  {#if showText}
    <span class="logo-text" style="color: {textColor};">
      <span class="text-apply">Apply</span><span class="text-cm" style="color: {cmColor};">CM</span>
    </span>
  {/if}
</div>

<style>
  .applycm-logo {
    display: inline-flex;
    align-items: center;
    gap: 0.65rem;
    text-decoration: none;
    line-height: 1;
    user-select: none;
  }

  .logo-mark {
    flex-shrink: 0;
    width: var(--logo-size, 28px);
    height: var(--logo-size, 28px);
    display: block;
    border-radius: 22%;
    box-shadow: 0 2px 6px rgba(2, 84, 161, 0.25);
    transition: transform 0.2s ease;
  }

  .applycm-logo:hover .logo-mark {
    transform: scale(1.05);
  }

  .logo-text {
    font-size: calc(var(--logo-size, 28px) * 0.72);
    font-weight: 800;
    letter-spacing: -0.02em;
    display: inline-flex;
    align-items: baseline;
  }

  .text-apply {
    color: inherit;
  }

  .text-cm {
    color: #01CCC9;
    font-weight: 800;
  }
</style>
