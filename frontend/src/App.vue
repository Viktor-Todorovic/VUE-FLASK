<script setup>
import { RouterLink, RouterView } from 'vue-router'
import Navigacija from './components/Navigacija.vue';
</script>

<template>
  <Navigacija />
  <RouterView />
</template>

<style>
:root {
  --bg: #f7f3ff;
  --bg-strong: #efe7ff;
  --surface: rgba(255, 255, 255, 0.86);
  --surface-solid: #ffffff;
  --text: #211a2f;
  --muted: #756b84;
  --line: rgba(83, 61, 112, 0.14);
  --primary: #7657d6;
  --primary-dark: #5f43bd;
  --accent: #e75a9a;
  --success: #158765;
  --danger: #d8475f;
  --shadow: 0 18px 50px rgba(64, 39, 103, 0.14);
  --shadow-soft: 0 10px 28px rgba(64, 39, 103, 0.1);
  --radius: 8px;
}

* {
  box-sizing: border-box;
}

html,
body,
#app {
  min-height: 100%;
}

html,
body {
  background:
    radial-gradient(circle at top left, rgba(231, 90, 154, 0.18), transparent 32rem),
    linear-gradient(135deg, var(--bg) 0%, #ffffff 52%, var(--bg-strong) 100%) !important;
  color: var(--text);
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  overflow-x: hidden;
}

body {
  margin: 0;
}

#app {
  padding-bottom: 4rem;
}

h1,
h2,
h3,
h4,
h5,
p {
  color: var(--text);
}

h1 {
  font-size: clamp(2rem, 4vw, 3.75rem);
  font-weight: 800;
  line-height: 1.05;
  letter-spacing: 0;
}

h2 {
  font-weight: 750;
  letter-spacing: 0;
}

a {
  color: var(--primary);
}

.navbar {
  position: sticky;
  top: 0;
  z-index: 20;
  margin: 1rem auto 0;
  width: min(1180px, calc(100% - 2rem));
  border: 1px solid rgba(255, 255, 255, 0.72);
  border-radius: var(--radius);
  background: rgba(255, 255, 255, 0.78) !important;
  box-shadow: var(--shadow-soft);
  backdrop-filter: blur(18px);
}

.navbar .container-fluid {
  padding: 0.75rem 1rem;
}

.navbar-collapse {
  align-items: center;
  gap: 0.75rem;
}

.navbar-nav {
  gap: 0.35rem;
  align-items: center;
}

.nav-link {
  border-radius: var(--radius);
  color: var(--muted) !important;
  font-weight: 700;
  padding: 0.65rem 0.9rem !important;
  transition: background-color 180ms ease, color 180ms ease, transform 180ms ease;
}

.nav-link:hover,
.nav-link.router-link-active {
  background: rgba(118, 87, 214, 0.11);
  color: var(--primary-dark) !important;
  transform: translateY(-1px);
}

.btn {
  border: 0;
  border-radius: var(--radius);
  font-weight: 750;
  letter-spacing: 0;
  box-shadow: none;
  transition: transform 180ms ease, box-shadow 180ms ease, background-color 180ms ease;
}

.btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 12px 22px rgba(64, 39, 103, 0.14);
}

.btn-primary {
  background: var(--primary) !important;
}

.btn-primary:hover,
.btn-primary:focus {
  background: var(--primary-dark) !important;
}

.btn-success {
  background: var(--success) !important;
}

.btn-danger {
  background: var(--danger) !important;
}

input,
select,
textarea {
  width: 100%;
  border: 1px solid var(--line) !important;
  border-radius: var(--radius) !important;
  background: rgba(255, 255, 255, 0.92) !important;
  color: var(--text) !important;
  outline: none;
  transition: border-color 160ms ease, box-shadow 160ms ease, background-color 160ms ease;
}

input:focus,
select:focus,
textarea:focus {
  border-color: rgba(118, 87, 214, 0.55) !important;
  box-shadow: 0 0 0 4px rgba(118, 87, 214, 0.12);
}

input[type="file"] {
  height: auto !important;
  padding: 0.65rem !important;
}

.card {
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.84) !important;
  border-radius: var(--radius) !important;
  background: var(--surface) !important;
  box-shadow: var(--shadow) !important;
}

.card-img-top,
.slika {
  object-fit: cover;
  background: #f2eef9;
}

.card-img-top {
  aspect-ratio: 4 / 3;
  cursor: pointer;
}

.card-body {
  padding: 1.15rem !important;
}

.card-title {
  color: var(--text);
  font-weight: 800;
}

.card-text {
  color: var(--muted) !important;
  line-height: 1.5;
}

hr {
  border-color: var(--line);
  opacity: 1;
}

.table {
  width: min(980px, calc(100% - 2rem)) !important;
  margin: 3rem auto !important;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.86);
  border-radius: var(--radius);
  background: var(--surface);
  box-shadow: var(--shadow);
}

thead {
  display: table-header-group;
  background: rgba(118, 87, 214, 0.1);
}

tbody {
  display: table-row-group;
}

tr {
  border-bottom: 1px solid var(--line);
}

th,
td {
  padding: 1rem;
  vertical-align: middle;
}

th {
  color: var(--text);
  font-size: 0.84rem;
  font-weight: 800;
  text-transform: uppercase;
}

td {
  color: var(--muted);
  font-weight: 600;
}

@media (max-width: 720px) {
  .navbar {
    width: calc(100% - 1rem);
    margin-top: 0.5rem;
  }

  th,
  td {
    padding: 0.75rem;
  }
}
</style>
